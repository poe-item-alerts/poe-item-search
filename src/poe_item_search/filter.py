import logging
import os


logger = logging.getLogger(__name__)
if os.environ.get("LOG_LEVEL"):
    logger.setLevel(os.environ["LOG_LEVEL"])
else:
    logger.setLevel("INFO")


def filter_items(items, filter):
    logger.debug(f"Started execution of filter_items with {len(items)} items.")
    filtered_items = []

    for item in items:
        acc = item["account_name"]
        result = []
        mods = []
        links = None
        unique = None
        for filter_type, filter_value in filter.items():
            if filter_type == "type":
                filter_result = type_filter(item, filter_value)
                result.append(filter_result)
            elif filter_type == "mod":
                filter_result, mod = mod_filter(item, filter_value)
                mods.append(mod)
                result.append(filter_result)
            elif filter_type == "links":
                filter_result, links = link_filter(item, filter_value)
                result.append(filter_result)
            elif filter_type == "unique":
                filter_result, unique = unique_filter(item, filter_value)
                result.append(filter_result)
            elif filter_type == "class":
                filter_result = class_filter(item, filter_value)
                result.append(filter_result)
        if result:
            # all will make empty lists True
            if all(result):
                logger.debug(f"All filters matched!")
                # Still not sure how to make this logic better :/
                if links and mods:
                    logger.debug(f"Link and mod filters matched!")
                    mods_string = ", ".join(mods)
                    item_line = f"{item['typeLine']}({links}L)[{mods_string}]"
                    filtered_items.append(
                        {
                            "account_name": acc,
                            "item": item_line,
                            "created": item["created"],
                            "inventory_id": item["inventoryId"]
                        }
                    )
                elif mods:
                    logger.debug(f"Mod filter matched!")
                    mods_string = ", ".join(mods)
                    item_line = f"{item['typeLine']}[{mods_string}]"
                    filtered_items.append(
                        {
                            "account_name": acc,
                            "item": item_line,
                            "created": item["created"],
                            "inventory_id": item["inventoryId"]
                        }
                    )
                elif links:
                    logger.debug(f"Link filter matched!")
                    item_line = f"{item['typeLine']}({links}L)"
                    filtered_items.append(
                        {
                            "account_name": acc,
                            "item": item_line,
                            "created": item["created"],
                            "inventory_id": item["inventoryId"]
                        }
                    )
                elif unique:
                    logger.debug(f"Unique filter matched!")
                    item_line = f"{unique}"
                    filtered_items.append(
                        {
                            "account_name": acc,
                            "item": item_line,
                            "created": item["created"],
                            "inventory_id": item["inventoryId"]
                        }
                    )
                else:
                    logger.debug(f"Type filter matched!")
                    item_line = f"{item['typeLine']}"
                    filtered_items.append(
                        {
                            "account_name": acc,
                            "item": item_line,
                            "created": item["created"],
                            "inventory_id": item["inventoryId"]
                        }
                    )
    logger.debug(f"Finished function filter_items")
    return filtered_items
                

def type_filter(item, filter_value):
    logger.debug(f"Started type filter against {filter_value}")
    filter_value = filter_value.lower()
    type_line = item["typeLine"].lower()
    inventory_id = item["inventoryId"].lower()
    if filter_value in type_line or filter_value in inventory_id:
        return True
    return False

def mod_filter(item, filter_value):
    logger.debug(f"Started mod filter against {filter_value}")
    if item["explicitMods"] and item["craftedMods"]:
        mods = item["explicitMods"] + item["craftedMods"]
    elif item["explicitMods"]:
        mods = item["explicitMods"]
    elif item["craftedMods"]:
        mods = item["craftedMods"]
    else:
        mods = []
    for mod in mods:
        # logger.debug(f"Matching {mod} against {filter_value}")
        if filter_value.lower() in mod.lower():
            logger.debug(f"Mod matched!")
            return True, mod
    return False, None

def link_filter(item, filter_value):
    logger.debug(f"Started link filter against {filter_value}")
    if item["links"] >= int(filter_value):
        return True, item["links"]
    return False, None

def class_filter(item, filter_value):
    logger.debug(f"Started class filter against {filter_value}")
    if item["character_class"] == filter_value:
        return True
    return False

def unique_filter(item, filter_value):
    logger.debug(f"Started unique filter against {filter_value}")
    if filter_value == "any":
        # Tabula seems to be the odd ball without a flavour text
        if (item.get("flavourText")) or (item["name"] == "Tabula Rasa"):
            if "Talisman" in item["typeLine"]:
                return False, None
            return True, item["name"]
    else:
        if item["name"]:
            if item["name"].lower() == filter_value.lower():
                return True, item["name"]
    return False, None

