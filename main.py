# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Union
from datetime import datetime, timedelta
# from jose import JWTError, jwt
from passlib.context import CryptContext
from enum import Enum
import secrets

# 示例数据
plants = [
    {"id": 1, "name": "玫瑰", "type": "花卉", "description": "美丽而受欢迎的花卉，需要充足阳光和定期修剪。",
     "imageUrl": "https://picsum.photos/id/152/400/300"},
    {"id": 2, "name": "绿萝", "type": "盆栽", "description": "常见的室内观叶植物，耐阴，容易养护。",
     "imageUrl": "https://picsum.photos/id/106/400/300"},
    {"id": 3, "name": "番茄", "type": "蔬菜", "description": "适合家庭种植的蔬菜，需要充足阳光和肥沃土壤。",
     "imageUrl": "https://picsum.photos/id/292/400/300"},
    {"id": 4, "name": "草莓", "type": "水果", "description": "美味的小型水果，适合阳台种植。",
     "imageUrl": "https://picsum.photos/id/175/400/300"},
    {"id": 5, "name": "多肉植物", "type": "盆栽", "description": "肉质叶片的植物，耐旱，适合懒人养护。",
     "imageUrl": "https://picsum.photos/id/325/400/300"}
]

care_guides = [
    {
        "id": 1,
        "title": "植物浇水的正确方法与频率",
        "content": "不同植物对水分需求不同...",
        "author": "李园丁",
        "authorAvatar": "https://picsum.photos/id/1005/50/50",
        "publish_date": "2025-05-15",
        "category": "浇水",
        "categoryColor": "blue",
        "imageUrl": "https://picsum.photos/id/106/400/300",
        "date": "2025年5月15日",
        "summary": "了解不同植物的需水量和浇水频率，避免过度浇水或浇水不足对植物造成的伤害..."
    },
    {
        "id": 2,
        "title": "不同植物的光照需求与摆放位置",
        "content": "根据植物的光照需求合理摆放...",
        "author": "王园艺师",
        "authorAvatar": "https://picsum.photos/id/1012/50/50",
        "publish_date": "2025-05-10",
        "category": "光照",
        "categoryColor": "yellow",
        "imageUrl": "https://picsum.photos/id/110/400/300",
        "date": "2025年5月10日",
        "summary": "了解不同植物对光照的需求，合理安排植物在室内外的摆放位置，让植物获得充足但不过量的光照..."
    },
    {
        "id": 3,
        "title": "家庭种植的土壤选择与配制",
        "content": "了解不同植物对土壤的要求...",
        "author": "张花匠",
        "authorAvatar": "https://picsum.photos/id/1027/50/50",
        "publish_date": "2025-05-05",
        "category": "土壤",
        "categoryColor": "brown",
        "imageUrl": "https://picsum.photos/id/145/400/300",
        "date": "2025年5月5日",
        "summary": "土壤是植物生长的基础，不同植物对土壤的要求各不相同。本文将介绍常见家庭植物的土壤选择和配制方法..."
    },
    {
        "id": 4,
        "title": "家庭植物的施肥时间与方法",
        "content": "正确的施肥是植物健康生长的关键...",
        "author": "刘教授",
        "authorAvatar": "https://picsum.photos/id/1074/50/50",
        "publish_date": "2025-04-28",
        "category": "施肥",
        "categoryColor": "green",
        "imageUrl": "https://picsum.photos/id/180/400/300",
        "date": "2025年4月28日",
        "summary": "施肥是植物养护中的重要环节，但很多人不知道何时施肥、施什么肥。本文将为您详细介绍家庭植物的施肥技巧..."
    },
    {
        "id": 5,
        "title": "夏季植物养护要点",
        "content": "夏季高温对植物的影响及应对措施...",
        "author": "陈专家",
        "authorAvatar": "https://picsum.photos/id/1062/50/50",
        "publish_date": "2025-04-20",
        "category": "季节养护",
        "categoryColor": "red",
        "imageUrl": "https://picsum.photos/id/21/400/300",
        "date": "2025年4月20日",
        "summary": "夏季高温多雨，是植物生长的旺季，但也是病虫害高发期。如何在夏季为植物提供最佳的生长环境？本文将为您提供专业建议..."
    }
]

