from fastapi import FastAPI
from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from fastapi import Query
app=FastAPI(title="Day02:参数与校验")

#路劲参数
@app.get("/users/{user_id}")
def get_user_by_id(user_id:int):
    return{"user_id":user_id,"type":type(user_id).__name__}

#查询参数
@app.get("/users")
def list_users(page:int=1,size:int=10,keyword:str=""):
    return{
        "page":page,
        "size":size,
        "keyword":keyword,
        "说明":"这些是查询参数，通过url?key=value传递"
    }

#请求体 +pydantic 前端给后端
#继承BaseMODEL,拥有自动数据校验
class UserCreate(BaseModel):
    username: str = Field(...,min_length=3,max_length=20,description="用户名")
#EmialStr自动校验是否为合法邮箱
    email:EmailStr
    age:int=Field(...,ge=1,le=120,description="年龄")
    bio:Optional[str]=None

@app.post("/users")
def create_user(user:UserCreate):
    return{
        "message":"用户创建成功",
        #`.model_dump()` 作用：把 Pydantic 模型对象 → 转换成普通 Python 字典
        "user":user.model_dump()
    }

#pydantic 响应模型 后端给前端
class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    age:int
    bio:Optional[str]=None
#只要设置了 response_model，最终输出严格按照这个模型定义。
#凡是响应模型里面没有声明的字段，全部会被过滤，不会返回给前端。
@app.get("/users/{user_id}/profile",response_model=UserResponse)
def get_user_profile(user_id:int):
    fake_db_data={
        "id": user_id,
        "username": "张三",
        "email": "zhangsan@example.com",
        "age": 20,
        "bio": "计算机专业学生",
        "hashed_password": "fake_hash_123"  # 这个字段不应返回给前端
    }
    return fake_db_data

#查询参数不能用 Field(...)。Field 是给请求体（Pydantic模型）用的。
# 查询参数要用 Query(...)。
@app.get("/search")
def searchs( q:str=Query(...,min_length=1,description="搜索关键词"),
    category:str=Query("all",description="分类"),
    limit:int=Query(20,ge=1,le=100)):
    return{"query":q,"category":category,"limit":limit}

class loginer(BaseModel):
    username:str=Field(...,min_length=3)
    password:str=Field(...,min_length=6)
@app.post("/login")
def logining(user:loginer):
    return{
        "message":"登录成功",
        "username":user.username
    }

@app.get("/users/{user_id}/posts/{post_id}")
def multiply(user_id:int,post_id:int):
    return {"result":user_id*post_id}