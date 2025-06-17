import os
from fastapi import FastAPI, Depends, HTTPException, status, Header, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, database, auth
from routers import tasks
from fastapi import APIRouter

# Create database tables
print("Creating database tables...")
models.Base.metadata.create_all(bind=database.engine)
print("Database tables created successfully!")

app = FastAPI(title="Assistant-for-Rent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В проде лучше указать домен!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create auth router
auth_router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(f"🔥 Registration attempt received")
    print(f"📋 User data: name='{user.name}', phone='{user.phone}', password length={len(user.password)}")
    try:
        print("✅ Starting registration process...")
        
        # Check if phone already exists
        existing_user = db.query(models.User).filter(models.User.phone == user.phone).first()
        if existing_user:
            print(f"❌ Phone {user.phone} already exists")
            raise HTTPException(status_code=400, detail="Phone already registered")
        
        print("✅ Phone is available, hashing password...")
        # Hash password and create user
        hashed = auth.get_password_hash(user.password)
        
        print("✅ Creating user object...")
        db_user = models.User(phone=user.phone, password_hash=hashed, name=user.name)
        
        print("✅ Adding to database...")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        print(f"✅ Registration successful! User ID: {db_user.id}")
        return db_user

    except HTTPException:
        print("❌ HTTP Exception raised")
        raise
    except Exception as e:
        print(f"💥 Registration error: {e}")
        print(f"💥 Error type: {type(e)}")
        import traceback
        print(f"💥 Traceback: {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@auth_router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    print(f"🔑 Login attempt: {user.phone}")
    db_user = db.query(models.User).filter(models.User.phone == user.phone).first()
    if not db_user or not auth.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect phone or password")
    token = auth.create_access_token({"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}

@auth_router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# Include routers
app.include_router(auth_router)
app.include_router(tasks.router)

# Mount static files
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Serve the HTML frontend
@app.get("/")
def read_root():
    print("🏠 Serving homepage")
    index_path = os.path.join(os.path.dirname(__file__), "frontend", "index.html")
    return FileResponse(index_path)

# Пример защищённого эндпоинта
@app.get("/protected")
def protected(current_user: models.User = Depends(auth.get_current_user)):
    return {"message": f"Hello, {current_user.name}!"}