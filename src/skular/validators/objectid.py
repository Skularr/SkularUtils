from re import match

from loguru import logger
from starlette.exceptions import HTTPException


def validate_oid(object_id: str):
    valid = validate_object_id(object_id)
    if valid:
        return valid

    logger.debug(f'Invalid object_id: {object_id}...')
    raise HTTPException(422, f"Provided id {object_id} is invalid...")


def validate_object_id(object_id: str):
    regex = r'^[0-9a-fA-F]{24}$'
    if match(regex, object_id):
        return True
    return False
