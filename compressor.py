from string import ascii_letters, digits
from typing import Union

class Compressor():
    "Convert between number and string representation of a different base made from defined"
    def __init__(self, char_space: str = ascii_letters + digits, precision: float = 1) -> None:
        """
        Variables:
        char_space: A string of any characters that will make up your new representation
        precision:  How precise the compressed number will be once uncompressed. Always will be rounded down. e.g.
            0.1 : Accurate to one decimal places
            5 : Rounded down to the nearest five
        """
        self.char_space = "".join(sorted(set(char_space)))
        self.base = len(self.char_space)
        self.precision = precision

        assert precision > 0, "precision must be greater than 0"

    def _extract_power_multipliers(self, value: int, character_index: int) -> str:
        results:list = []
        current_power = self.base**character_index
        if character_index == 0:
            return [value]
        for i in range(self.base):
            next_char_val = current_power * (i + 1)
            if next_char_val > value:
                results = [i]
                results.extend(self._extract_power_multipliers(value-(current_power*i), character_index-1))
                return results

    def compress(self, value: Union[int, float]) -> str:
        "Convert number into different base and characters"
        value = int(value/self.precision)

        exp = 0
        while self.base**exp <= value:
            exp += 1

        return "".join([self.char_space[i] for i in self._extract_power_multipliers(value, exp-1)])
    
    def decompress(self, value: str) -> Union[int, float]:
        "Convert string from compress into number"
        return round(sum([self.char_space.index(char)*(self.base**i) for i, char in enumerate(reversed(value))])*self.precision, len(str(self.precision).split(".")[-1]))

