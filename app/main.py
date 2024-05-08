from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from app.config.db import get_db, engine
from app.config.settings import settings
from app.orders.models import Order
from app.users.routers import router as user_router
from app.items.routers import router as items_router
from app.orders.routers import router as order_router
from app.users.models import User, UserNeederDocuments
from app.items.models import Item, Category


app = FastAPI(title="GIVEme.kz", docs_url="/")

# admin
# #TO-DO
admin = Admin(engine, title="Admin Panel")
admin.add_view(ModelView(User))
admin.add_view(ModelView(Item))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(Order))
admin.add_view(ModelView(UserNeederDocuments))
admin.mount_to(app)

# routers
app.include_router(router=user_router)
app.include_router(router=items_router)
app.include_router(router=order_router)

# CORS
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
