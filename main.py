from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db, create_tables, User
from typing import List
import uvicorn

# ایجاد اپلیکیشن FastAPI
app = FastAPI()

# تنظیم فولدر استاتیک و تمپلیت‌ها
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ایجاد جداول در شروع برنامه
create_tables()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    # دریافت همه کاربران
    users = db.query(User).all()
    # تهیه عناوین جدول
    titles = ["شناسه", "نام", "ایمیل", "سن"]
    # تبدیل کاربران به لیست برای نمایش
    data = [[user.id, user.name, user.email, user.age] for user in users]
    return templates.TemplateResponse(
        "front.html",
        {"request": request, "titles": titles, "data": data}
    )

@app.post("/insert")
async def create_user(
    name: str = Form(...),
    email: str = Form(...),
    age: int = Form(...)
):
    db = next(get_db())
    try:
        # ایجاد کاربر جدید
        new_user = User(name=name, email=email, age=age)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.get("/delete/{user_id}")
async def delete_user(user_id: int):
    db = next(get_db())
    try:
        # حذف کاربر
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.get("/edit/{user_id}")
async def edit_user_form(request: Request, user_id: int, db: Session = Depends(get_db)):
    # دریافت اطلاعات کاربر برای ویرایش
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "user": user}
    )

@app.post("/edit/{user_id}")
async def update_user(
    user_id: int,
    name: str = Form(...),
    email: str = Form(...),
    age: int = Form(...)
):
    db = next(get_db())
    try:
        # به‌روزرسانی اطلاعات کاربر
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.name = name
            user.email = email
            user.age = age
            db.commit()
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 