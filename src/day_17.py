import re

from pathlib import Path

DATA_PATH = Path("data")


class Computer:
    def __init__(self, register_a, register_b, register_c, program):
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c

        self.program = program
        self.output = ""

        self.pointer = 0
        self.jump = 2

    def map_instructions(self, instruction: int):
        return {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }[instruction]

    def translate_combo_operand(self, operand: int):
        return {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: self.register_a,
            5: self.register_b,
            6: self.register_c,
        }[operand]

    @staticmethod
    def int_to_bits(n: int) -> str:
        return "{:b}".format(n)

    @staticmethod
    def bits_to_int(s: str) -> int:
        return int(s, 2)

    def adv(self, operand: int):
        self.register_a = self.register_a // pow(
            2, self.translate_combo_operand(operand)
        )

    def bxl(self, operand: int):
        self.register_b = self.register_b ^ operand

    def bst(self, operand: int):
        self.register_b = self.bits_to_int(
            self.int_to_bits(self.translate_combo_operand(operand))[-3:]
        )

    def jnz(self, operand: int):
        if self.register_a != 0:
            self.pointer = operand
            self.jump = 0

    def bxc(self, operand: int):
        self.register_b = self.register_b ^ self.register_c

    def out(self, operand: int):
        result = self.bits_to_int(
            self.int_to_bits(self.translate_combo_operand(operand))[-3:]
        )
        self.output += str(result)

    def bdv(self, operand: int):
        self.register_b = self.register_a // pow(
            2, self.translate_combo_operand(operand)
        )

    def cdv(self, operand: int):
        self.register_c = self.register_a // pow(
            2, self.translate_combo_operand(operand)
        )

    def run(self):
        while self.pointer < len(self.program):
            instruction = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            self.map_instructions(instruction)(operand)
            self.pointer += self.jump
            # Reset jump
            self.jump = 2

        return ",".join(list(self.output))


with open(DATA_PATH / "day_17_toy_2.txt") as f:
    data = f.read()

a_register, b_register, c_register = [
    int(x) for x in re.findall(r"Register [A|B|C]: (\d+)", string=data)
]

program = [int(x) for x in data.split("Program: ")[1].split(",")]
print(f"Register A: {a_register}")
print(f"Register B: {b_register}")
print(f"Register C: {c_register}")
print(f"Program: {program}")

# Part 1
computer = Computer(a_register, b_register, c_register, program)
output = computer.run()

# Part 2
output = ""
a_register = 0
while output != ",".join([str(f) for f in program]):
    computer = Computer(a_register, b_register, c_register, program)
    output = computer.run()
    a_register += 1
    # if a_register % 10_000 == 0:
    #     print(f"Register A: {a_register}")
    #     print(f"Output:   {output}")
    #     print(f"Expected: {','.join([str(f) for f in program])}")

print(f"Register A: {a_register - 1}")
