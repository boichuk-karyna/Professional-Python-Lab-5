import pytest
from sqlalchemy.orm import Session

from warehouse_manager.repositories import WarehouseRepository
from warehouse_manager.services import WarehouseService


def test_service_register_incoming(db_session: Session):
    repo = WarehouseRepository(db_session)
    product = repo.create_product(
        code="PRD-003", name="Монітор", quantity=2, price=7000.0
    )

    service = WarehouseService(db_session)
    updated = service.register_incoming(product.id, 3)
    assert updated.quantity == 5


def test_service_invalid_incoming_amount(db_session: Session):
    repo = WarehouseRepository(db_session)
    product = repo.create_product(
        code="PRD-004", name="Клавіатура", quantity=5, price=1500.0
    )

    service = WarehouseService(db_session)
    with pytest.raises(
        ValueError, match="Кількість для надходження має бути більше нуля"
    ):
        service.register_incoming(product.id, 0)


def test_service_excessive_write_off(db_session: Session):
    repo = WarehouseRepository(db_session)
    product = repo.create_product(
        code="PRD-005", name="Навушники", quantity=2, price=2000.0
    )

    service = WarehouseService(db_session)
    with pytest.raises(
        ValueError, match="Товар не знайдено або недостатньо коштів/запасів"
    ):
        service.register_write_off(product.id, 10)
