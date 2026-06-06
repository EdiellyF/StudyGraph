from datetime import datetime, timedelta
import os
from typing import Optional

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
import jwt

load_dotenv()

app = FastAPI(title="StudyGraph API")

SECRET_KEY = os.getenv("SECRET_KEY", "1234567890abcdef")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "studygraph")

if not MONGO_URI:
    raise ValueError("⚠️ MONGO_URI não encontrada! Verifique seu arquivo .env")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

@app.on_event("startup")
async def ensure_collections():
    existing = await db.list_collection_names()
    for collection_name in ["users", "posts", "follows"]:
        if collection_name not in existing:
            await db.create_collection(collection_name)

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)
    semester: Optional[str] = None
    institution: Optional[str] = None
    course: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserProfileUpdate(BaseModel):
    name: Optional[str]
    institution: Optional[str]
    course: Optional[str]
    semester: Optional[str]
    bio: Optional[str]


class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class PostResponse(BaseModel):
    id: str
    content: str
    authorId: str
    authorName: str
    authorAvatar: Optional[str]
    likesCount: int
    commentsCount: int
    createdAt: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user


def user_response(user: dict):
    return {
        "id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
        "institution": user.get("institution"),
        "course": user.get("course"),
        "semester": user.get("semester"),
        "bio": user.get("bio"),
        "followersCount": user.get("followersCount", 0),
        "followingCount": user.get("followingCount", 0),
        "createdAt": user.get("createdAt"),
    }


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    # Verifica se o email já existe
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Hash da senha e inserção no banco
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.model_dump()
    user_dict["password"] = hashed_password
    user_dict["followersCount"] = 0
    user_dict["followingCount"] = 0
    user_dict["createdAt"] = datetime.utcnow().isoformat()

    await db.users.insert_one(user_dict)
    return {"message": "Usuário criado com sucesso!"}

@app.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    access_token = create_access_token(data={"sub": str(db_user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile/me")
async def read_my_profile(current_user: dict = Depends(get_current_user)):
    return user_response(current_user)


@app.put("/profile/me")
async def update_my_profile(update: UserProfileUpdate, current_user: dict = Depends(get_current_user)):
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

    await db.users.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": update_data})
    updated = await db.users.find_one({"_id": ObjectId(current_user["_id"])})
    return user_response(updated)


@app.delete("/profile/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_profile(current_user: dict = Depends(get_current_user)):
    await db.users.delete_one({"_id": ObjectId(current_user["_id"])})
    return


@app.get("/profile/{user_id}")
async def read_profile(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido")
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user_response(user)


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    post_dict = post.model_dump()
    post_dict["authorId"] = str(current_user["_id"])
    post_dict["authorName"] = current_user.get("name")
    post_dict["authorAvatar"] = current_user.get("avatarUrl")
    post_dict["likesCount"] = 0
    post_dict["commentsCount"] = 0
    post_dict["createdAt"] = datetime.utcnow().isoformat()

    result = await db.posts.insert_one(post_dict)
    created_post = await db.posts.find_one({"_id": result.inserted_id})

    return {
        "id": str(created_post["_id"]),
        "content": created_post["content"],
        "authorId": created_post["authorId"],
        "authorName": created_post["authorName"],
        "authorAvatar": created_post.get("authorAvatar"),
        "likesCount": created_post["likesCount"],
        "commentsCount": created_post["commentsCount"],
        "createdAt": created_post["createdAt"],
    }


@app.get("/posts")
async def get_posts(current_user: dict = Depends(get_current_user), limit: int = 20, skip: int = 0):
    cursor = db.posts.find().sort("createdAt", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)

    return [
        {
            "id": str(post["_id"]),
            "content": post["content"],
            "authorId": post["authorId"],
            "authorName": post["authorName"],
            "authorAvatar": post.get("authorAvatar"),
            "likesCount": post["likesCount"],
            "commentsCount": post["commentsCount"],
            "createdAt": post["createdAt"],
        }
        for post in posts
    ]


@app.get("/users/suggested")
async def get_suggested_users(current_user: dict = Depends(get_current_user), limit: int = 5):
    cursor = db.users.find({"_id": {"$ne": current_user["_id"]}}).limit(limit)
    users = await cursor.to_list(length=limit)

    return [
        {
            "id": str(user["_id"]),
            "name": user.get("name"),
            "institution": user.get("institution"),
            "course": user.get("course"),
            "avatarUrl": user.get("avatarUrl"),
            "followersCount": user.get("followersCount", 0),
        }
        for user in users
    ]