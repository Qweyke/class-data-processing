import matplotlib.pyplot as plt


def gcd_by_euclid(a, b):
    while a != 0:
        b, a = a, b % a

    return b


def is_prime(n):
    """Check prime"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def count_primes_by_dirichlet(a, b, limit_k):
    if gcd_by_euclid(a, b) != 1:
        print("a and b are not coprime")
        return None, None

    primes_for_k = []
    total_found = 0
    for k in range(limit_k):
        number = a * k + b
        if is_prime(number):
            total_found += 1
        primes_for_k.append(total_found)
    return primes_for_k, total_found


a, b, limit = 27, 7, 20000
res, total_found = count_primes_by_dirichlet(a=a, b=b, limit_k=limit)
if res:
    # Отрисовка
    plt.figure(figsize=(10, 6))
    plt.plot(res, label=f"Progression {a}k + {b}; ", color="blue")

    plt.title(f"Primes accumulation (Dirichlet). Total: {total_found}")
    plt.xlabel("k-value (iteration)")
    plt.ylabel("Primes count")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()
