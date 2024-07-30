import re

from typing import Union, List

def have_re_code(text: Union[str, List[str]], code: str="P1OP1_F") -> bool:
    is_found = False
    if isinstance(text, list):
        for str_text in text:
            if code in str_text: is_found = True
    else:
        if code in text: is_found = True

    return is_found