problems = [
    {"id": 1, "question": "植物叶子发黄是什么原因？",
     "answer": "植物叶子发黄可能由多种原因引起，包括浇水过多或过少、光照不足、营养缺乏、温度不适、病虫害等。具体原因需要结合植物的具体情况进行分析...",
     "category": "常见问题"},
    {"id": 2, "question": "如何防治常见的植物病虫害？",
     "answer": "常见的植物病虫害包括蚜虫、白粉病、红蜘蛛、介壳虫等。防治方法包括物理防治（如手动清除）、生物防治（如引入天敌）和化学防治（如使用杀虫剂）。应根据病虫害的类型和严重程度选择合适的防治方法...",
     "category": "病虫害防治"},
    {"id": 3, "question": "室内植物如何增加湿度？",
     "answer": "增加湿度的方法包括喷雾、使用加湿器、放置水盆、群植等。不同的植物对湿度的要求不同，大多数热带植物需要较高的湿度。在干燥的季节，特别是冬季，增加湿度对室内植物的健康非常重要...",
     "category": "环境管理"},
    {"id": 4, "question": "如何判断植物是否需要浇水？",
     "answer": "判断植物是否需要浇水可以通过观察土壤干湿、植物叶片状态、重量法等方法。一般来说，当土壤表面干燥约2厘米时，就是浇水的适当时机。但不同植物对水分的需求差异很大，需要根据具体植物进行调整...",
     "category": "浇水管理"},
    {"id": 5, "question": "盆栽植物如何换盆？",
     "answer": "换盆时机一般选择在植物休眠期或生长初期。换盆时需要选择比原来稍大的花盆，使用合适的土壤，并注意不要损伤植物根系。换盆后需要适当浇水，并避免阳光直射，直到植物适应新环境...",
     "category": "盆栽管理"}
]

community_posts = [
    {
        "id": 1,
        "title": "我的阳台小花园终于成型了！",
        "content": "经过三个月的努力，我的阳台小花园终于有了雏形...",
        "username": "陈小花",
        "userAvatar": "https://picsum.photos/id/1027/50/50",
        "publish_date": "2025-05-25",
        "timeAgo": "2天前",
        "category": "花园展示",
        "likes": 42,
        "comments": 18,
        "images": ["https://picsum.photos/id/145/300/200", "https://picsum.photos/id/292/300/200",
                   "https://picsum.photos/id/175/300/200"],
        "author": "陈小花",  # 添加缺失的author字段，与username保持一致
        "timaAgo": "2天前"  # 添加缺失的timaAgo字段（可能是模型拼写错误）
    },
    {
        "id": 2,
        "title": "我的多肉植物叶子变软了，怎么办？",
        "content": "最近发现我的多肉植物叶子开始变软...",
        "username": "林园丁",
        "userAvatar": "https://picsum.photos/id/1074/50/50",
        "publish_date": "2025-05-20",
        "timeAgo": "7天前",
        "category": "求助",
        "likes": 28,
        "comments": 35,
        "images": ["https://picsum.photos/id/325/300/200"],
        "author": "林园丁",  # 添加缺失的author字段
        "timaAgo": "7天前"  # 添加缺失的timaAgo字段
    },
    {
        "id": 3,
        "title": "分享我的室内植物装饰方案",
        "content": "如何利用植物美化室内空间...",
        "username": "王设计师",
        "userAvatar": "https://picsum.photos/id/1062/50/50",
        "publish_date": "2025-05-18",
        "timeAgo": "9天前",
        "category": "装饰灵感",
        "likes": 56,
        "comments": 24,
        "images": ["https://picsum.photos/id/106/300/200", "https://picsum.photos/id/110/300/200"],
        "author": "王设计师",  # 添加缺失的author字段
        "timaAgo": "9天前"  # 添加缺失的timaAgo字段
    },
    {
        "id": 4,
        "title": "第一次尝试水培，成功了！",
        "content": "水培植物的优点和注意事项...",
        "username": "赵水培",
        "userAvatar": "https://picsum.photos/id/1025/50/50",
        "publish_date": "2025-05-15",
        "timeAgo": "12天前",
        "category": "种植经验",
        "likes": 32,
        "comments": 17,
        "images": ["https://picsum.photos/id/104/300/200", "https://picsum.photos/id/106/300/200"],
        "author": "赵水培",  # 添加缺失的author字段
        "timaAgo": "12天前"  # 添加缺失的timaAgo字段
    },
    {
        "id": 5,
        "title": "请教：我的月季花生病了，如何治疗？",
        "content": "我的月季叶片上出现了白斑...",
        "username": "钱花匠",
        "userAvatar": "https://picsum.photos/id/1012/50/50",
        "publish_date": "2025-05-10",
        "timeAgo": "17天前",
        "category": "病虫害",
        "likes": 19,
        "comments": 29,
        "images": ["https://picsum.photos/id/152/300/200"],
        "author": "钱花匠",  # 添加缺失的author字段
        "timaAgo": "17天前"  # 添加缺失的timaAgo字段
    }
]


# 用户模型
class UserType(str, Enum):
    admin = "admin"
    user = "user"


class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    user_type: UserType = UserType.user


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True


# 植物模型
class PlantType(str, Enum):
    flower = "花卉"
    potted = "盆栽"
    vegetable = "蔬菜"
    fruit = "水果"
    other = "其他"


class PlantBase(BaseModel):
    name: str
    type: PlantType
    description: str
    imageUrl: str


