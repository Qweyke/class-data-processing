from euclidean import get_gcd, solve_extended_ea
from binary_exp import mod_bin_exp
from prime_generator import PrimeNumberGenerator


def generate_key_pair(key_size=2048, pub_exponent=65537):
    half_size = key_size // 2
    p = PrimeNumberGenerator(half_size).generate()
    q = PrimeNumberGenerator(half_size).generate()
    n = p * q

    e = pub_exponent
    # Euler's totient func for primes
    phi_n = (p - 1) * (q - 1)

    # Check for coprimality
    if get_gcd(e, phi_n) != 1:
        raise ValueError("e and phi(n) are not coprime!")

    # Euclidean theorem  M^phi(n) ≡ 1 (mod n) == [e * d + phi(n) * k = 1]
    _, d, _ = solve_extended_ea(e, phi_n)
    if d < 0:
        d = d % phi_n

    return n, e, d


def encrypt(m: int, e, n):
    return mod_bin_exp(m, e, n)


def decrypt(cipher: int, d, n):
    return mod_bin_exp(cipher, d, n)


if __name__ == "__main__":
    n, e, d = generate_key_pair()
    print(f"Public key:  e={e}\n")
    print(f"Private key: d={d}\n\n")

    message = 123
    encoded = encrypt(m=message, e=e, n=n)
    decoded = decrypt(cipher=encoded, d=d, n=n)
    print(decoded)
