from random import randint

PC = 0
FILE = []
OUTPUT = []

INSTRUCTIONS = {
    "add": {
        "type": "A",
        "opcode": "00000",
    },
    "sub": {
        "type": "A",
        "opcode": "00001",
    },
    "mov $Imm": {
        "type": "B",
        "opcode": "00010",
    },
    "mov": {
        "type": "C",
        "opcode": "00011",
    },
    "ld": {
        "type": "D",
        "opcode": "00100",
    },
    "st": {
        "type": "D",
        "opcode": "00101",
    },
    "mul": {
        "type": "A",
        "opcode": "00110",
    },
    "div": {
        "type": "C",
        "opcode": "00111",
    },
    "rs": {
        "type": "B",
        "opcode": "01000",
    },
    "ls": {
        "type": "B",
        "opcode": "01001",
    },
    "xor": {
        "type": "A",
        "opcode": "01010",
    },
    "or": {
        "type": "A",
        "opcode": "01011",
    },
    "and": {
        "type": "A",
        "opcode": "01100",
    },
    "not": {
        "type": "C",
        "opcode": "01101",
    },
    "cmp": {
        "type": "C",
        "opcode": "01110",
    },
    "jmp": {
        "type": "E",
        "opcode": "01111",
    },
    "jlt": {
        "type": "E",
        "opcode": "11100",
    },
    "jgt": {
        "type": "E",
        "opcode": "11101",
    },
    "je": {
        "type": "E",
        "opcode": "11111",
    },
    "hlt": {
        "type": "F",
        "opcode": "11010",
    },
}

REGISTERS = {
    "R0": {
        "address": "000",
        "value": "",
    },
    "R1": {
        "address": "001",
        "value": "",
    },
    "R2": {
        "address": "010",
        "value": "",
    },
    "R3": {
        "address": "011",
        "value": "",
    },
    "R4": {
        "address": "100",
        "value": "",
    },
    "R5": {
        "address": "101",
        "value": "",
    },
    "R6": {
        "address": "110",
        "value": "",
    },
    "FLAGS": {
        "address": "111",
        "value": "",
    },
}

LABELS = {}

LABEL_LINES = set()

VARIABLES = {}

MEMORY_ADDRESSES = set()

REGISTER_NAMES = {"R0", "R1", "R2", "R3", "R4", "R5", "R6"}


def is_reg_valid(r: str) -> bool:
    if r in REGISTER_NAMES:
        return True
    return False


def is_imm_val_valid(imm_val: str) -> bool:
    return True


def raise_error_invalid_reg(r: str):
    OUTPUT.append(f'Error in Line {PC + 1}: No register named "{r}"')


def raise_error_flag_reg_used():
    OUTPUT.append(f"Error in Line {PC + 1}: Illegal use of Flags Register")


def raise_error_imm_value(imm_val: str):
    OUTPUT.append(f"Error in Line {PC + 1}: Invalid immediate value used")


def raise_error_invalid_instruction(instruction: str):
    OUTPUT.append(f"Error in Line {PC + 1}: No instruction such as {instruction} found")


def int_to_bin_imm(imm_val: str) -> str:
    bin_val = bin(int(imm_val))[2:]
    bin_val = ("0" * (7 - len(bin_val))) + bin_val
    return bin_val


def binary_to_floating(imm_val):
    imm_val = "100.2"
    new_imm_val = imm_val.split(".")

    int_decimal = int(new_imm_val[0])

    # print(int_decimal%2)
    new_list = []
    while(int_decimal > 0):
        binary_decimal = int_decimal % 2
        new_list.append((binary_decimal))
        int_decimal = int(int_decimal/2)

    new_list.reverse()
    size = len(new_list)

    new_decimal = ""
    for i in new_list:
        i = str(i)
        new_decimal += i

    count = 0
    for i in new_imm_val[1]:
        count += 1

    decimal_2 = float(int(new_imm_val[1])/(10**count))

    after_size = (8 - size)
    new_count = 0
    new_list_2 = []
    while((decimal_2*10)%10 != 0 and new_count < after_size):
        decimal_2 *= 2
        decimal_2_str = str(decimal_2)
        new_list_2.append(decimal_2_str[0])
        new_count += 1
        
    new_str = ""
    for i in new_list_2:
        new_str += str(i)
    actual_str = (new_decimal + "." + new_str)
    

    b = actual_str.split(".")
    # print(b)
    mantissa = ""
    for i in range(1, 6):
        mantissa += b[0][i]

    exponent = (size-1)
    biased_exponent = (((exponent-1)*2)-1)
    c = bin(biased_exponent)[2:]
    c = c[:3]
    print(c)

    floating_point = (c + mantissa)
    return (floating_point)


# def int_to_bin_imm(imm_val: str) -> str:
#     #bin_val = bin(int(imm_val))[2:]
#     #bin_val = ("0" * (7 - len(bin_val))) + bin_val
#     return bin(int(imm_val)).replace("0b", "")

