from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import os
import uuid
import logging
import requests
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Any, Dict

import bcrypt
import jwt
from fastapi import (
    FastAPI, APIRouter, Depends, HTTPException, Header, UploadFile, File, Request, Response
)
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, ConfigDict

from seed_data import build_menu_seed, OUTLETS_SEED, CATEGORIES_ORDER

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALG = "HS256"
JWT_EXPIRES_MIN = int(os.environ.get("JWT_EXPIRES_MIN", "720"))
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY", "")
APP_NAME = os.environ.get("APP_NAME", "pjours")

STORAGE_URL = "https://integrations.emergentagent.com/objstore/api/v1/storage"
_storage_key: Optional[str] = None

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("pjours")

# ---------------------------------------------------------------------------
# Mongo
# ---------------------------------------------------------------------------
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# ---------------------------------------------------------------------------
# Security helpers
# ---------------------------------------------------------------------------
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_admin_token() -> str:
    payload = {
        "sub": "admin",
        "role": "admin",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRES_MIN),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def require_admin(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization[7:]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return payload


# ---------------------------------------------------------------------------
# Object storage
# ---------------------------------------------------------------------------
def init_storage() -> Optional[str]:
    global _storage_key
    if _storage_key:
        return _storage_key
    if not EMERGENT_LLM_KEY:
        logger.warning("EMERGENT_LLM_KEY not set; object storage disabled")
        return None
    try:
        resp = requests.post(
            f"{STORAGE_URL}/init",
            json={"emergent_key": EMERGENT_LLM_KEY},
            timeout=30,
        )
        resp.raise_for_status()
        _storage_key = resp.json()["storage_key"]
        logger.info("Object storage initialised")
        return _storage_key
    except Exception as e:
        logger.error(f"Object storage init failed: {e}")
        return None


def put_object(path: str, data: bytes, content_type: str) -> dict:
    key = init_storage()
    if not key:
        raise HTTPException(status_code=500, detail="Object storage unavailable")
    resp = requests.put(
        f"{STORAGE_URL}/objects/{path}",
        headers={"X-Storage-Key": key, "Content-Type": content_type},
        data=data,
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def get_object(path: str):
    key = init_storage()
    if not key:
        raise HTTPException(status_code=500, detail="Object storage unavailable")
    resp = requests.get(
        f"{STORAGE_URL}/objects/{path}",
        headers={"X-Storage-Key": key},
        timeout=60,
    )
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="File not found")
    resp.raise_for_status()
    return resp.content, resp.headers.get("Content-Type", "application/octet-stream")


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------
class SizeVariant(BaseModel):
    label: str
    price: float


class MenuItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: str
    name: str
    base_price: float
    sizes: List[SizeVariant] = []
    image_url: Optional[str] = None
    active: bool = True
    popular: bool = False
    popular_order: int = 0
    position: int = 0


class MenuItemCreate(BaseModel):
    category: str
    name: str
    base_price: float
    sizes: List[SizeVariant] = []
    image_url: Optional[str] = None
    active: bool = True
    popular: bool = False
    popular_order: int = 0


class MenuItemUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    base_price: Optional[float] = None
    sizes: Optional[List[SizeVariant]] = None
    image_url: Optional[str] = None
    active: Optional[bool] = None
    popular: Optional[bool] = None
    popular_order: Optional[int] = None


class Outlet(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    full_address: str
    whatsapp: str
    map_query: str
    hours: str
    position: int = 0


class OutletUpdate(BaseModel):
    name: Optional[str] = None
    full_address: Optional[str] = None
    whatsapp: Optional[str] = None
    map_query: Optional[str] = None
    hours: Optional[str] = None


class LoginRequest(BaseModel):
    password: str


class TokenResponse(BaseModel):
    token: str
    expires_in: int


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(title="PJ Ours API")
api = APIRouter(prefix="/api")


# ---------------- Seeding ----------------
async def seed_if_needed():
    # Menu seed
    count = await db.menu_items.count_documents({})
    if count == 0:
        items = build_menu_seed()
        docs = []
        for it in items:
            doc = {"id": str(uuid.uuid4()), **it}
            docs.append(doc)
        if docs:
            await db.menu_items.insert_many(docs)
            logger.info(f"Seeded {len(docs)} menu items")

    # Outlets seed / upsert (keeps the core WhatsApp numbers even after restart if doc exists)
    for o in OUTLETS_SEED:
        existing = await db.outlets.find_one({"id": o["id"]})
        if existing is None:
            await db.outlets.insert_one(o)
    logger.info("Outlets ensured")


@app.on_event("startup")
async def _startup():
    await seed_if_needed()
    # Init storage in background — don't crash if it fails
    init_storage()


@app.on_event("shutdown")
async def _shutdown():
    client.close()


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------
@api.get("/")
async def root():
    return {"service": "pj-ours", "ok": True}


@api.get("/categories")
async def get_categories():
    return {"categories": CATEGORIES_ORDER}


@api.get("/menu", response_model=List[MenuItem])
async def get_menu(active_only: bool = True):
    q = {"active": True} if active_only else {}
    cursor = db.menu_items.find(q, {"_id": 0}).sort("position", 1)
    items = await cursor.to_list(length=1000)
    return items


@api.get("/outlets", response_model=List[Outlet])
async def get_outlets():
    cursor = db.outlets.find({}, {"_id": 0}).sort("position", 1)
    return await cursor.to_list(length=20)


@api.get("/popular", response_model=List[MenuItem])
async def get_popular(limit: int = 5):
    cursor = db.menu_items.find(
        {"popular": True, "active": True}, {"_id": 0}
    ).sort("popular_order", 1)
    items = await cursor.to_list(length=50)
    return items[:limit]


# Public image serving (menu images are public)
@api.get("/files/{path:path}")
async def serve_file(path: str):
    data, content_type = get_object(path)
    return Response(content=data, media_type=content_type)


# ---------------------------------------------------------------------------
# Admin auth
# ---------------------------------------------------------------------------
@api.post("/admin/login", response_model=TokenResponse)
async def admin_login(body: LoginRequest):
    # We keep the hashed password in memory per process — hashed from env at first login.
    # Simple throttle: use login_attempts collection.
    ip_key = "admin_global"  # single-user, no per-IP needed
    attempt = await db.login_attempts.find_one({"id": ip_key})
    now = datetime.now(timezone.utc)
    if attempt and attempt.get("lock_until") and now.timestamp() < attempt["lock_until"]:
        raise HTTPException(status_code=429, detail="Too many failed attempts. Try again later.")

    if body.password != ADMIN_PASSWORD:
        # increment fail count
        fails = (attempt or {}).get("fails", 0) + 1
        lock_until = 0
        if fails >= 5:
            lock_until = (now + timedelta(minutes=15)).timestamp()
            fails = 0
        await db.login_attempts.update_one(
            {"id": ip_key},
            {"$set": {"id": ip_key, "fails": fails, "lock_until": lock_until}},
            upsert=True,
        )
        raise HTTPException(status_code=401, detail="Invalid password")

    # Success: clear attempts
    await db.login_attempts.delete_one({"id": ip_key})
    token = create_admin_token()
    return TokenResponse(token=token, expires_in=JWT_EXPIRES_MIN * 60)


@api.get("/admin/me")
async def admin_me(payload: Dict[str, Any] = Depends(require_admin)):
    return {"role": payload.get("role"), "ok": True}


# ---------------------------------------------------------------------------
# Admin: Menu CRUD
# ---------------------------------------------------------------------------
@api.get("/admin/menu", response_model=List[MenuItem], dependencies=[Depends(require_admin)])
async def admin_list_menu():
    cursor = db.menu_items.find({}, {"_id": 0}).sort("position", 1)
    return await cursor.to_list(length=1000)


@api.post("/admin/menu", response_model=MenuItem)
async def admin_create_item(body: MenuItemCreate, _: Any = Depends(require_admin)):
    # Next position
    last = await db.menu_items.find_one({}, {"_id": 0, "position": 1}, sort=[("position", -1)])
    next_position = (last["position"] + 1) if last else 1
    item = MenuItem(**body.model_dump(), position=next_position)
    doc = item.model_dump()
    await db.menu_items.insert_one(doc)
    return item


@api.put("/admin/menu/{item_id}", response_model=MenuItem)
async def admin_update_item(item_id: str, body: MenuItemUpdate, _: Any = Depends(require_admin)):
    update = {k: v for k, v in body.model_dump().items() if v is not None}
    if not update:
        raise HTTPException(status_code=400, detail="No fields to update")
    # Convert pydantic SizeVariant → dict
    if "sizes" in update and update["sizes"] is not None:
        update["sizes"] = [
            s.model_dump() if hasattr(s, "model_dump") else s for s in update["sizes"]
        ]
    res = await db.menu_items.update_one({"id": item_id}, {"$set": update})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = await db.menu_items.find_one({"id": item_id}, {"_id": 0})
    return updated


@api.delete("/admin/menu/{item_id}")
async def admin_delete_item(item_id: str, _: Any = Depends(require_admin)):
    res = await db.menu_items.delete_one({"id": item_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}


# ---------------------------------------------------------------------------
# Admin: Outlet updates
# ---------------------------------------------------------------------------
@api.put("/admin/outlets/{outlet_id}", response_model=Outlet)
async def admin_update_outlet(outlet_id: str, body: OutletUpdate, _: Any = Depends(require_admin)):
    update = {k: v for k, v in body.model_dump().items() if v is not None}
    if not update:
        raise HTTPException(status_code=400, detail="No fields to update")
    res = await db.outlets.update_one({"id": outlet_id}, {"$set": update})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Outlet not found")
    updated = await db.outlets.find_one({"id": outlet_id}, {"_id": 0})
    return updated


# ---------------------------------------------------------------------------
# Admin: Upload
# ---------------------------------------------------------------------------
MIME_MAP = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
}
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB


@api.post("/admin/upload")
async def admin_upload(
    request: Request,
    file: UploadFile = File(...),
    _: Any = Depends(require_admin),
):
    content_type = (file.content_type or "").lower()
    if content_type not in MIME_MAP:
        raise HTTPException(status_code=400, detail="Unsupported file type (use JPEG / PNG / WEBP / GIF)")
    data = await file.read()
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds 5 MB limit")

    ext = MIME_MAP[content_type]
    path = f"{APP_NAME}/menu/{uuid.uuid4()}.{ext}"
    result = put_object(path, data, content_type)

    # Record in db (soft-delete-able)
    await db.files.insert_one({
        "id": str(uuid.uuid4()),
        "storage_path": result["path"],
        "original_filename": file.filename,
        "content_type": content_type,
        "size": len(data),
        "is_deleted": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })

    # Build a browser-accessible URL via our /api/files proxy endpoint
    # (uses REACT_APP_BACKEND_URL-style path; frontend can prefix the backend host)
    public_url = f"/api/files/{result['path']}"
    return {"url": public_url, "path": result["path"], "size": len(data)}


# ---------------------------------------------------------------------------
# Mount router + middleware
# ---------------------------------------------------------------------------
app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)
