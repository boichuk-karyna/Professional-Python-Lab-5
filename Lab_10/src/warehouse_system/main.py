import uvicorn
from warehouse_system.api import app

if __name__ == "__main__":
    uvicorn.run("warehouse_system.main:app", host="127.0.0.1", port=8000, reload=True)