import os

import uvicorn
from fastapi import FastAPI

import routes

os.popen("node index.js")

app = FastAPI()
app.include_router(routes.database.router)
app.include_router(routes.account.router)
app.include_router(routes.permission.router)

if __name__ == "__main__":
    uvicorn.run(app, port=10003)
