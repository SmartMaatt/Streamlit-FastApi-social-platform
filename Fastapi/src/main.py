from fastapi import FastAPI
from .routers import image_edit

app = FastAPI(title="Streamlit - FastAPI compatibility test")
app.include_router(image_edit.router)
