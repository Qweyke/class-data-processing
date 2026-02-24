def bin_exp(base, power):
    res = 1
    while power > 0:
        if power & 1:
            res *= base
        base *= base
        power >>= 1

    return res


if __name__ == "__main__":
    print(bin_exp(24, 3))
