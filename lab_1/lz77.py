class LZ77:
    def __init__(self, sb_size=256, lab_size=32):
        self.sb_size = sb_size
        self.lab_size = lab_size

    def encode(self, input_str: str = "abrababratritigratri"):
        output_tuples = []

        curr_pos = 0
        while curr_pos < len(input_str):

            found_idx = -1
            comb_len = 0
            search_buf: str = input_str[max(0, curr_pos - self.sb_size) : curr_pos]
            for advance in range(1, self.lab_size + 1):
                combination = input_str[curr_pos : curr_pos + advance]
                res = search_buf.rfind(combination)
                if res < 0:
                    break

                else:
                    comb_len = len(combination)
                    found_idx = res

            offset = (len(search_buf) - found_idx) if found_idx != -1 else 0
            next_char_pos = curr_pos + comb_len
            next_char = (
                input_str[next_char_pos] if next_char_pos < len(input_str) else ""
            )
            output_tuples.append((offset, comb_len, next_char))

            curr_pos = next_char_pos + 1

        return output_tuples

    def decode(self, instructions: list):
        output_str = ""
        curr_pos = 0
        for instr in instructions:
            offset, length, char = instr

            offset_pos = curr_pos - offset
            combination = output_str[offset_pos : max(0, offset_pos + length)]
            output_str += combination + char

            curr_pos += length + 1

        return output_str


lz = LZ77()
encoded = lz.encode()

print(lz.decode(encoded))
