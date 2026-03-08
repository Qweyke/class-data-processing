def get_gcd(a, b):
    while a != 0:
        b, a = a, b % a

    return b


def solve_extended_ea(a, b):
    # ax + by = a
    x_a, y_a = 1, 0
    # ax + by = b
    x_b, y_b = 0, 1

    while a != 0:
        x_a, y_a, x_b, y_b = x_b - (b // a) * x_a, y_b - (b // a) * y_a, x_a, y_a
        b, a = a, b % a

    return b, x_b, y_b


if __name__ == "__main__":
    print(solve_extended_ea(196, 180))