# Type A: 3 Register Type
# def type_a(opcode: str, reg1: str, reg2: str, reg3: str) -> str:
def type_a(opcode, line_split: list[str]) -> str:
    error = False
    if len(line_split) != 4:
        OUTPUT.append(f"Error in Line {PC + 1}: {line_split[0]} must have 3 parameters")
        error = True
        return

    for reg in line_split[1:]:
        if not is_reg_valid(reg):
            if reg == "FLAGS":
                raise_error_flag_reg_used()
            else:
                raise_error_invalid_reg(reg)
            error = True

    if error:
        return

    reg1_address = REGISTERS[line_split[1]]["address"]
    reg2_address = REGISTERS[line_split[2]]["address"]
    reg3_address = REGISTERS[line_split[3]]["address"]
    return f"{opcode}00{reg1_address}{reg2_address}{reg3_address}"


# Type B : Register and Immediate Type
# def type_b(opcode: str, reg1: str, imm_val: str) -> str:
def type_b(opcode, line_split: list[str]) -> str:
    error = False
    if len(line_split) != 3:
        OUTPUT.append(f"Error in Line {PC + 1}: {line_split[0]} must have 2 parameters")
        error = True
        return

    if not is_reg_valid(line_split[1]):
        if line_split[1] == "FLAGS":
            raise_error_flag_reg_used()
        else:
            raise_error_invalid_reg(line_split[1])
        error = True

    if not is_imm_val_valid(line_split[2]):
        raise_error_imm_value
        error = True

    if error:
        return

    reg1 = REGISTERS[line_split[1]]["address"]
    imm_val = line_split[2][1:]
    imm_val = int_to_bin_imm(imm_val)
    return f"{opcode}0{reg1}{imm_val}"


# Type C : 2 registers type
# def type_c(opcode: str, reg1: str, reg2: str) -> str:
def type_c(opcode, line_split: list[str]) -> str:
    error = False
    if len(line_split) != 3:
        OUTPUT.append(f"Error in Line {PC + 1}: {line_split[0]} must have 2 parameters")
        error = True
        return

    if not is_reg_valid(line_split[1]):
        if line_split[1] == "FLAGS":
            raise_error_flag_reg_used()
        else:
            raise_error_invalid_reg(line_split[1])
        error = True

    if not is_reg_valid(line_split[2]):
        if line_split[2] == "FLAGS":
            pass
        else:
            raise_error_invalid_reg(line_split[2])
            error = True

    if error:
        return

    reg1_address = REGISTERS[line_split[1]]["address"]
    reg2_address = REGISTERS[line_split[2]]["address"]
    return f"{opcode}00000{reg1_address}{reg2_address}"


# Type D : Register and Memory Address Type
# def type_d(opcode: str, reg1: str, mem_add: str) -> str:
def type_d(opcode, line_split: list[str]) -> str:
    error = False
    if len(line_split) != 3:
        OUTPUT.append(f"Error in Line {PC + 1}: {line_split[0]} must have 2 parameters")
        error = True
        return

    if not is_reg_valid(line_split[1]):
        if line_split[1] == "FLAGS":
            raise_error_flag_reg_used()
        else:
            raise_error_invalid_reg(line_split[1])
        error = True

    reg1 = REGISTERS[line_split[1]]["address"]

    mem_add = line_split[2]
    if not mem_add.isnumeric():  # ->variable used
        if mem_add not in VARIABLES:
            OUTPUT.append(f"Error in Line {PC + 1}: No variable named {mem_add}")
            return
        
        add = VARIABLES[mem_add]["address"]
        return f"{opcode}0000{add}"

    return f"{opcode}0{reg1}{mem_add}"


# Type E : Memory Address Type
# def type_e(opcode: str, mem_add: str) -> str:
def type_e(opcode, line_split: list[str]) -> str:
    if len(line_split) != 2:
        OUTPUT.append(f"Error in Line {PC + 1}: {line_split[0]} must have 1 parameters")
        error = True
        return

    mem_add = line_split[1]
    if not mem_add.isnumeric():  # ->label used
        if mem_add not in LABELS:
            OUTPUT.append(f"Error in Line {PC + 1}: No label named {mem_add}")
            return
        
        add = LABELS[mem_add]["address"]
        return f"{opcode}0000{add}"
    
    return f"{opcode}0000{mem_add}"
    


# Type F : Halt
# def type_f(opcode: str) -> str:
def type_f(opcode, line_split: list[str]) -> str:
    # if len(line_split) != 1:
    #     OUTPUT.append(f"Error in Line {PC + 1}: {line_split[0]} must have 1 parameters")
    #     error = True
    #     return

    return opcode + ("0" * 11)


# Storing function references
FUNCTION_TYPES = {
    "A": type_a,
    "B": type_b,
    "C": type_c,
    "D": type_d,
    "E": type_e,
    "F": type_f,
}


def gen_random_memory_address():
    address = bin(randint(20, 127))[2:]
    address = ((7 - len(address)) * "0") + address
    return address


def assign_variable(var_name: str):
    address = gen_random_memory_address()
    while address in MEMORY_ADDRESSES:
        address = gen_random_memory_address()
    VARIABLES[var_name]["address"] = address
    MEMORY_ADDRESSES.add(address)


