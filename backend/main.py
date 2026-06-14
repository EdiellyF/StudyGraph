from datetime import datetime, timedelta
import os
from typing import Optional, List
import base64
from io import BytesIO

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
import jwt
from PIL import Image

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
    for collection_name in ["users", "posts", "follows", "likes", "comments", "notifications", "saved_posts"]:
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
    images: Optional[List[str]] = Field(None, description="Lista de imagens em base64")


class PostResponse(BaseModel):
    id: str
    content: str
    authorId: str
    authorName: str
    authorAvatar: Optional[str]
    images: Optional[List[str]] = None
    likesCount: int
    commentsCount: int
    createdAt: str


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)


class CommentResponse(BaseModel):
    id: str
    content: str
    authorId: str
    authorName: str
    authorAvatar: Optional[str]
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


@app.post("/profile/me/avatar")
async def upload_avatar(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    """Upload de avatar do usuário. Máximo 2MB, formatos: PNG, JPG, JPEG."""
    # Valida tipo de arquivo
    allowed_types = {"image/png", "image/jpeg", "image/jpg"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Formato de arquivo não permitido. Use PNG ou JPEG.")
    
    # Lê o arquivo
    contents = await file.read()
    
    # Verifica tamanho (máximo 2MB)
    if len(contents) > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Arquivo excede o tamanho máximo de 2MB")
    
    try:
        # Converte para base64
        avatar_base64 = base64.b64encode(contents).decode('utf-8')
        avatar_data_url = f"data:{file.content_type};base64,{avatar_base64}"
        
        # Comprime imagem
        compressed_avatar = validate_and_compress_image(avatar_data_url)
        
        # Atualiza usuário
        await db.users.update_one(
            {"_id": ObjectId(current_user["_id"])},
            {"$set": {"avatarUrl": compressed_avatar}}
        )
        
        updated = await db.users.find_one({"_id": ObjectId(current_user["_id"])})
        return user_response(updated)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar avatar: {str(e)}")


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


@app.get("/users/search")
async def search_users(q: str, current_user: dict = Depends(get_current_user), limit: int = 10):
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Query deve ter pelo menos 2 caracteres")
    
    cursor = db.users.find({
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"institution": {"$regex": q, "$options": "i"}},
            {"course": {"$regex": q, "$options": "i"}}
        ]
    }).limit(limit)
    
    users = await cursor.to_list(length=limit)
    
    return [
        {
            "id": str(user["_id"]),
            "name": user.get("name"),
            "institution": user.get("institution"),
            "course": user.get("course"),
            "followersCount": user.get("followersCount", 0),
        }
        for user in users
    ]


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    post_dict = post.model_dump()
    post_dict["authorId"] = str(current_user["_id"])
    post_dict["authorName"] = current_user.get("name")
    post_dict["authorAvatar"] = current_user.get("avatarUrl")
    post_dict["likesCount"] = 0
    post_dict["commentsCount"] = 0
    post_dict["createdAt"] = datetime.utcnow().isoformat()
    
    # Processa imagens se fornecidas
    if post_dict.get("images"):
        processed_images = []
        for img in post_dict["images"][:4]:  # Máximo 4 imagens
            try:
                compressed_img = validate_and_compress_image(img)
                processed_images.append(compressed_img)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        post_dict["images"] = processed_images
    else:
        post_dict["images"] = []

    result = await db.posts.insert_one(post_dict)
    created_post = await db.posts.find_one({"_id": result.inserted_id})

    return {
        "id": str(created_post["_id"]),
        "content": created_post["content"],
        "authorId": created_post["authorId"],
        "authorName": created_post["authorName"],
        "authorAvatar": created_post.get("authorAvatar"),
        "images": created_post.get("images", []),
        "likesCount": created_post["likesCount"],
        "commentsCount": created_post["commentsCount"],
        "createdAt": created_post["createdAt"],
    }


