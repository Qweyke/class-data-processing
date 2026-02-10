from math import log2, ceil
from bitstring import BitArray, BitStream
import pandas as pd

BYTE_LEN = 8


class LZSS:
    def __init__(self, sb_size=32, lab_size=32):
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

    def encode_with_table(self, input_sequence: str):
        steps = []
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

            # Data for table step
            step_data = {
                "Symbol sequence": "",
                "Flag": 0,
                "d": "-",
                "l": 0,
                "Code sequence": "",
                "Bits": 0,
            }

            # Assemble output bit-sequence
            if match_length >= 2:
                bit_stream.append("0b1")
                offset = len(search_buf) - match_start_pos
                bit_stream.append(f"uint:{self.offset_bits}={offset}")

                length_bit = self._encode_length_by_elias(match_length)
                bit_stream.append(length_bit)

                # Fill table data for match
                step_data["Flag"] = 1
                step_data["Symbol sequence"] = input_sequence[pos : pos + match_length]
                step_data["d"] = f"{offset}({pos})"
                step_data["l"] = match_length
                step_data["Code sequence"] = (
                    f"1 [{bin(offset)[2:].zfill(self.offset_bits)}] |{length_bit[2:]}|"
                )
                step_data["Bits"] = 1 + self.offset_bits + (len(length_bit) - 2)

                pos += match_length

            else:
                bit_stream.append("0b0")
                bit_stream.append(f"uint:{BYTE_LEN}={ord(input_sequence[pos])}")

                # Fill table data for literal
                char = input_sequence[pos]
                step_data["Flag"] = 0
                step_data["Symbol sequence"] = char
                step_data["Code sequence"] = f"0 [{bin(ord(char))[2:].zfill(BYTE_LEN)}]"
                step_data["Bits"] = 1 + BYTE_LEN

                pos += 1

            steps.append(step_data)

        # Generate DataFrame and Summary
        df = pd.DataFrame(steps)
        total_bits = df["Bits"].sum()
        original_bits = len(input_sequence) * BYTE_LEN

        summary_row = {col: "" for col in df.columns}
        summary_row["Symbol sequence"] = "TOTAL"
        summary_row["Bits"] = total_bits
        summary_row["Code sequence"] = (
            f"Compression: {100 - (total_bits/original_bits*100):.2f}%"
        )

        df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)

        return bit_stream, df

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


test = "IF_WE_CANNOT_DO_AS_WE_WOULD_WE_SHOULD_DO_AS_WE_CAN"
test2 = "abrababr atritigratriritigratrabrtrari ratit patati"

lz = LZSS()
encoded, lz_df = lz.encode_with_table(input_sequence=test)
print(lz_df)

total_bits = lz_df["Bits"].sum()
print(f"Encoded: {lz.decode(encoded)}")
