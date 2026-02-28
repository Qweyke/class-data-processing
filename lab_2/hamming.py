from bitstring import BitArray

from hamming_utils import (
    covered_data_bits_positions,
    evaluate_parity_bits_needed,
    is_power_of_two,
)


def encode_block(input_data: BitArray):
    print(f"Sequence to encode: {input_data.bin}")

    parity_bits = evaluate_parity_bits_needed(len(input_data))
    encoded_len = parity_bits + len(input_data)

    # Create code block for assembling
    encoded = BitArray(encoded_len)

    # Fill in the data bits
    data_idx = 0
    for pos in range(1, encoded_len + 1):
        if not is_power_of_two(pos):
            python_index = pos - 1
            encoded[python_index] = input_data[data_idx]
            data_idx += 1

    # Fill in parity bits
    for power in range(parity_bits):
        # Get next 2^power
        parity_bit_pos = 1 << power

        print(
            f"Checking parity bit at position {parity_bit_pos}[{bin(parity_bit_pos)}] with py-index {parity_bit_pos - 1}"
        )
        xor_parity_res = 0  # Gives bit-value to achieve parity
        for data_pos in covered_data_bits_positions(parity_bit_pos, encoded_len):
            python_index = data_pos - 1
            xor_parity_res ^= encoded[python_index]
            print(
                f"Data at pos {data_pos} is under current parity bit. Current XOR-result inference: {"odd" if xor_parity_res else "even"}"
            )

        if xor_parity_res:
            print(
                f"Final parity inference - odd. Inverting parity-bit to {xor_parity_res}"
            )
            python_index = parity_bit_pos - 1
            encoded[python_index] = bool(xor_parity_res)

        else:
            print(f"Final parity inference - even. No invert needed")

        print(f"Current encoded state: {encoded.bin}\n")

    return encoded


def decode_block(encoded: BitArray):
    print(f"Sequence to decode: {encoded.bin}")
    encoded_len = len(encoded)

    # Find error position by XOR
    xor_syndrome = 0
    for pos in range(1, encoded_len + 1):
        python_idx = pos - 1

        # XOR only position where data is True, because False doesn't affect parity
        if encoded[python_idx] == True:
            xor_syndrome ^= pos
            print(
                f"Data bit at position {pos}[{bin(pos)}] with py-index {python_idx} is True. Using XOR"
            )

    if xor_syndrome > encoded_len:
        print(
            f"HAMMING: More than one error found - correction is impossible. Found position: {xor_syndrome}, python-index {xor_syndrome - 1}"
        )
        return None

    elif xor_syndrome == 0:
        print(f"HAMMING: No errors detected")
    else:
        # Correct error
        python_xor_syndrome = xor_syndrome - 1
        encoded.invert(python_xor_syndrome)
        print(
            f"HAMMING: Error found and corrected to {encoded[python_xor_syndrome]}. Found position: {xor_syndrome},  python-index {python_xor_syndrome}"
        )

    # Assemble decoded data
    decoded = BitArray()
    for pos in range(1, encoded_len + 1):
        if not is_power_of_two(pos):
            python_idx = pos - 1
            decoded.append([encoded[python_idx]])

    return decoded


if __name__ == "__main__":
    test = BitArray("0b0011000111")
    block_encoded = encode_block(test)

    # Invert at python index, for hamming-count position use + 1
    block_encoded.invert(3)
    inverted: str = f"{block_encoded}"
    print(f"Inverted encoded: {block_encoded.bin}")

    block_decoded = decode_block(block_encoded)
    if block_decoded:
        print(f"Decoded block: {block_decoded.bin}")

    print(
        f"Origin sequence: {test} -> Encoded: {block_encoded} -> Inverted: {inverted} -> Decoded {block_decoded} "
    )
