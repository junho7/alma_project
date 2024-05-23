from fastapi import FastAPI
from app.routers import users, leads

app = FastAPI()

app.include_router(users.router)
app.include_router(leads.router)
