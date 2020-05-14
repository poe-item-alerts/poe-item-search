import logging
import time
import json

from poe_item_search.search import search_items
from poe_item_search.filter import filter_items

logger = logging.getLogger("item_search")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)


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

