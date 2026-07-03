import logging


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def log_event(event: str, **fields: object) -> None:
    logging.getLogger("fieldpilot").info("%s | %s", event, fields)
