import time
import logging
import json
from datetime import datetime, timedelta

import boto3
import requests


logger = logging.getLogger("item_search")
logger.setLevel(logging.DEBUG)


def search_items(item_filter):
    search_fields = {
        "base": ["character_name", "account_name", "id", "typeLine"],
        "mod": ["craftedMods", "explicitMods"],
        "type": ["inventoryId"],
        "links": ["links"],
        "unique": ["name", "flavourText"]
    }
    
    request_fields = search_fields["base"]
    for f_type in item_filter.keys():
        tmp = search_fields[f_type]
        request_fields += tmp
    start_time = time.perf_counter()
    items = request_items(request_fields)
    stop_time = time.perf_counter()
    duration = f"{stop_time - start_time:0.2f}"
    logger.info(f"Total time in request item for {duration}s")
    return items


def request_items(request_fields):
    client = boto3.client("appsync")
    for api in client.list_graphql_apis()["graphqlApis"]:
        if api["name"] == "poe_ladder_export":
            api_uri = api["uris"]["GRAPHQL"]
            api_id = api["apiId"]
    if not api_id:
        logging.critical("No api id detected aborting!")
        return {"error": {"code": 1, "message": "No api id detected!"}}
    key_timeout = datetime.today() + timedelta(days=2)
    api_key = client.create_api_key(
        apiId=api_id,
        description="API key for the current filter run",
        expires=int(key_timeout.timestamp())
    )["apiKey"]["id"]
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/graphql"
    }
    
    query_start_time = time.perf_counter()
    query = "query{listItems(limit:1000){items{%s}nextToken}}" % " ".join(request_fields)
    result = []
    while True:
        items = requests.post(
            api_uri,
            headers=headers,
            json={"query": query}
        ).json()
        next_token = items["data"]["listItems"]["nextToken"]
        result += items["data"]["listItems"]["items"]
        query = 'query{listItems(limit:1000,nextToken: "%s"){items{%s}nextToken}}' % (next_token, " ".join(request_fields))
        if not next_token:
            break
    query_stop_time = time.perf_counter()
    query_duration = f"{query_stop_time - query_start_time:0.2f}"
    logger.debug(f"Total query time {query_duration}s")
    client.delete_api_key(apiId=api_id, id=api_key)
    return result
    
