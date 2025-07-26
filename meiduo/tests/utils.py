import random
import string
from functools import lru_cache


def generate_phone_number():
    # 第二位数字的可选范围
    second_digits = ['3', '4', '5', '7', '8', '9']
    # 随机选择第二位数字
    second_digit = random.choice(second_digits)
    # 随机生成后面的9位数字
    remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    # 组合成完整的手机号
    return f'1{second_digit}{remaining_digits}'


@lru_cache
def generate_username(length=8):
    # 定义可用字符：字母（大小写）、数字和下划线
    characters = string.ascii_letters + string.digits + '_'
    # 随机选择字符生成用户名
    return ''.join(random.choice(characters) for _ in range(length))


username = generate_username()
# print(username)
# print(username)

if __name__ == "__main__":
    # 生成一个随机手机号
    phone_number = generate_phone_number()
    print("随机生成的手机号：", phone_number)

    # 生成一个随机用户名
    username = generate_username()
    print("随机生成的用户名：", username)
