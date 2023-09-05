class BlockTemplate:
    def __init__(self, range, name, description):
        self.range = range
        self.name = name
        self.description = description


class Bit:
    def __init__(self, value, absolute_position, block):
        self.value = value
        self.absolute_position = absolute_position
        self.block = block

    @property
    def block_position(self):
        return self.absolute_position - self.block.range.start


class Block:
    def __init__(self):
        self.full_bin_value = None
        self.range = None
        self.name = ""
        self.description = ""
        self.interpretation = ""
        self.blocks = []
        self.bits = []

    def extract_pure_relevant_bits(self):
        extracted_value = self.pure_bits(self.full_bin_value)[::-1][self.range.start:self.range.stop]
        return extracted_value[::-1]

    def pure_bits(self, value):
        return value.replace("0b", "")

    def binary(self):
        return f"0b{self.extract_pure_relevant_bits()}"

    def octal(self):
        return oct(int(self.binary(), 2))

    def decimal(self):
        return str(int(self.binary(), 2))

    def hexadecimal(self):
        return hex(int(self.binary(), 2))


class BlockAssigner:
    def __init__(self, predefined_blocks):
        self.predefined_blocks = predefined_blocks
        self.auto_blocks = []
        self.full_bin_value = None

    def assign(self, bit, full_bin_value):
        self.full_bin_value = full_bin_value
        block = self.find(bit)

        block.bits.append(bit)
        bit.block = block

    def find(self, bit):
        for block in self.predefined_blocks:
            if bit.absolute_position in block.range:
                return block
        return self.find_auto_block(bit)

    def blocks(self):
        bs = self.predefined_blocks + self.auto_blocks
        return sorted(bs, key=lambda b: b.range.start)

    def find_auto_block(self, bit):
        for block in self.auto_blocks:
            if bit.absolute_position - 1 in block.range:
                block.range = range(block.range.start, block.range.stop + 1)
                return block
            if bit.absolute_position + 1 in block.range:
                block.range = range(block.range.start - 1, block.range.stop)
                return block
        return self.create_new_auto_block(bit)

    def create_new_auto_block(self, bit):
        b = Block()
        b.full_bin_value = self.full_bin_value
        b.range = range(bit.absolute_position, bit.absolute_position + 1)
        b.name = "X"
        self.auto_blocks.append(b)
        return b


def generate_blocks_from_templates(templates, full_bin_value):
    # return list(map(generate_block_from_template, templates, full_bin_value))

    blocks = []
    for template in templates:
        blocks.append(generate_block_from_template(template, full_bin_value))
    return blocks

def generate_block_from_template(template, full_bin_value):
    b = Block()
    b.full_bin_value = full_bin_value
    b.range = template.range
    b.name = template.name
    b.description = template.description
    return b


class Parser:
    def __init__(self, templates):
        self.templates = templates
        self.block_assigner = None
        self.predefined_blocks = []

    def parse(self, binary_value):
        self.predefined_blocks = generate_blocks_from_templates(self.templates, binary_value)
        self.block_assigner = BlockAssigner(self.predefined_blocks)

        pure_bits = binary_value.replace("0b", "")

        block = Block()
        block.full_bin_value = binary_value
        block.range = range(0, len(pure_bits))

        for position, bit_value in enumerate(pure_bits[::-1]):
            bit = Bit(bit_value, position, None)
            self.block_assigner.assign(bit, binary_value)
            block.bits.append(bit)

        block.blocks = self.block_assigner.blocks()
        return block





