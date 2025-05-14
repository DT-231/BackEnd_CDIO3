import os
from app import app
import uvicorn

if __name__ == "__main__":
    os.system("cls")
    uvicorn.run(app, host="0.0.0.0", port=8000)