class PlantCreate(PlantBase):
    pass


class Plant(PlantBase):
    id: int

    class Config:
        orm_mode = True


# 养护指南模型
class GuideCategory(str, Enum):
    watering = "浇水"
    lighting = "光照"
    soil = "土壤"
    fertilization = "施肥"
    pruning = "修剪"
    season = "季节养护"
    pest_control = "病虫害防治"


class CareGuideBase(BaseModel):
    title: str
    content: str
    author: str
    publish_date: str
    category: GuideCategory
    imageUrl: str
    categoryColor: str
    date: str
    authorAvatar: str
    summary: str


class CareGuideCreate(CareGuideBase):
    pass


class CareGuide(CareGuideBase):
    id: int

    class Config:
        orm_mode = True


# 问题模型
class ProblemCategory(str, Enum):
    common = "常见问题"
    pest = "病虫害防治"
    environment = "环境管理"
    watering = "浇水管理"
    fertilization = "施肥管理"
    potting = "盆栽管理"


class ProblemBase(BaseModel):
    question: str
    answer: str
    category: ProblemCategory


class ProblemCreate(ProblemBase):
    pass


class Problem(ProblemBase):
    id: int

    class Config:
        orm_mode = True


# 社区帖子模型
class CommunityPostBase(BaseModel):
    title: str
    content: str
    author: str
    publish_date: str
    likes: int = 0
    comments: int = 0
    username: str
    userAvatar: str
    timeAgo: str
    category: str
    images: List[str]


class CommunityPostCreate(CommunityPostBase):
    pass


class CommunityPost(CommunityPostBase):
    id: int

    class Config:
        orm_mode = True


# 认证相关
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31W",  # "secret"
        "disabled": False,
        "user_type": "user"
    },
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31W",  # "secret"
        "disabled": False,
        "user_type": "admin"
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="绿居 - 家庭园艺养护平台 API", description="提供植物养护知识和社区交流的API服务", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 认证函数
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return "ok"


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = {}
        # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception as e:
        raise e
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# 路由
@app.post("/api/auth/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# 植物相关API
@app.get("/api/plants/", response_model=List[Plant])
async def get_plants(type: Optional[PlantType] = None, limit: int = 10, offset: int = 0):
    filtered_plants = plants
    if type:
        filtered_plants = [plant for plant in plants if plant["type"] == type]
    return filtered_plants[offset:offset + limit]


@app.get("/api/plants/{plant_id}", response_model=Plant)
async def get_plant(plant_id: int):
    plant = next((plant for plant in plants if plant["id"] == plant_id), None)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


# 养护指南相关API
@app.get("/api/guides/", response_model=List[CareGuide])
async def get_care_guides(category: Optional[GuideCategory] = None, limit: int = 10, offset: int = 0):
    filtered_guides = care_guides
    if category:
        filtered_guides = [guide for guide in care_guides if guide["category"] == category]
    return filtered_guides[offset:offset + limit]


@app.get("/api/guides/{guide_id}", response_model=CareGuide)
async def get_care_guide(guide_id: int):
    guide = next((guide for guide in care_guides if guide["id"] == guide_id), None)
    if guide is None:
        raise HTTPException(status_code=404, detail="Care guide not found")
    return guide


# 常见问题相关API
@app.get("/api/problems/", response_model=List[Problem])
async def get_problems(category: Optional[ProblemCategory] = None, limit: int = 10, offset: int = 0):
    filtered_problems = problems
    if category:
        filtered_problems = [problem for problem in problems if problem["category"] == category]
    return filtered_problems[offset:offset + limit]


@app.get("/api/problems/{problem_id}", response_model=Problem)
async def get_problem(problem_id: int):
    problem = next((problem for problem in problems if problem["id"] == problem_id), None)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


# 社区相关API
@app.get("/api/posts/", response_model=List[CommunityPost])
async def get_community_posts(limit: int = 10, offset: int = 0):
    return community_posts[offset:offset + limit]


@app.get("/api/posts/{post_id}", response_model=CommunityPost)
async def get_community_post(post_id: int):
    post = next((post for post in community_posts if post["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/api/community/posts/", response_model=CommunityPost, dependencies=[Depends(get_current_active_user)])
async def create_community_post(post: CommunityPostCreate):
    new_post = post.dict()
    new_post["id"] = max([p["id"] for p in community_posts]) + 1 if community_posts else 1
    new_post["publish_date"] = datetime.now().strftime("%Y-%m-%d")
    community_posts.append(new_post)
    return new_post


@app.post("/api/community/posts/{post_id}/like", dependencies=[Depends(get_current_active_user)])
async def like_post(post_id: int):
    post = next((post for post in community_posts if post["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post["likes"] += 1
    return {"message": "Post liked successfully", "likes": post["likes"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
