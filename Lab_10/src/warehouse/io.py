import csv
import json
from pathlib import Path
from .models import WarehouseItem, ImportRecordError

def read_items(path):
    """Stream rows without loading the whole CSV file."""
    with Path(path).open('r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not {'code','name','quantity','unit_price'} <= set(reader.fieldnames):
            raise ImportRecordError(1, 'header')
        for row_number, row in enumerate(reader, 2):
            try:
                quantity = int(row['quantity'])
            except (TypeError, ValueError) as exc:
                raise ImportRecordError(row_number, 'quantity') from exc
            try:
                price = float(row['unit_price'])
            except (TypeError, ValueError) as exc:
                raise ImportRecordError(row_number, 'unit_price') from exc
            try:
                yield WarehouseItem(row['code'], row['name'], quantity, price)
            except (ValueError, TypeError) as exc:
                raise ImportRecordError(row_number, 'item') from exc

def export_json(items, path):
    payload = [{'code': x.code, 'name': x.name, 'quantity': x.quantity, 'unit_price': x.unit_price, 'value': x.value} for x in items]
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
