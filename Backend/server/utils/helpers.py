import json
import random
import re
import string
import importlib
from typing import Any
import base64
import inspect

from fastapi import Depends
from pydantic import BaseModel

from server.config import app_configs
from server.middlewares.exception_handler import ExcRaiser, ExcRaiser500


def is_valid_email(email: str) -> bool:
    """
    Checks if the provided string is a valid email address.
    
    Parameters:
        email (str): The string to check.
        
    Returns:
        bool: True if the string is a valid email, False otherwise.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))


def otp_generator() -> str:
    """
    Generates a 6-digit numeric OTP.
    """
    return ''.join(random.choices(string.digits, k=6))


def category_id_generator() -> str:
    """
    Generates a 6-digit numeric category ID.
    """
    get_db = importlib.import_module('server.config').get_db
    DBAdaptor = importlib.import_module('server.repositories').DBAdaptor
    prefix = 'CAT'
    db = get_db()
    db = next(db)
    cat_repo = DBAdaptor(db).category_repo
    prev_id = cat_repo.get_last_id()
    if not prev_id:
        return f'{prefix}001'
    num = int(prev_id[3:]) + 1
    return f'{prefix}{num:03}'


def sub_category_id_generator() -> str:
    """
    Generates a 6-digit numeric sub-category ID.
    """
    get_db = importlib.import_module('server.config').get_db
    DBAdaptor = importlib.import_module('server.repositories').DBAdaptor
    prefix = 'SUBCAT'
    db = get_db()
    db = next(db)
    sub_cat_repo = DBAdaptor(db).sub_category_repo
    prev_id = sub_cat_repo.get_last_id()
    if not prev_id:
        return f'{prefix}0001'
    num = int(prev_id[6:]) + 1
    return f'{prefix}{num:04}'


def paginator(page: int, item_per_page: int) -> int:
    """
    Paginates the query results.
    
    Parameters:
        page (int): The page number.
        item_per_page (int): The number of items per page.
        
    Returns:
        int: The offset value.
    """
    return (page - 1) * item_per_page if page > 1 else 0


def cache_obj_format(entity: BaseModel | list[BaseModel] | Any) -> str:
    """
    Returns the cache object format.
    """
    if isinstance(entity, list) and len(entity) == 0:
        return []
    if isinstance(entity, list):
        temp = []
        for ent in entity:
            if issubclass(type(ent), BaseModel):
                temp.append(ent.model_dump_json())
            else:
                temp.append(json.dumps(ent))
        return json.dumps(temp)
    elif isinstance(entity, BaseModel):
        return entity.model_dump_json()
    elif isinstance(entity, dict):
        return json.dumps(entity)
    elif isinstance(entity, str):
        return entity
    elif isinstance(entity, int):
        return str(entity)
    elif isinstance(entity, float):
        return str(entity)
    else:
        return json.dumps(entity)


def load_obj_from_cache(
    obj: str,
    model: BaseModel | None = None,
) -> BaseModel | dict:
    """
    Loads the object from cache.
    
    Parameters:
        obj (str | dict): The object to load.
        
    Returns:
        BaseModel | dict: The loaded object.
    """
    try:
        obj = json.loads(obj)
        if isinstance(obj, list):
            temp = []
            for ent in obj:
                if model:
                    temp.append(model.model_validate_json(ent))
                else:
                    temp.append(ent)
            return temp
        elif isinstance(obj, dict):
            if model:
                return model.model_validate_json(obj)
        else:
            return obj
    except Exception as e:
        raise TypeError(f"Invalid type: {type(obj)}")


def generate_referral_code(username: str) -> str:
    """
    Generates a random 10-character referral code.
    
    Returns:
        str: The generated referral code.
    """
    try:
        binary_data = username.encode('utf-8')
        base64_encoded = base64.b64encode(binary_data)
        ref_code = f'REF_{base64_encoded.decode("utf-8")}'
        return ref_code
    except ExcRaiser as e:
        raise
    except Exception as e:
        if app_configs.DEBUG:
            method_name = inspect.stack()[0].frame.f_code.co_name
            print(f'Unexpected error in {method_name}: {e}')
        raise ExcRaiser500(detail=str(e))


def decode_referral_code(ref_code: str) -> None:
    """
    Decodes the referral code to get the username."
    """
    try:
        decode_username = ref_code[4:]
        decoded = base64.b64decode(decode_username.encode('utf-8'))
        return decoded.decode('utf-8')
    except ExcRaiser as e:
        raise
    except Exception as e:
        if app_configs.DEBUG:
            method_name = inspect.stack()[0].frame.f_code.co_name
            print(f'Unexpected error in {method_name}: {e}')
        raise ExcRaiser500(detail=f'{str(e)}, Proceed to login')
