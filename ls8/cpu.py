"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101

POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.pc = 0
        self.ram = [0] * 256
        self.halted = False
        self.sp = 7


    def load(self, filename):
        """Load a program into memory."""

        address = 0
        # open the file
        with open(filename) as my_file:
            # go through each line to parse and get
            # the instruction
            for line in my_file:
                # try and get the instruction/operand in the line
                comment_split = line.split("#")
                maybe_binary_number = comment_split[0]
                try:
                    x = int(maybe_binary_number, 2)
                    self.ram_write(x, address)
                    address += 1
                except:
                    continue
            space_for_stack = 256 - len(filename)
            memory = filename + [0] * space_for_stack
            return memory

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == MUL:
            self.registers[reg_a] *= self.registers[reg_b]
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            if IR == HLT:
                self.halted = True
                self.pc += 1
            elif IR == PRN:
                print(self.registers[operand_a])
                self.pc += 2
            elif IR == LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif IR == PUSH:
                self.registers[self.sp] -= 1
                reg_address = self.ram[self.pc+1]
                self.ram[self.registers[self.sp]] = self.registers[reg_address]
                self.pc += 2
            elif IR == POP:
                reg_address = self.ram[self.pc+1]
                self.registers[reg_address] = self.ram[self.registers[self.sp]]
                self.registers[self.sp] += 1
                self.pc += 2