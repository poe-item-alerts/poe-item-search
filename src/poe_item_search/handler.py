import logging
import time
import json

import boto3
import requests

from search import search_items
from filter import filter_items

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

    print(json.dumps(filtered_items, indent=4))

    # assemble result
    # return

if __name__ == "__main__":
    test_event = {"filter": {"type": "quicksilver Flask of Adrenaline"}}
    handler(test_event, None)