def assign_label(label_name: str):
    address = gen_random_memory_address()
    while address in MEMORY_ADDRESSES:
        address = gen_random_memory_address()
    LABELS[label_name]["address"] = address
    MEMORY_ADDRESSES.add(address)


def load_file(filename: str):
    with open(filename, "r") as f:
        FILE_TEMP = f.readlines()

    for i in range(len(FILE_TEMP)):
        line_split = FILE_TEMP[i].strip().split()

        if line_split[0][-1] == ":":
            LABELS[line_split[0][:-1]] = {}  # Check -1 or not
            LABEL_LINES.add(len(FILE))

        if line_split[0] == "var":
            VARIABLES[line_split[1]] = {}

        FILE.append(line_split)


def check_hlt():
    HALT_AT = {}
    for i in range(len(FILE)):
        hlt_count = FILE[i].count("hlt")
        if hlt_count > 0:
            HALT_AT[i] = hlt_count
            if hlt_count > 1:
                OUTPUT.append(
                    f"Error in Line {i + 1}: Multiple halt statements encountered in one line"
                )

    if len(HALT_AT) == 0:
        OUTPUT.append(f"Error: Halt statement is required in the program")
        return

    for i in range(max(HALT_AT) + 1, len(FILE)):
        if len(FILE[i]) != 0:
            OUTPUT.append(
                f"Error in Line {i + 1}: Halt statement should be the last statement"
            )
            return


def load_memory_adresses():
    for line_split in FILE:
        if line_split[0] in {"ld", "st"}:
            if len(line_split) == 3:
                if line_split[2].isnumeric():
                    MEMORY_ADDRESSES.add(line_split(2))
        elif line_split[0] in {"jmp", "jlt", "jgt", "je"}:
            if len(line_split) == 2:
                if line_split[1].isnumeric():
                    MEMORY_ADDRESSES.add(line_split[1])


def read_file():
    for i in range(len(FILE)):
        pass


def write_file(filename: str):
    with open(filename, "w") as f:
        for o in OUTPUT:
            if o is not None:
                f.write(o)
                f.write("\n")


def execute_instruction(line_split: list[str]):
    # Label statement encountered
    if PC in LABEL_LINES:
        # assign_label(line_split[0])
        LABELS[line_split[0][:-1]]["freq"] += 1
        line_split = line_split[1:]

    # Blank line encountered
    if len(line_split) == 1 and line_split[0] == "":
        return PC + 1

    # Variable assignment instruction
    if line_split[0] == "var":
        for i in range(0, PC):
            if len(FILE[i]) > 0:
                if line_split[1] != "var":
                    OUTPUT.append(
                        f"Error in line {PC + 1}: Variable assignment must be done in the beginning of the program"
                    )
                    return PC + 1

        if VARIABLES[line_split[1]]["freq"] == 1:
            OUTPUT.append(f"Error in line {PC + 1}: Variable already assigned")
            return PC + 1

        VARIABLES[line_split[1]]["freq"] += 1
        return PC + 1

    instruction = line_split[0]
    if instruction not in INSTRUCTIONS:
        raise_error_invalid_instruction(instruction)
        return PC + 1

    type_of_instruction = INSTRUCTIONS[instruction]["type"]
    opcode_of_instruction = INSTRUCTIONS[instruction]["opcode"]

    # Since mov has 2 types of instructions
    if instruction == "mov":
        if line_split[2][0] == "$":  # Immediate value used
            opcode_of_instruction = "00010"
            result = type_b(opcode_of_instruction, line_split)
            OUTPUT.append(result)
        else:  # Register used
            result = type_c(opcode_of_instruction, line_split)
            OUTPUT.append(result)
        return PC + 1

    function_to_call = FUNCTION_TYPES[type_of_instruction]
    result = function_to_call(opcode_of_instruction, line_split)
    OUTPUT.append(result)

    if instruction == "hlt":
        return len(FILE) + 1

    return PC + 1


def assign_all_label_adresses():
    for l in LABELS:
        LABELS[l] = {"address": None, "freq": 0}
        assign_label(l)

def assign_all_var_adresses():
    for v in VARIABLES:
        VARIABLES[v] = {"address": None, "freq": 0}
        assign_variable(v)

def assemble():
    check_hlt()
    load_memory_adresses()
    assign_all_label_adresses()
    assign_all_var_adresses()
    global PC
    while PC < len(FILE):
        line_split = FILE[PC]
        next_line = execute_instruction(line_split)
        PC = next_line


def init():
    global PC, FILE, OUTPUT, LABELS, VARIABLES, LABEL_LINES
    PC = 0
    FILE, OUTPUT = [], []
    LABELS, VARIABLES = {}, {}
    LABEL_LINES = set()

    for r in REGISTERS:
        REGISTERS[r]["value"] = ""


def print_output():
    for o in OUTPUT:
        print(o)


def main():
    init()
    load_file("sample.txt")
    assemble()
    print_output()
    write_file("output.txt")


if __name__ == "__main__":
    main()
