from bitstring import BitArray


class HammingCoder:
    def __init__(self, data_bits_len, secded=False) -> None:
        self.secded = secded

        self._data_bits_num = data_bits_len
        self._parity_bits_num = 0

        self._evaluate_parity_bits_needed()

        self._block_len = (
            self._data_bits_num + self._parity_bits_num + 1
        )  # +1 for SECDED feature

        print(f"Data len: {data_bits_len}, redundant len: {self._parity_bits_num}\n")

    def _evaluate_parity_bits_needed(self):
        # (2^par ≥ data + par + 1)
        while 2**self._parity_bits_num < (
            self._data_bits_num + self._parity_bits_num + 1
        ):
            # Formatting the current state of the inequality
            print(f"Step: 2^{self._parity_bits_num} < {self._data_bits_num} + {self._parity_bits_num} + 1")

            self._parity_bits_num += 1
        
        print(f"Step: 2^{self._parity_bits_num} >= {self._data_bits_num} + {self._parity_bits_num} + 1\n")

    def _is_power_of_two(self, num):
        return (num - 1) & num == 0

    def _covered_data_bits_positions(self, parity_bit):
        for pos in range(3, self._block_len, 1):  # Start from '3' - the fist data pos
            # Get data bit with current parity bit turned on
            if not self._is_power_of_two(pos) and (pos & parity_bit):
                yield pos

    def encode_block(self, input_data: BitArray):
        print(f"Input data: {input_data.bin}\n")
        encoded = BitArray(self._block_len)

        # Fill in the data bits
        data_idx = 0
        for pos in range(1, self._block_len):
            if not self._is_power_of_two(pos):
                encoded[pos] = input_data[data_idx]
                data_idx += 1
        
        print(f"Data bits distributed {encoded.bin}, len with 0-pos parity {encoded.len} \n")

        # Fill in parity bits
        for power in range(self._parity_bits_num):
            # Get next 2^power
            parity_bit_pos = 1 << power

            xor_parity_res = 0  # Gives bit-value to achieve parity
            print(f"Checking parity for bit in pos {parity_bit_pos}\n")
            for data_pos in self._covered_data_bits_positions(parity_bit_pos):
                xor_parity_res ^= encoded[data_pos]
                print(f"Data at pos {data_pos} is under parity bit {parity_bit_pos}. Xor result: {xor_parity_res}")
            
            print(f"Final XOR res for parity bit {parity_bit_pos}: {xor_parity_res}. State of encoded str is {encoded.bin}")
            encoded[parity_bit_pos] = bool(xor_parity_res)
            print()

        # SECDED check
        if self.secded:
            total_parity = bool(encoded.count(True) % 2)
            encoded[0] = total_parity
            print(f"Total parity res {total_parity}\n")
            return encoded
        else:
            return encoded[1:]

    def decode_block(self, encoded: BitArray):
        encoded = (
            encoded if self.secded else (BitArray([0]) + encoded)
        )  # For easy indexing
        print(f"Inverted encoded block: {encoded[1:].bin}")


        width = self._parity_bits_num
        
        # Find error position
        xor_syndrome = 0
        for pos in range(1, len(encoded)):
            if encoded[pos] == True:
                xor_syndrome ^= pos
                print(f"Pos {pos:2} (1) -> New syndrome: {xor_syndrome:0{width}b} ({xor_syndrome})")

        print(f"Xor syndrome for decoding {xor_syndrome}, {xor_syndrome:0{width}b}-pos")

        overall_error = encoded.count(True) % 2

        
        if xor_syndrome != 0:
            if self.secded and not overall_error:
                print("SECDED: Double error detected")
                return None

            else:
                encoded.invert(xor_syndrome)
                print(f"HAMMING: Error found and corrected at position {xor_syndrome}")

        output_data = BitArray()
        for pos in range(1, self._block_len):
            if not self._is_power_of_two(pos):
                output_data.append([encoded[pos]])

        return output_data


if __name__ == "__main__":
    test = BitArray("0b11000111001100000110001110000110001110110001110011100")

    coder = HammingCoder(data_bits_len=len(test), secded=False)
    

    block_encoded = coder.encode_block(test)
    print(f"Original encoded block: {block_encoded.bin}")

    block_encoded.invert(37)
    # block_encoded.invert(7

    block_decoded = coder.decode_block(block_encoded)
    if block_decoded:
        print(f"Decoded block: {block_decoded.bin}")
