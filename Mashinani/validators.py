from django.core.exceptions import ValidationError
import re

def validate_kenyan_id(value):
    if not re.match(r'^\d{7,8}$', str(value)):
        raise ValidationError(f'{value} is not a valid Kenyan ID number. It must be 7 or 8 digits long.')

def validate_kenyan_phone_number(value):
    value_str = str(value)
    if not re.match(r'^(?:\+254|0)?7\d{8}$', value_str):
        raise ValidationError(
            f'{value} is not a valid Kenyan phone number. It must be in the format 0798073204 or +254798073404.'
        )
