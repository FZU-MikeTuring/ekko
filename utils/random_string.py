#生成指定位数的字符串
import random
import string


def gen_random_string(length:int=7,character:bool=False) -> str:
    characters=string.digits #只数字
    if character:
        characters = characters + string.ascii_letters  # 大小写字母+数字
    return ''.join(random.choice(characters) for _ in range(length))