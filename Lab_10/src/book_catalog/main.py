import uvicorn
from book_catalog.api import app
from book_catalog.config import settings

def main() -> None:
    uvicorn.run("book_catalog.api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
