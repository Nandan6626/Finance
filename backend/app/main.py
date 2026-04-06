from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware.error_handler import add_error_handler_middleware
from app.modules.auth.routes import router as auth_router
from app.modules.users.routes import router as users_router
from app.modules.records.routes import router as records_router
from app.modules.dashboard.routes import router as dashboard_router
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend for Finance Dashboard System",
    version="1.0.0"
)
# Restrict CORS to explicit origins configured via environment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add custom Middlewares
add_error_handler_middleware(app)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(records_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"message": "Welcome to Finance Dashboard API"}
