"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) is not 2:
            print("Must include filename")
            sys.exit(1)

        address = 0

        program = sys.argv[1]

        with open(program) as prog:
            for line in prog:
                line = line.strip()
                split = line.split('#')[0]
                if split == '':
                    continue
                value = int(split, 2)
                self.ram[address] = value
                address += 1

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Load immediate, store a value in a register, 'set this register to this value'
        LDI = 0b10000010
        # prints numeric value stored in register
        PRN = 0b01000111
        # does multiplication(?)
        MUL = 0b10100010
        # add
        ADD = 0b10100000
        # pushing and popping
        PUSH = 0b01000101
        POP  = 0b01000110
        # call and return
        CALL = 0b01010000
        RET = 0b00010001
        # stack pointer
        SP = 255
        # halt cpu, exit emulator
        HLT = 0b0000001

        running = True
        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3

            elif IR == ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3

            elif IR == PUSH:
                SP -= 1
                self.ram_write(SP, self.reg[operand_a])
                self.pc += 2

            elif IR == POP:
                self.reg[operand_a] = self.ram[SP]
                SP += 1
                self.pc += 2

            elif IR == CALL:
                value = self.pc + 2
                SP -= 1
                self.ram[SP] = value
                self.pc = self.reg[operand_a]
            
            elif IR == RET:
                self.pc = self.ram[SP]
                SP += 1

            elif IR == HLT:
                running = False

            else:
                self.pc += 1