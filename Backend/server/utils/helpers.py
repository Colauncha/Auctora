import random
import re
import string
import importlib

from fastapi import Depends


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