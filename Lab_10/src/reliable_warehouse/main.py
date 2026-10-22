import logging
from pathlib import Path
from reliable_warehouse.config import load_config
from reliable_warehouse.exceptions import ApplicationError
from reliable_warehouse.exporters import export_items_json
from reliable_warehouse.logging_config import configure_logging
from reliable_warehouse.services import ImportStatistics, process_warehouse_items
from reliable_warehouse.utils import logged_operation

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        config = load_config(Path("config.yaml"))
        configure_logging(config.logging.level, config.logging.path)

        statistics = ImportStatistics()

        with logged_operation("Warehouse data import/export"):
            items = process_warehouse_items(
                config.input_path,
                skip_invalid=config.processing.skip_invalid,
                low_stock_threshold=config.processing.low_stock_threshold,
                statistics=statistics,
            )
            exported = export_items_json(items, config.output_path)

        logger.info(
            "Total = %s, valid = %s, invalid = %s, low_stock_warnings = %s, exported = %s",
            statistics.total,
            statistics.valid,
            statistics.invalid,
            statistics.low_stock_count,
            exported,
        )
    except ApplicationError as error:
        logger.error("Application error: %s", error)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()