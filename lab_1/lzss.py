from math import log2, ceil
from bitstring import BitArray, BitStream

BYTE_LEN = 8


class LZSS:
    def __init__(self, sb_size=256, lab_size=32):
        self.search_buf_len = sb_size  # W, window size
        self.offset_bits = ceil(log2(self.search_buf_len))

        self.look_ahead_buf_len = lab_size

    def _encode_length_by_elias(self, length: int) -> str:
        if length == 1:
            return "0b0"

        # bin'()
        full_bin_l3 = bin(length)[2:]
        l3_part = full_bin_l3[1:]
        l3_total_len = len(full_bin_l3)

        # bin'(|bin'|)
        full_bin_l2 = bin(l3_total_len)[2:]
        l2_part = full_bin_l2[1:]
        l2_total_len = len(full_bin_l2)

        # unar(| bin'(|bin'|)| + 2)
        l1_part = "1" * (l2_total_len + 2) + "0"

        return "0b" + l1_part + l2_part + l3_part

    def encode(self, input_sequence: str):
        bit_stream = BitArray()

        pos = 0
        while pos < len(input_sequence):
            search_buf: str = input_sequence[max(0, pos - self.search_buf_len) : pos]

            # Match return-params
            match_length = 0
            match_start_pos = -1
            # Match search loop
            for increment in range(1, self.look_ahead_buf_len + 1):
                candidate = input_sequence[pos : pos + increment]

                search_res = search_buf.rfind(candidate)
                if search_res <= -1:
                    break

                match_length = len(candidate)
                match_start_pos = search_res

            # Assemble output bit-sequence
            if match_length >= 2:
                bit_stream.append("0b1")
                offset = len(search_buf) - match_start_pos
                bit_stream.append(f"uint:{self.offset_bits}={offset}")

                length_bit = self._encode_length_by_elias(match_length)
                bit_stream.append(length_bit)

                pos += match_length

            else:
                bit_stream.append("0b0")
                bit_stream.append(f"uint:{BYTE_LEN}={ord(input_sequence[pos])}")
                pos += 1

        return bit_stream

    def _decode_length_by_elias(self, stream: BitStream):
        unary_len = 0
        while stream.read("bool"):
            unary_len += 1

        l2_total_len = unary_len - 2
        if l2_total_len <= 0:
            return 1

        l3_bits = "1"
        if l2_total_len > 1:
            l3_bits += stream.read(f"bin:{l2_total_len - 1}")
        l3_total_len = int(l3_bits, 2)

        final_bits = "1"
        if l3_total_len > 1:
            final_bits += stream.read(f"bin:{l3_total_len - 1}")

        return int(final_bits, 2)

    def decode(self, code_sequence: BitArray):
        decoded_sequence = ""

        stream = BitStream(code_sequence)
        while stream.pos < stream.len:
            if stream.read("bool"):
                offset = stream.read(f"uint:{self.offset_bits}")
                match_length = self._decode_length_by_elias(stream)

                start_pos = len(decoded_sequence) - offset
                for i in range(match_length):
                    decoded_sequence += decoded_sequence[start_pos + i]

            else:
                char_code = stream.read(f"uint:{BYTE_LEN}")
                decoded_sequence += chr(char_code)

        return decoded_sequence


lz = LZSS()
encoded = lz.encode(input_sequence="abrababr atritigratri")
print(lz.decode(encoded))
