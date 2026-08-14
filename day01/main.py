from fastapi import FastAPI
from datetime import datetime

app=FastAPI(title="我的第一个FastAPI应用")

@app.get("/hello/{name}")
def read_root(name):
    return {"message":f"hello,{name}","time":datetime.now().isoformat()}

@app.get("/time")
def current_time():
    return{datetime.now().year}

@app.get("/add/{a}/{b}")
def added(a:int,b:int):
    return{"result":a+b}