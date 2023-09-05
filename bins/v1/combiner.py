
class Combiner:
    def __init__(self):
        self.value = 0
        self.bits_size = 32

    def set(self, value, bits_size):
        self.value = value
        self.bits_size = bits_size

    def bin(self):
        return format(int(self.save_value()), f'#0{self.save_bits_size() + 2}b')

    def save_bits_size(self):
        try:
            return int(self.bits_size)
        except Exception as e:
            return 32

    def save_value(self):
        try:
            return int(str(self.value), 0)
        except Exception as e:
            return 0