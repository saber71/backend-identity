import os

import uvicorn
from fastapi import FastAPI

import routes.database

os.popen("node index.js")

app = FastAPI()
app.include_router(routes.database.router)

if __name__ == "__main__":
    uvicorn.run(app, port=10003)
