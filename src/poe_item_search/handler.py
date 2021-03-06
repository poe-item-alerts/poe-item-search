import logging
import time
import json
import os

from poe_item_search.search import search_items
from poe_item_search.filter import filter_items

logger = logging.getLogger(__name__)
if os.environ.get("LOG_LEVEL"):
    logger.setLevel(os.environ["LOG_LEVEL"])
else:
    logger.setLevel("INFO")


def handler(event, context):
    item_filter = event["filter"]
    logger.debug(
        f"Started event with {json.dumps(item_filter, indent=4)}"
    )
    start_time = time.perf_counter()
    items = search_items(item_filter)
    stop_time = time.perf_counter()
    duration = f"{stop_time - start_time:0.2f}"
    logger.info(f"Total execution time of search_items for {duration}s")
    filtered_items = filter_items(items, item_filter)
    return filtered_items

