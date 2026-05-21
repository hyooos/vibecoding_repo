def add(a, b):
    """두 수를 더한다."""
    return a + b


def subtract(a, b):
    """두 수를 뺀다."""
    return a - b


def multiply(a, b):
    """두 수를 곱한다."""
    return a * b


def divide(a, b):
    """두 수를 나눈다."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b