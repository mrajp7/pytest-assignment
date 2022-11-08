import logging
import re
import utils
from jsonschema import validate as validate_schema
from jsonschema import ValidationError, SchemaError
import collections
import json

ALLOWED_SPECIAL_CHARS = [' ', '.']
GENDERS = ['male', 'female']
WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
ORDER_SCHEMA_FILE = "order_json_schema.json"

def validate_int(orders:list, key:str):
    
    validated = True

    for order in orders:
        order = order['_source']
        order_id = order['order_id']
        logging.info(f"Validating Order - {order_id}")

        value = order[key]

        if not isinstance(value, int) or value < 0:
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{value}' is not an postive integer")
        
    return validated

def validate_non_empty_string(orders:list, key:str):
    
    validated = True

    for order in orders:
        order = order['_source']
        order_id = order['order_id']
        logging.info(f"Validating Order - {order_id}")

        value = order[key]

        if not isinstance(value, str):
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{value}' is not a valid string")
            continue

        value = value.strip()
        
        if len(value) == 0:
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{value}' is an empty string")
        if any(char.isdigit() for char in value):
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{value}' contains number")
        if any(not char.isalnum() and not char in ALLOWED_SPECIAL_CHARS for char in value):
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{value}' contains special characters")
        
    return validated

def validate_email_address(orders:list, key:str):

    validated = True
    # for validating an Email
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    for order in orders:
        order = order['_source']
        order_id = order['order_id']
        logging.info(f"Validating Order - {order['order_id']}")

        email = order[key]

        if not isinstance(email, str):
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{email}' is not in type string")
            continue

        if not re.match(pat,email):
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{email}' is not a valid email")

    return validated

def validate_phone_number(orders:list, key:str, allow_empty:bool=True):

    validated = True
    # for validating phone number
    pat = r'\+[0-9]+\s*?[0-9]{9,}'

    for order in orders:
        order = order['_source']
        order_id = order['order_id']
        logging.info(f"Validating Order - {order['order_id']}")

        phone = order[key]

        if not isinstance(phone, str):
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{phone}' is not in type string")
            continue
            
        if allow_empty and len(phone) == 0:
            continue
            
        if not re.match(pat,phone):
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{phone}' is not a valid phone number")

    return validated

def validate_gender(orders:list, key:str):

    validated = True

    for order in orders:
        order = order['_source']
        order_id = order['order_id']
        logging.info(f"Validating Order - {order_id}")

        value = order[key]

        if not isinstance(value, str):
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{value}' is not a valid string")
            continue

        value = value.strip().lower()
        
        if not value in GENDERS:
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{value}' is not one of {GENDERS}")

    return validated

def validate_date_time(orders:list, key:str):

    validated = True

    for order in orders:
        order = order['_source']
        order_id = order['order_id']
        logging.info(f"Validating Order - {order_id}")

        value = order[key]
        #2022-10-30T21:59:02+00:0
        # validate the date format
        date = utils.get_datetime_from_iso(value)
        
        if not date:
            validated = False
            logging.error(f"[{order_id}] [{key}] - '{value}' is not in ISO format")
    
    return validated

def validate_weekdays_value(orders:list, date_key:str, weekday_key:str, weekdayi_key:str):

    validated = True

    for order in orders:
        order = order['_source']
        order_id = order['order_id']
        logging.info(f"Validating Order - {order_id}")

        order_date = order[date_key]
        weekday = order[weekday_key] 
        weekday_i = order[weekdayi_key]

        date = utils.get_datetime_from_iso(order_date)
        if date:
            if not date.weekday() == weekday_i:
                validated = False
                logging.error(f"[{order_id}] [{weekdayi_key}] - '{weekday_i}' is not matching the order weekday int")
            if not weekday.lower() in WEEKDAYS and WEEKDAYS[date.weekday()] == weekday.lower():
                validated = False
                logging.error(f"[{order_id}] [{weekday_key}] - '{weekday}' is not matching the order weekday")

    return validated

def validate_order_json_schema(orders:list, key:str):

    validated = True
    order_schema = {}
    with open(ORDER_SCHEMA_FILE) as f:
        order_schema = json.load(f)

    for order in orders:
        order_id = order['_source']['order_id']
        logging.info(f"Validating Order - {order_id}")

        try:
            validate_schema(order,order_schema)
        except ValidationError as e:
            validated = False
            logging.error(f"[{order_id}] Product has validation error - '{e}'")
        except SchemaError as e:
            validated = False
            logging.error(f"[{order_id}] Product has schema error - '{e}'")

    return validated

def validate_order_details_against_product(orders:list):

    validated = True

    for order in orders:
        order = order['_source']
        order_id = order['order_id']
        logging.info(f"Validating Order - {order_id}")

        products = order['products']
        order_categories = order['category']
        order_manufacturer = order['manufacturer']
        order_sku = order['sku']
        product_categories = []
        product_manufacturer = []
        product_sku = []
        for product in products:
            if not product['category'] in product_categories:
                product_categories.append(product['category'])
            if not product['manufacturer'] in product_manufacturer:
                product_manufacturer.append(product['manufacturer'])
            if not product['sku'] in product_sku:
                product_sku.append(product['sku'])
        
        if collections.Counter(order_categories) != collections.Counter(product_categories):
            validated = False
            logging.error(f"[{order_id}] [{order_categories}] does not match the categories in products - '{product_categories}'")
        
        if collections.Counter(order_manufacturer) != collections.Counter(product_manufacturer):
            validated = False
            logging.error(f"[{order_id}] [{order_manufacturer}] does not match the categories in products - '{product_manufacturer}'")
        if collections.Counter(order_sku) != collections.Counter(product_sku):
            validated = False
            logging.error(f"[{order_id}] [{order_sku}] does not match the categories in products - '{product_sku}'")

    return validated
        

def validate_order_payment_details(orders:list):

    validated = True

    for order in orders:
        order = order['_source']
        order_id = order['order_id']
        logging.info(f"Validating Order - {order_id}")

        products = order['products']
        order_taxfull_price = order['taxful_total_price']
        order_taxless_price = order['taxless_total_price']
        order_quantity = order['total_quantity']
        order_products_count = order['total_unique_products']

        exp_taxfull_price = 0
        exp_taxless_price = 0
        exp_quantity = 0
        exp_prod_count = len(products)

        for product in products:
            exp_taxfull_price += product['taxful_price']
            exp_taxless_price += product['base_price'] - product['discount_amount']
            exp_quantity += product['quantity']

        if round(exp_taxfull_price,2) != order_taxfull_price:
            validated = False
            logging.error(f"[{order_id}] taxful_total_price [{order_taxfull_price}] added products - '{exp_taxfull_price}'")
        
        if round(exp_taxless_price,2) != order_taxless_price:
            validated = False
            logging.error(f"[{order_id}] taxless_total_price [{order_taxfull_price}] added products - '{exp_taxless_price}'")

        if exp_quantity != order_quantity:
            validated = False
            logging.error(f"[{order_id}] total_quantity [{order_quantity}] added products - '{exp_quantity}'")

        if exp_prod_count != order_products_count:
            validated = False
            logging.error(f"[{order_id}] total_unique_products [{order_quantity}] added products - '{exp_prod_count}'")
    
    return validated
        
        