@app.get("/posts")
async def get_posts(current_user: dict = Depends(get_current_user), user_id: Optional[str] = None, limit: int = 20, skip: int = 0):
    filter_query = {}
    if user_id:
        filter_query["authorId"] = user_id
    
    cursor = db.posts.find(filter_query).sort("createdAt", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)

    return [
        {
            "id": str(post["_id"]),
            "content": post["content"],
            "authorId": post["authorId"],
            "authorName": post["authorName"],
            "authorAvatar": post.get("authorAvatar"),
            "images": post.get("images", []),
            "likesCount": post["likesCount"],
            "commentsCount": post["commentsCount"],
            "createdAt": post["createdAt"],
        }
        for post in posts
    ]


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="ID de post inválido")
    
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    if post["authorId"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Você não tem permissão para deletar este post")
    
    await db.posts.delete_one({"_id": ObjectId(post_id)})
    await db.likes.delete_many({"postId": post_id})
    await db.comments.delete_many({"postId": post_id})
    return


@app.post("/posts/{post_id}/like", status_code=status.HTTP_200_OK)
async def like_post(post_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="ID de post inválido")
    
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    # Verifica se já curtiu
    existing_like = await db.likes.find_one({
        "postId": post_id,
        "userId": str(current_user["_id"])
    })
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Você já curtiu este post")
    
    # Adiciona like
    await db.likes.insert_one({
        "postId": post_id,
        "userId": str(current_user["_id"]),
        "createdAt": datetime.utcnow().isoformat()
    })
    
    # Incrementa contador
    await db.posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$inc": {"likesCount": 1}}
    )
    
    return {"message": "Post curtido com sucesso"}


@app.delete("/posts/{post_id}/like", status_code=status.HTTP_200_OK)
async def unlike_post(post_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="ID de post inválido")
    
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    # Verifica se curtiu
    existing_like = await db.likes.find_one({
        "postId": post_id,
        "userId": str(current_user["_id"])
    })
    
    if not existing_like:
        raise HTTPException(status_code=400, detail="Você não curtiu este post")
    
    # Remove like
    await db.likes.delete_one({
        "postId": post_id,
        "userId": str(current_user["_id"])
    })
    
    # Decrementa contador
    await db.posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$inc": {"likesCount": -1}}
    )
    
    return {"message": "Like removido com sucesso"}


@app.post("/posts/{post_id}/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: str, comment: CommentCreate, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="ID de post inválido")
    
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    comment_dict = {
        "postId": post_id,
        "authorId": str(current_user["_id"]),
        "authorName": current_user.get("name"),
        "authorAvatar": current_user.get("avatarUrl"),
        "content": comment.content,
        "createdAt": datetime.utcnow().isoformat()
    }
    
    result = await db.comments.insert_one(comment_dict)
    
    # Incrementa contador
    await db.posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$inc": {"commentsCount": 1}}
    )
    
    return {
        "id": str(result.inserted_id),
        "content": comment_dict["content"],
        "authorId": comment_dict["authorId"],
        "authorName": comment_dict["authorName"],
        "authorAvatar": comment_dict.get("authorAvatar"),
        "createdAt": comment_dict["createdAt"]
    }


@app.get("/posts/{post_id}/comments")
async def get_comments(post_id: str, current_user: dict = Depends(get_current_user), limit: int = 20, skip: int = 0):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="ID de post inválido")
    
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    cursor = db.comments.find({"postId": post_id}).sort("createdAt", -1).skip(skip).limit(limit)
    comments = await cursor.to_list(length=limit)
    
    return [
        {
            "id": str(comment["_id"]),
            "content": comment["content"],
            "authorId": comment["authorId"],
            "authorName": comment["authorName"],
            "authorAvatar": comment.get("authorAvatar"),
            "createdAt": comment["createdAt"]
        }
        for comment in comments
    ]


