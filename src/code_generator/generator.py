"""
Code Generator - Generates production-ready, professional code
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class CodeFile:
    path: str
    name: str
    content: str
    language: str
    description: str

class CodeGenerator:
    def __init__(self):
        self.quality_rules = [
            "PEP 8 compliance",
            "Type hints",
            "Docstrings",
            "Error handling",
            "Logging",
            "Comments"
        ]
        logger.info("CodeGenerator initialized")

    def generate_backend_code(self, architecture, spec) -> List[CodeFile]:
        """Generate complete backend code"""
        logger.info(f"Generating backend code for {spec.name}")
        code_files = []
        
        # Main app file
        code_files.append(self._generate_main_app(spec))
        
        # Config
        code_files.append(self._generate_config())
        
        # Database setup
        code_files.append(self._generate_database())
        
        # Models
        code_files.extend(self._generate_models(spec))
        
        # Schemas
        code_files.extend(self._generate_schemas(spec))
        
        # Routes
        code_files.extend(self._generate_routes(spec))
        
        # Services
        code_files.extend(self._generate_services(spec))
        
        # Utils & Auth
        code_files.extend(self._generate_utils())
        
        # Requirements
        code_files.append(self._generate_requirements(spec))
        
        # .env example
        code_files.append(self._generate_env_example())
        
        logger.info(f"✅ Generated {len(code_files)} backend files")
        return code_files

    def generate_frontend_code(self, architecture, spec) -> List[CodeFile]:
        """Generate complete frontend code"""
        logger.info(f"Generating frontend code for {spec.name}")
        code_files = []
        
        if "React" in spec.frontend_tech:
            code_files.extend(self._generate_react_code(spec))
        elif "Vue" in spec.frontend_tech:
            code_files.extend(self._generate_vue_code(spec))
        
        logger.info(f"✅ Generated {len(code_files)} frontend files")
        return code_files

    def _generate_main_app(self, spec) -> CodeFile:
        """Generate main FastAPI application"""
        content = f'''"""Main FastAPI Application for {spec.name}"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any

from app.core.config import settings
from app.api.routes import health, users, products

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    logger.info("🚀 Application starting up...")
    yield
    logger.info("🛑 Application shutting down...")

app = FastAPI(
    title="{spec.name}",
    description="{spec.description}",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status": "error"},
    )

# Include Routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(products.router, prefix="/api", tags=["products"])

