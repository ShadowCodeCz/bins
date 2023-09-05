class BlockTemplate:
    def __init__(self, range, name, description):
        self.range = range
        self.name = name
        self.description = description


all = {
    "Basic A429 Label": [
        BlockTemplate(range(0, 8), "Label", "ARINC A429 label. It expressed in octal."),
        BlockTemplate(range(8, 10), "SDI", "Source/Destination Identifiers (SDI) and may indicate the intended receiver or, more frequently, indicate the transmitting subsystem."),
        BlockTemplate(range(10, 29), "Data", "Bit-field discrete data, Binary Coded Decimal (BCD), and Binary Number Representation (BNR) are common ARINC 429 data formats. Data formats may also be mixed."),
        BlockTemplate(range(29, 31), "SSM", "SSM bits are the Sign/Status Matrix (SSM)"),
        BlockTemplate(range(31, 32), "P", "P is the parity bit, and is used to verify that the word was not damaged or garbled during transmission. "),
    ],
    "Basic A429 Payload": [
        BlockTemplate(range(0, 8), "Label", ""),
        BlockTemplate(range(8, 32), "Payload", ""),
    ]
}