@app.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(comment_id):
        raise HTTPException(status_code=400, detail="ID de comentário inválido")
    
    comment = await db.comments.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    if comment["authorId"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Você não tem permissão para deletar este comentário")
    
    await db.comments.delete_one({"_id": ObjectId(comment_id)})
    
    # Decrementa contador
    await db.posts.update_one(
        {"_id": ObjectId(comment["postId"])},
        {"$inc": {"commentsCount": -1}}
    )
    return


@app.post("/posts/{post_id}/save", status_code=status.HTTP_200_OK)
async def save_post(post_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="ID de post inválido")
    
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    # Verifica se já salvou
    existing_save = await db.saved_posts.find_one({
        "postId": post_id,
        "userId": str(current_user["_id"])
    })
    
    if existing_save:
        raise HTTPException(status_code=400, detail="Você já salvou este post")
    
    # Salva post
    await db.saved_posts.insert_one({
        "postId": post_id,
        "userId": str(current_user["_id"]),
        "createdAt": datetime.utcnow().isoformat()
    })
    
    return {"message": "Post salvo com sucesso"}


@app.delete("/posts/{post_id}/save", status_code=status.HTTP_200_OK)
async def unsave_post(post_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="ID de post inválido")
    
    # Remove save
    result = await db.saved_posts.delete_one({
        "postId": post_id,
        "userId": str(current_user["_id"])
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=400, detail="Você não salvou este post")
    
    return {"message": "Post removido dos salvos"}


@app.get("/saved-posts")
async def get_saved_posts(current_user: dict = Depends(get_current_user), limit: int = 20, skip: int = 0):
    # Busca IDs dos posts salvos
    saved_cursor = db.saved_posts.find({"userId": str(current_user["_id"])}).sort("createdAt", -1).skip(skip).limit(limit)
    saved = await saved_cursor.to_list(length=limit)
    
    post_ids = [ObjectId(s["postId"]) for s in saved]
    
    # Busca os posts
    posts_cursor = db.posts.find({"_id": {"$in": post_ids}})
    posts = await posts_cursor.to_list(length=limit)
    
    return [
        {
            "id": str(post["_id"]),
            "content": post["content"],
            "authorId": post["authorId"],
            "authorName": post["authorName"],
            "authorAvatar": post.get("authorAvatar"),
            "images": post.get("images", []),
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


@app.post("/users/{user_id}/follow", status_code=status.HTTP_200_OK)
async def follow_user(user_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido")
    
    if user_id == str(current_user["_id"]):
        raise HTTPException(status_code=400, detail="Você não pode seguir a si mesmo")
    
    user_to_follow = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verifica se já segue
    existing_follow = await db.follows.find_one({
        "followerId": str(current_user["_id"]),
        "followingId": user_id
    })
    if existing_follow:
        raise HTTPException(status_code=400, detail="Você já está seguindo este usuário")
    
    # Cria relacionamento de follow
    await db.follows.insert_one({
        "followerId": str(current_user["_id"]),
        "followingId": user_id,
        "createdAt": datetime.utcnow().isoformat()
    })
    
    # Atualiza contadores
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {"followersCount": 1}}
    )
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$inc": {"followingCount": 1}}
    )
    
    return {"message": "Usuário seguido com sucesso"}


@app.delete("/users/{user_id}/follow", status_code=status.HTTP_200_OK)
async def unfollow_user(user_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido")
    
    user_to_unfollow = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user_to_unfollow:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verifica se segue
    existing_follow = await db.follows.find_one({
        "followerId": str(current_user["_id"]),
        "followingId": user_id
    })
    if not existing_follow:
        raise HTTPException(status_code=400, detail="Você não está seguindo este usuário")
    
    # Remove relacionamento de follow
    await db.follows.delete_one({
        "followerId": str(current_user["_id"]),
        "followingId": user_id
    })
    
    # Atualiza contadores
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {"followersCount": -1}}
    )
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$inc": {"followingCount": -1}}
    )
    
    return {"message": "Usuário deixado de seguir com sucesso"}


@app.get("/notifications")
async def get_notifications(current_user: dict = Depends(get_current_user), limit: int = 20, skip: int = 0):
    cursor = db.notifications.find({"userId": str(current_user["_id"])}).sort("createdAt", -1).skip(skip).limit(limit)
    notifications = await cursor.to_list(length=limit)
    
    return [
        {
            "id": str(notif["_id"]),
            "type": notif.get("type"),
            "message": notif.get("message"),
            "fromUserId": notif.get("fromUserId"),
            "fromUserName": notif.get("fromUserName"),
            "postId": notif.get("postId"),
            "read": notif.get("read", False),
            "createdAt": notif.get("createdAt")
        }
        for notif in notifications
    ]


@app.put("/notifications/{notification_id}/read", status_code=status.HTTP_200_OK)
async def mark_notification_read(notification_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(status_code=400, detail="ID de notificação inválido")
    
    await db.notifications.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": {"read": True}}
    )
    
    return {"message": "Notificação marcada como lida"}


def validate_and_compress_image(image_base64: str, max_size_mb: float = 2.0) -> str:
    """Valida e comprime imagem em base64. Retorna a imagem comprimida em base64."""
    try:
        # Remove prefixo data:image se existir
        if image_base64.startswith('data:image'):
            image_base64 = image_base64.split(',')[1]
        
        # Decodifica base64
        image_data = base64.b64decode(image_base64)
        
        # Verifica tamanho máximo
        max_size_bytes = max_size_mb * 1024 * 1024
        if len(image_data) > max_size_bytes:
            raise ValueError(f"Imagem excede o tamanho máximo de {max_size_mb}MB")
        
        # Abre imagem com PIL
        image = Image.open(BytesIO(image_data))
        
        # Converte para RGB se necessário
        if image.mode in ('RGBA', 'LA', 'P'):
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = rgb_image
        
        # Redimensiona se muito grande (máximo 1920x1920)
        max_dimension = 1920
        if image.width > max_dimension or image.height > max_dimension:
            image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        
        # Comprime e salva em base64
        output = BytesIO()
        image.save(output, format='JPEG', quality=85, optimize=True)
        compressed_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
        
        return f"data:image/jpeg;base64,{compressed_base64}"
    except Exception as e:
        raise ValueError(f"Erro ao processar imagem: {str(e)}")
