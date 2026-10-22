from book_catalog.config import logger, settings

def main() -> None:
    logger.info(f"Starting {settings.app_name} in {settings.environment} mode.")

if __name__ == "__main__":
    main()
