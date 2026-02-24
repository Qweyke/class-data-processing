import secrets


class PrimeNumberGenerator:
    def __init__(self, num_len=1024) -> None:
        self.num_len = num_len
        self._primes = self._sieve_of_eratosthenes()

    def _sieve_of_eratosthenes(self, limit=1000):
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

    def _generate_odd_bit_candidate(self):
        bit_num = secrets.randbits(self.num_len)
        # Make sure the MSB is 1
        bit_num |= 1 << (self.num_len - 1)
        # Make the number odd
        bit_num |= 1

        return bit_num

    def _is_prime_by_miller_rabin(self, candidate, check_iters=40):
        for i in range(check_iters):
            base = secrets.randbelow(candidate - 4) + 2

    def generate(self):
        while True:
            # 0. Generate odd candidate
            candidate = self._generate_odd_bit_candidate()

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
