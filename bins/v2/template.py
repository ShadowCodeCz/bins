class BlockTemplate:
    def __init__(self, range, name, description):
        self.range = range
        self.name = name
        self.description = description


all = {
    "Basic A429 Label": [
        BlockTemplate(range(0, 8), "Label", ""),
        BlockTemplate(range(8, 10), "SDI", ""),
        BlockTemplate(range(10, 29), "Data", ""),
        BlockTemplate(range(29, 31), "SSM", ""),
        BlockTemplate(range(31, 32), "P", ""),
    ],
    "Basic A429 Payload": [
        BlockTemplate(range(0, 8), "Label", ""),
        BlockTemplate(range(8, 32), "Payload", ""),
    ]
}