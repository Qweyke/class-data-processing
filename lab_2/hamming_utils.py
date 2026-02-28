def evaluate_parity_bits_needed(data_bits_num):
    parity_bits_num = 0
    # (2^par ≥ data + par + 1)
    while 2**parity_bits_num < (data_bits_num + parity_bits_num + 1):
        parity_bits_num += 1
        print(
            f"Step {parity_bits_num}: 2^{parity_bits_num} < {data_bits_num} + {parity_bits_num} + 1"
        )

    print(
        f"Total len needed: {parity_bits_num + data_bits_num}. Data len: {data_bits_num}, redundant len: {parity_bits_num}\n"
    )
    return parity_bits_num


def is_power_of_two(num):
    return (num - 1) & num == 0


def covered_data_bits_positions(parity_bit, code_block_len):
    for pos in range(3, code_block_len + 1):  # Start from '3' - the fist data pos
        # Get data bit with current parity bit turned on
        if not is_power_of_two(pos) and (pos & parity_bit):
            yield pos
