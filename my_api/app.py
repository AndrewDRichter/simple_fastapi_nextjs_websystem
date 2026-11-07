from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from my_api.routers import users, auth, brands, products, stock_lots

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(
    router=users.router,
    prefix='/api/v1/users',
    tags=['users']
)

app.include_router(
    router=auth.router,
    prefix='/api/v1/auth',
    tags=['auth']
)

app.include_router(
    router=brands.router,
    prefix='/api/v1/brands',
    tags=['brands']
)

app.include_router(
    router=products.router,
    prefix='/api/v1/products',
    tags=['products']
)

app.include_router(
    router=stock_lots.router,
    prefix='/api/v1/stock_lots',
    tags=['stock_lots']
)

@app.get(
    path='/',
    status_code=status.HTTP_200_OK
)
async def health():
    return {'ok': True}
