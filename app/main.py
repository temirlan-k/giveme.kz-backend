from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from app.config.db import get_db,engine
from app.users.routers import router as user_router
from app.items.routers import router as items_router
from app.users.models import User
from app.items.models import Item,Category

app = FastAPI(title='GIVEme.kz',docs_url='/')

#admin 
# #TO-DO
admin = Admin(engine, title="Admin Panel")
admin.add_view(ModelView(User))
admin.add_view(ModelView(Item))
admin.add_view(ModelView(Category))
admin.mount_to(app)

#routers
app.include_router(router=user_router)
app.include_router(router=items_router)

#CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods='*',
    allow_headers='*',
)

#checkpoint
@app.get("/health", status_code=200, include_in_schema=False,tags='test')
def health_check(db=Depends(get_db)):
    """This is the health check endpoint"""
    return {"status": "ok"}
# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)