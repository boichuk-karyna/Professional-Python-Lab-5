from sqlalchemy.orm import Session

from warehouse_manager.repositories import WarehouseRepository


def test_create_and_get_product(db_session: Session):
    repo = WarehouseRepository(db_session)
    product = repo.create_product(
        code="PRD-001", name="Ноутбук", quantity=10, price=25000.0
    )

    assert product.id is not None
    assert product.code == "PRD-001"
    assert product.name == "Ноутбук"
    assert product.quantity == 10

    fetched = repo.get_product_by_id(product.id)
    assert fetched is not None
    assert fetched.code == "PRD-001"


def test_add_incoming_and_write_off(db_session: Session):
    repo = WarehouseRepository(db_session)
    product = repo.create_product(code="PRD-002", name="Мишка", quantity=5, price=500.0)

    # Надходження товару
    updated = repo.add_incoming(product.id, 10)
    assert updated.quantity == 15

    # Списання товару
    written_off = repo.write_off(product.id, 4)
    assert written_off is not None
    assert written_off.quantity == 11

    # Списання занадто великої кількості (надмірне списання)
    failed_write_off = repo.write_off(product.id, 20)
    assert failed_write_off is None
