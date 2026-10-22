from typing import TypedDict

class ProductPayload(TypedDict):
    code: str
    name: str
    price: float
    currency: str
    supplier_id: int
    supplier_name: str
    supplier_email: str
