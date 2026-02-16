from bitstring import BitArray


class HammingCoder:
    def __init__(self, data_bits_len, secded=False) -> None:
        self.secded = secded

        self._data_bits_len = data_bits_len
        self._parity_bits_len = (
            data_bits_len + 1
        ).bit_length()  # Estimation, given total_bits ~= data_bits + redundant_bits

        # Find best parity len
        while 2**self._parity_bits_len < (data_bits_len + self._parity_bits_len + 1):
            self._parity_bits_len += 1

        self._block_len = self._data_bits_len + self._parity_bits_len

        self._is_power_of_two = lambda i: ((i - 1) & i) == 0

        print(f"Data len: {data_bits_len}, redundant len: {self._parity_bits_len}")

    # def encode_message(self, data_sequence: str):
    #     if isinstance(data_sequence, str):
    #         if data_sequence.startswith("0b"):
    #             data_bits = BitArray(data_sequence)

    #         else:
    #             data_bits = BitArray(bytes=data_sequence.encode("utf-8"))

    #     padding_bits = self._data_bits_len - (data_bits.len() % self._data_bits_len)
    #     padded_data: BitArray = data_bits + BitArray(length=padding_bits)

    #     for i in range(0, len(padded_data), self._data_bits_len):
    #         chunk = padded_data[i : i + self._data_bits_len]
    #         self.encode_block(chunk)

    def encode_block(self, bit_sequence: BitArray):
        code_block = BitArray(length=self._block_len)

        # Fill code block
        block_pos = 0
        for i in range(1, self._block_len + 1):
            # If not power of 2, then insert data bit
            if not self._is_power_of_two(i):
                code_block[i - 1] = bool(bit_sequence[block_pos])
                block_pos += 1

        # Flip the query bits to achieve parity, if needed
        xor_syndrome = 0
        for i in range(1, self._block_len + 1):
            if code_block[i - 1] != 1:
                continue

            xor_syndrome ^= i

        for i in range(self._parity_bits_len):
            redundant_pos = 1 << i

            if redundant_pos & xor_syndrome:
                code_block[redundant_pos - 1] = True

        # if self.secded:
        #     global_parity = code_block.count(True) % 2
        #     code_block.append([global_parity])

        return code_block

    def decode_block(self, code_block: BitArray):
        # Find error pos
        xor_syndrome = 0
        for i in range(1, self._block_len + 1):
            if code_block[i - 1] != 1:
                continue

            xor_syndrome ^= i

        # Change bit at error pos, if error is found
        if xor_syndrome > 0:
            if code_block[xor_syndrome]:
                code_block.invert(xor_syndrome - 1)

        # Extract data bits
        data_sequence = BitArray()
        data_pos = 0
        for i in range(1, self._block_len + 1):
            # If not power of 2, then extract data bit
            if not self._is_power_of_two(i):
                data_sequence.append([code_block[i - 1]])
                data_pos += 1

        return data_sequence[: self._data_bits_len]


if __name__ == "__main__":

    test = BitArray("0b00110001110")
    coder = HammingCoder(data_bits_len=len(test))
    print(f"Original block: {test.bin}")

    block_encoded = coder.encode_block(test)
    print(f"Original encoded block: {block_encoded.bin}")
    block_encoded.invert(2)
    print(f"Inverted encoded block: {block_encoded.bin}")

    block_decoded = coder.decode_block(block_encoded)
    print(f"Decoded block: {block_decoded}")