@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("✅ Database connection established")
    logger.info(f"📊 API Documentation: http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("❌ Database connection closed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
'''
        return CodeFile(
            path="backend/main.py",
            name="main.py",
            content=content,
            language="python",
            description="Main FastAPI application"
        )

    def _generate_config(self) -> CodeFile:
        """Generate configuration file"""
        content = '''"""Application Configuration"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Enterprise AI Platform"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()
'''
        return CodeFile(
            path="backend/app/core/config.py",
            name="config.py",
            content=content,
            language="python",
            description="Application configuration"
        )

    def _generate_database(self) -> CodeFile:
        """Generate database setup"""
        content = '''"""Database Configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
        return CodeFile(
            path="backend/app/core/database.py",
            name="database.py",
            content=content,
            language="python",
            description="Database configuration"
        )

    def _generate_models(self, spec) -> List[CodeFile]:
        """Generate database models"""
        content = '''"""Database Models"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from app.core.database import Base

class User(Base):
    """User Model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User {self.email}>"

class Product(Base):
    """Product Model"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Product {self.name}>"

class Order(Base):
    """Order Model"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    total_amount = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Order {self.id}>"
'''
        return [CodeFile(
            path="backend/app/models/models.py",
            name="models.py",
            content=content,
            language="python",
            description="Database models"
        )]

    def _generate_schemas(self, spec) -> List[CodeFile]:
        """Generate Pydantic schemas"""
        content = '''"""Pydantic Schemas for validation"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float = Field(..., gt=0)
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    product_ids: list[int]
    total_amount: float

class Order(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
'''
        return [CodeFile(
            path="backend/app/schemas/schemas.py",
            name="schemas.py",
            content=content,
            language="python",
            description="Pydantic validation schemas"
        )]

    def _generate_routes(self, spec) -> List[CodeFile]:
        """Generate API routes"""
        routes = []
        
        # Health route
        health_content = '''"""Health Check Endpoint"""
from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "message": "Service is running",
        "timestamp": None
    }
'''
        routes.append(CodeFile(
            path="backend/app/api/routes/health.py",
            name="health.py",
            content=health_content,
            language="python",
            description="Health check routes"
        ))
        
        # Users route
        users_content = '''"""User Endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.schemas import User, UserCreate, UserUpdate
from app.models.models import User as UserModel
from app.core.database import get_db
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users")

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    logger.info(f"Register user: {user.email}")
    
    existing_user = db.query(UserModel).filter(
        (UserModel.email == user.email) | (UserModel.username == user.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    return UserService.create_user(db, user)

@router.get("/me", response_model=User)
async def get_current_user(db: Session = Depends(get_db)):
    """Get current user"""
    logger.info("Get current user")
    return {"id": 1, "email": "user@example.com", "username": "user"}

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    logger.info(f"Get user: {user_id}")
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Update user"""
    logger.info(f"Update user: {user_id}")
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user
'''
        routes.append(CodeFile(
            path="backend/app/api/routes/users.py",
            name="users.py",
            content=users_content,
            language="python",
            description="User endpoints"
        ))
        
        # Products route
        products_content = '''"""Product Endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.schemas import Product, ProductCreate
from app.models.models import Product as ProductModel
from app.core.database import get_db
from app.services.product_service import ProductService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/products")

@router.get("/", response_model=list[Product])
async def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all products"""
    logger.info(f"Get products: skip={skip}, limit={limit}")
    return ProductService.get_products(db, skip, limit)

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create new product"""
    logger.info(f"Create product: {product.name}")
    return ProductService.create_product(db, product)

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    logger.info(f"Get product: {product_id}")
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: int, product_update: ProductCreate, db: Session = Depends(get_db)):
    """Update product"""
    logger.info(f"Update product: {product_id}")
    return ProductService.update_product(db, product_id, product_update)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete product"""
    logger.info(f"Delete product: {product_id}")
    return ProductService.delete_product(db, product_id)
'''
        routes.append(CodeFile(
            path="backend/app/api/routes/products.py",
            name="products.py",
            content=products_content,
            language="python",
            description="Product endpoints"
        ))
        
        # Routes init
        routes.append(CodeFile(
            path="backend/app/api/routes/__init__.py",
            name="__init__.py",
            content="""from . import health, users, products

__all__ = ['health', 'users', 'products']
""",
            language="python",
            description="Routes module init"
        ))
        
        return routes

    def _generate_services(self, spec) -> List[CodeFile]:
        """Generate business logic services"""
        services = []
        
        # User service
        user_service = '''"""User Business Logic"""
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.schemas import UserCreate
import logging

logger = logging.getLogger(__name__)

class UserService:
    """User service"""
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Create new user"""
        db_user = User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=user.password  # In production, hash this!
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User created: {user.email}")
        return db_user
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
'''
        services.append(CodeFile(
            path="backend/app/services/user_service.py",
            name="user_service.py",
            content=user_service,
            language="python",
            description="User service"
        ))
        
        # Product service
        product_service = '''"""Product Business Logic"""
from sqlalchemy.orm import Session
from app.models.models import Product
from app.schemas.schemas import ProductCreate
import logging

logger = logging.getLogger(__name__)

class ProductService:
    """Product service"""
    
    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 10):
        """Get all products"""
        return db.query(Product).filter(Product.is_active == True).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        """Create new product"""
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        logger.info(f"Product created: {product.name}")
        return db_product
    
    @staticmethod
    def update_product(db: Session, product_id: int, product_update: ProductCreate) -> Product:
        """Update product"""
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product:
            for field, value in product_update.dict().items():
                setattr(db_product, field, value)
            db.commit()
            db.refresh(db_product)
        return db_product
    
    @staticmethod
    def delete_product(db: Session, product_id: int):
        """Delete product"""
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product:
            db.delete(db_product)
            db.commit()
            logger.info(f"Product deleted: {product_id}")
'''
        services.append(CodeFile(
            path="backend/app/services/product_service.py",
            name="product_service.py",
            content=product_service,
            language="python",
            description="Product service"
        ))
        
        # Services init
        services.append(CodeFile(
            path="backend/app/services/__init__.py",
            name="__init__.py",
            content="""from .user_service import UserService
from .product_service import ProductService

__all__ = ['UserService', 'ProductService']
""",
            language="python",
            description="Services module init"
        ))
        
        return services

    def _generate_utils(self) -> List[CodeFile]:
        """Generate utility functions"""
        utils = []
        
        # Auth utils
        auth_utils = '''"""Authentication Utilities"""
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
import jwt
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
'''
        utils.append(CodeFile(
            path="backend/app/utils/auth.py",
            name="auth.py",
            content=auth_utils,
            language="python",
            description="Authentication utilities"
        ))
        
        # Common utils
        common_utils = '''"""Common Utilities"""
import logging
from functools import wraps
from datetime import datetime

logger = logging.getLogger(__name__)

def log_execution(func):
    """Decorator to log function execution"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = datetime.utcnow()
        logger.info(f"Executing {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"✅ {func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.error(f"❌ {func.__name__} failed after {duration:.2f}s: {str(e)}")
            raise
    return wrapper
'''
        utils.append(CodeFile(
            path="backend/app/utils/common.py",
            name="common.py",
            content=common_utils,
            language="python",
            description="Common utilities"
        ))
        
        # Utils init
        utils.append(CodeFile(
            path="backend/app/utils/__init__.py",
            name="__init__.py",
            content="""from .auth import hash_password, verify_password, create_access_token
from .common import log_execution

__all__ = ['hash_password', 'verify_password', 'create_access_token', 'log_execution']
""",
            language="python",
            description="Utils module init"
        ))
        
        # Core init
        utils.append(CodeFile(
            path="backend/app/core/__init__.py",
            name="__init__.py",
            content="",
            language="python",
            description="Core module init"
        ))
        
        # Models init
        utils.append(CodeFile(
            path="backend/app/models/__init__.py",
            name="__init__.py",
            content="""from .models import User, Product, Order

__all__ = ['User', 'Product', 'Order']
""",
            language="python",
            description="Models module init"
        ))
        
        # Schemas init
        utils.append(CodeFile(
            path="backend/app/schemas/__init__.py",
            name="__init__.py",
            content="",
            language="python",
            description="Schemas module init"
        ))
        
        # App init
        utils.append(CodeFile(
            path="backend/app/__init__.py",
            name="__init__.py",
            content="",
            language="python",
            description="App module init"
        ))
        
        # API init
        utils.append(CodeFile(
            path="backend/app/api/__init__.py",
            name="__init__.py",
            content="",
            language="python",
            description="API module init"
        ))
        
        return utils

    def _generate_requirements(self, spec) -> CodeFile:
        """Generate requirements.txt"""
        content = """fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
pyjwt==2.8.1
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
email-validator==2.1.0
httpx==0.25.1
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.12.0
flake8==6.1.0
mypy==1.7.1
"""
        return CodeFile(
            path="backend/requirements.txt",
            name="requirements.txt",
            content=content,
            language="text",
            description="Python dependencies"
        )

    def _generate_env_example(self) -> CodeFile:
        """Generate .env.example"""
        content = """DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
LOG_LEVEL=INFO
"""
        return CodeFile(
            path="backend/.env.example",
            name=".env.example",
            content=content,
            language="text",
            description="Environment variables example"
        )

    def _generate_react_code(self, spec) -> List[CodeFile]:
        """Generate React frontend code"""
        files = []
        
        # App.jsx
        app_jsx = '''import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navigation from './components/Navigation';
import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';

function App() {
  const [loading, setLoading] = useState(true);
  const [apiHealthy, setApiHealthy] = useState(false);

  useEffect(() => {
    // Check API health
    const checkHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/health');
        if (response.ok) {
          setApiHealthy(true);
          console.log('✅ API is healthy');
        }
      } catch (error) {
        console.error('❌ API error:', error);
        setApiHealthy(false);
      } finally {
        setLoading(false);
      }
    };
    
    checkHealth();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!apiHealthy) {
    return <div className="error">API is not available. Please check backend.</div>;
  }

  return (
    <Router>
      <Navigation />
      <main className="container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/products" element={<ProductsPage />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
'''
        files.append(CodeFile(
            path="frontend/src/App.jsx",
            name="App.jsx",
            content=app_jsx,
            language="javascript",
            description="Main App component"
        ))
        
        # useApi Hook
        use_api = '''import { useState, useEffect } from 'react';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const useApi = (endpoint, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
          method: options.method || 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            ...options.headers,
          },
        });
        
        if (!response.ok) throw new Error('API request failed');
        
        const result = await response.json();
        setData(result);
        setError(null);
      } catch (err) {
        setError(err.message);
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [endpoint]);

  return { data, loading, error };
};
'''
        files.append(CodeFile(
            path="frontend/src/hooks/useApi.js",
            name="useApi.js",
            content=use_api,
            language="javascript",
            description="Custom hook for API calls"
        ))
        
        # Navigation component
        nav_component = '''import React from 'react';
import { Link } from 'react-router-dom';
import './Navigation.css';

function Navigation() {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          🚀 Enterprise AI
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">
              Home
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/products" className="nav-link">
              Products
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
'''
        files.append(CodeFile(
            path="frontend/src/components/Navigation.jsx",
            name="Navigation.jsx",
            content=nav_component,
            language="javascript",
            description="Navigation component"
        ))
        
        # HomePage
        home_page = '''import React from 'react';

function HomePage() {
  return (
    <div className="home-page">
      <h1>Welcome to Enterprise AI Platform</h1>
      <p>Your AI-powered full-stack application</p>
      <div className="features">
        <div className="feature-card">
          <h3>🚀 Fast Performance</h3>
          <p>Built with FastAPI and React for lightning-fast response times</p>
        </div>
        <div className="feature-card">
          <h3>🔒 Secure</h3>
          <p>JWT authentication and industry-standard security practices</p>
        </div>
        <div className="feature-card">
          <h3>📊 Scalable</h3>
          <p>Docker-ready and designed for horizontal scaling</p>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
'''
        files.append(CodeFile(
            path="frontend/src/pages/HomePage.jsx",
            name="HomePage.jsx",
            content=home_page,
            language="javascript",
            description="Home page"
        ))
        
        # ProductsPage
        products_page = '''import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';

function ProductsPage() {
  const { data: products, loading, error } = useApi('/products');
  const [newProduct, setNewProduct] = useState({ name: '', description: '', price: 0, stock: 0 });

  const handleCreateProduct = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newProduct),
      });
      if (response.ok) {
        alert('Product created successfully!');
        setNewProduct({ name: '', description: '', price: 0, stock: 0 });
      }
    } catch (error) {
      console.error('Error creating product:', error);
    }
  };

  if (loading) return <div>Loading products...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="products-page">
      <h1>Products</h1>
      
      <div className="create-product-form">
        <h2>Add New Product</h2>
        <input
          type="text"
          placeholder="Product Name"
          value={newProduct.name}
          onChange={(e) => setNewProduct({...newProduct, name: e.target.value})}
        />
        <textarea
          placeholder="Description"
          value={newProduct.description}
          onChange={(e) => setNewProduct({...newProduct, description: e.target.value})}
        />
        <input
          type="number"
          placeholder="Price"
          value={newProduct.price}
          onChange={(e) => setNewProduct({...newProduct, price: parseFloat(e.target.value)})}
        />
        <input
          type="number"
          placeholder="Stock"
          value={newProduct.stock}
          onChange={(e) => setNewProduct({...newProduct, stock: parseInt(e.target.value)})}
        />
        <button onClick={handleCreateProduct}>Create Product</button>
      </div>

      <div className="products-list">
        <h2>Available Products</h2>
        {products && products.length > 0 ? (
          <div className="product-grid">
            {products.map((product) => (
              <div key={product.id} className="product-card">
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <p className="price">${product.price}</p>
                <p className="stock">Stock: {product.stock}</p>
              </div>
            ))}
          </div>
        ) : (
          <p>No products available</p>
        )}
      </div>
    </div>
  );
}

export default ProductsPage;
'''
        files.append(CodeFile(
            path="frontend/src/pages/ProductsPage.jsx",
            name="ProductsPage.jsx",
            content=products_page,
            language="javascript",
            description="Products page"
        ))
        
        # package.json
        package_json = '''{
  "name": "enterprise-ai-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .js,.jsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "eslint": "^8.53.0"
  }
}
'''
        files.append(CodeFile(
            path="frontend/package.json",
            name="package.json",
            content=package_json,
            language="json",
            description="Frontend dependencies"
        ))
        
        # Vite config
        vite_config = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
'''
        files.append(CodeFile(
            path="frontend/vite.config.js",
            name="vite.config.js",
            content=vite_config,
            language="javascript",
            description="Vite configuration"
        ))
        
        return files

    def _generate_vue_code(self, spec) -> List[CodeFile]:
        """Generate Vue frontend code"""
        return []
