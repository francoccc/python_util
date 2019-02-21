import re


def format_message(message, params):
    index = 0
    for param in params:
        message = re.sub('{[' + str(index) + ']}', str(param), message)
        index += 1
    return message

