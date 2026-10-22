import os

def low_stock_threshold():
    raw = os.getenv('WAREHOUSE_LOW_STOCK', '5')
    try:
        threshold = int(raw)
    except ValueError as exc:
        raise ValueError('invalid threshold') from exc
    if threshold < 0:
        raise ValueError('invalid threshold')
    return threshold
