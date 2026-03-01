import secrets

from binary_exp import mod_bin_exp


class PrimeNumberGenerator:
    def __init__(self, num_len=1024) -> None:
        self.num_len = num_len
        self._primes = self._generate_primes_by_sieve_of_eratosthenes()

    def _generate_primes_by_sieve_of_eratosthenes(self, limit=1000):
        prime_nums = []
        raw_nums = [True] * (limit + 1)  # +1 for iterating from idx = 2
        sqrt_limit = int(
            limit**0.5
        )  # truncate to achieve one of the factors <= sqrt(limit)

        for num in range(2, limit + 1):
            if raw_nums[num]:
                # Get the prime number for output list
                prime_nums.append(num)

                # If all possible composites marked- continue filling the prime list
                if num > sqrt_limit:
                    continue

                # Strike out composites for current prime
                for comp_num in range(num**2, limit + 1, num):
                    raw_nums[comp_num] = False

        return prime_nums

    def _is_prime_by_miller_rabin(self, odd_n, check_iters=40):
        def factorize_by_powers_of_two(even_num):
            d = even_num
            s = 0
            # Check if candidate num can be divided by 2
            while not (d & 1):
                d >>= 1  # Factorize by 2
                s += 1

            # Return max power of 2 and remaining odd factor 'd'
            return s, d

        power_s, odd_d = factorize_by_powers_of_two(odd_n - 1)

        # Test n-candidate for primality
        for _ in range(check_iters):
            # Get random 'a-base from [2, n - 2]
            a_base = secrets.randbelow(odd_n - 4) + 2

            # Check odd start-number-'d'
            mod_res = mod_bin_exp(a_base, odd_d, odd_n)
            if mod_res == 1 or mod_res == odd_n - 1:
                # 'n'-candidate passed check, all the other mod results will be = 1
                continue

            # Check for last power 's' is obsolete, if we didn't achieve mod_res == n - 1, then
            # next mod_res isn't 1, so Ferma Little theorem doesn't hold
            entry_found = False
            for _ in range(power_s - 1):
                mod_res = mod_bin_exp(mod_res, 2, odd_n)
                if mod_res == odd_n - 1:
                    entry_found = True
                    break

            if not entry_found:
                return False

        return True

    def generate(self):
        def generate_odd_bit_candidate():
            bit_num = secrets.randbits(self.num_len)
            # Make sure the MSB is 1
            bit_num |= 1 << (self.num_len - 1)
            # Make the number odd
            bit_num |= 1
            return bit_num

        while True:
            # 0. Generate odd candidate
            candidate = generate_odd_bit_candidate()

            # 1. Light check by small primes
            passed_small_prime_check = True
            for small_prime in self._primes:
                if candidate % small_prime == 0:
                    passed_small_prime_check = False
                    break

            if not passed_small_prime_check:
                continue

            # 2. Heavy check by Miller-Rabin
            if self._is_prime_by_miller_rabin(candidate):
                return candidate
