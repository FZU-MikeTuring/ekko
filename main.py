from fastapi import FastAPI
from routers import users, domain, channel, email
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handler import register_exception_handler
ekko = FastAPI()

register_exception_handler(ekko)

ekko.include_router(users.ekko)
ekko.include_router(domain.ekko)
ekko.include_router(channel.ekko)

ekko.include_router(email.ekko)


origins=[
    "*"
]
ekko.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    #允许的源
    allow_credentials=True,   #允许携带cookie
    allow_methods=["*"],      #允许的请求方法
    allow_headers=["*"],      #允许的请求头
)


