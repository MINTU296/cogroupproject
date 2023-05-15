
code = []
with open("ans.txt", "r") as f:
    for line in f:
        code.append(line.strip())

print(code)
# Register addresses
rig={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

# operation codes

operation={ "add":"00000", "sub":"00001", "mov1":"00010","mov2":"00011", "ld":"00100", "st":"00101", "mul":"00110","div":"00111","rs":"01000","ls":"01001", "xor":"01010","or":"01011", "and":"01100","not":"01101","cmp":"01110","jmp":"01111", "jlt":"11100", "jgt":"11101","je":"11111", "hlt":"11010", "addf":"10000", "subf":"10001", "movf":"10010"}

# code for type of instruction
typ={"add":"A","sub":"A","mov1":"B","mov2":"C","ld":"D","st":"D", "mul":"A","div":"C","rs":"B","ls":"B", "xor":"A","or":"A","and":"A","not":"C","cmp":"C","jmp":"E","jlt":"E","jgt":"E","je":"E","hlt":"F","addf":"A","subf":"A","movf":"B"}

variable=[]
label={}
labels = {}
variables = {}

# function to convert decimal to binary
def get_binary(n):
    return format(int(n), '07b')
  
# function for type A
def typeA(value, r1, r2, r3):
    machine_code = operation.get(value)
    i = 0
    while i < 2:
        machine_code += "0"
        i += 1
    machine_code += rig.get(r1) + rig.get(r2) + rig.get(r3)
    
    return machine_code


# function for type B
def typeB(value, r1, n):
    a = get_binary(n)
    machine_code = operation.get(value)
    i = 0
    while i < 1:
        machine_code += "0"
        i += 1
    machine_code += rig.get(r1) + a
    return machine_code


# function for type C
# def typeC(value, r1, r2):
#     machine_code = operation.get(value)
    
#     if r1 in rig and r2 in rig:
#         machine_code += rig.get(r1) + rig.get(r2)
#     else:
#         # Handle the case where either r1 or r2 is not a valid key in rig
#         # You can raise an exception, return an error code, or handle it based on your requirements
#         raise KeyError("Invalid register(s) in typeC")
    
#     return machine_code


def typeC(value, r1, r2):
    machine_code = operation.get(value)
    
    i=0
    while i<5:
        machine_code+="0"
        i+=1
    machine_code+=rig.get(r1)+rig.get(r2)
    return machine_code

# function for type D
def typeD(value, r1, var):
    machine_code = operation.get(value)
    i=0
    while i<1:
        machine_code+="0"
        i+=1
    machine_code+=rig.get(r1)+get_binary(variables[var])
    return  machine_code

    
# function for type E
def typeE(value, label):
    machine_code = operation.get(value)
    i=0
    while i<4:
        machine_code+="0"
        i+=1
    machine_code+=get_binary(labels[label+':'])
    return machine_code


# function for type F
def typeF(value):
    machine_code = operation.get(value)
    while(len(machine_code)<16):
        machine_code+="0"
    return machine_code

def check_errors(code):
    operations = {
        "mov": "A",
        "add": "A",
        "sub": "A",
        "mul": "A",
        "div": "A",
        "jmp": "C",
        "jz": "C",
        "jnz": "C",
        "je": "C",
        "jne": "C",
        "label": "E",
        "var": "F"
    }

    error_types = {
        "a": "Typo in instruction",
        "b": "Undefined use of variables",
        "c": "Undefined use of labels",
        "d": "Illegal use of flags",
        "e": "Illegal value (greater than 8 bits)",
        "f": "Label defined as variable or variable defined as label",
        "g": "Variable not defined in the beginning",
        "h": "Missing halt instruction",
        "i": "Last line not halt",
        "j": "General error"
    }

    variables = []
    labels = {}
    errors = []
    register_withoutflag = {
    "R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110"
}

    def add_error(address, error_type, extra_message=""):
        error_message = f"Line number {address} has an error of type: {error_types[error_type]}"
        if extra_message:
            error_message += " " + extra_message
        errors.append(error_message)

    def check_typo(address, parameter_name, n):
        if parameter_name not in operations.keys() and n == 1:
            add_error(address, "a")
            exit()
        elif parameter_name not in rig.keys() and n == 0:
            add_error(address, "a")
            exit()

    def check_undefined_variable(address, variable_name):
        add_error(address, "b", variable_name)
        exit()

    def check_undefined_label(address, label_name):
        add_error(address, "c", label_name)
        exit()

    def check_illegal_flags(address):
        add_error(address, "d")
        exit()

    def check_illegal_immvalue(address, immvalue):
        if immvalue > 127 or immvalue < 0:
            add_error(address, "e")
            exit()

    def check_label_var(address, name, n):
        if name not in labels and n == 1:
            if name in variables:
                add_error(address, "f")
                exit()

        if name not in variables and n == 0:
            if name in labels:
                add_error(address, "f")
                exit()

    def check_not_def_variable_beg(address):
        add_error(address, "g")
        exit()

    def check_miss_halt(address):
        add_error(address, "h")
        exit()

    def check_last_not_hlt():
        add_error(line_number, "i")
        exit()

    def check_general_error(address):
        add_error(address, "j")
        exit()

    def check_variable_errors(flag, line):
        nonlocal line_number

        if flag:
            if line[1].isdigit():
                check_general_error(line_number)
            if len(line) == 2:
                if line[1] not in variables:
                    if line[1] not in rig:
                        variables.append(line[1])
                    else:
                        add_error(line_number, "j", "Register name used as variable name")
                        exit()
                else:
                    check_general_error(line_number)
            else:
                check_general_error(line_number)
        else:
            check_not_def_variable_beg(line_number)

    var_flag = True
    hlt_flag = True
    line_number = 0

    for line in code:
        line_list=line.split()

        if len(line_list) == 0:
            continue

        line_number += 1

        if line_list[0] == "var":
            check_variable_errors(var_flag, line_list)
            continue
        else:
            var_flag = False
        
        if not hlt_flag:
            check_last_not_hlt()
        
        if "FLAGS" in line_list:
            if line_list[0] == "mov" and line_list[1] == "FLAGS" and line_list[2] in register_withoutflag:
                pass
            else:
                check_illegal_flags(line_number)
        if line_list[0][-1]==":":
            labels[line_list[0][:-1]] = [True, line_number]
            line_list.pop(0)

        if line_list[0] == "mov":
            if line_list[2][0]=="$":
                line_list[0] = "mov1"
            else:
                line_list[0] = "mov2"

        if line_list[0] == "movf":
            if line_list[1] in register_withoutflag:
                if float(line_list[2][1:])<1:
                    add_error(line_number, "j", "Floating point number less than 1")
                    exit()
                try:
                    aa,bb=line_list[2][1:].split(".")
                    continue
                except:

                    add_error(line_number, "j", "immediate value not a floating point number")
                    exit()
            else:
                check_general_error(line_number)
            if line_list[0] in operations.keys():
                operation_type=operations[line_list[0]]
                if operation_type=="A":
                    if len(line_list)==4:
                        for i in range(1,len(line_list)):
                            check_typo(line_number, line_list[i], 0)
                    else:
                        check_general_error(line_number)

                elif operation_type=="B":
                    if len(line_list)==3:
                        check_typo(line_number, line_list[1], 0)
                        if line_list[2][0]!="$":
                            check_general_error(line_number)
                        try:
                            imm_value = int(line_list[2][1:])
                            check_illegal_immvalue(line_number, imm_value)
                        except:
                            check_illegal_immvalue(line_number, 127)
                    else:
                         check_general_error(line_number)

                elif operation_type == "C":
                    if len(line_list) == 3:
                        for i in range(1, len(line_list)):
                            check_typo(line_number, line_list[i], 0)
                    else:
                        check_general_error(line_number)

                elif operation_type == "D":
                    if len(line_list) == 3:
                        check_typo(line_number, line_list[1], 0)
                        check_label_var(line_number, line_list[2], 0)

                        if line_list[2] not in variables:
                            check_undefined_variable(line_number, line_list[2])
                    else:
                        check_general_error(line_number)

                elif operation_type == "E":
                    if len(line_list) == 2:
                        check_label_var(line_number, line_list[1], 1)

                        if line_list[1] not in labels:
                            labels[line_list[1]] = [False, line_number]
                    else:
                        check_general_error(line_number)

                elif operation_type == "F":
                    if len(line_list) == 1:
                        if not hlt_flag:
                            check_last_not_hlt()
                        hlt_flag = False
                    else:
                        check_general_error(line_number)

                else:
                    check_typo(line_number, line_list[0], 1)

            if hlt_flag:
                check_miss_halt(line_number)
            for label_name, label_info in labels.items():
                if not label_info[0]:
                    check_undefined_label(label_info[1], label_name)
            
            return errors
            

address = -1
for line in code:

    if len(line) == 0:
        continue

    line_list = list(line.split())

    if line_list[0] == "mov":
        if line_list[2][0] == "$":
            line_list[0] = "mov1"
        else:
            line_list[0] = "mov2"

    if (line_list[0] in operation and line_list[0] != "hlt"):
        address += 1

    elif (line_list[0] == "hlt"):
        address += 1
        labels[line_list[0]] = address

    elif (line_list[0][-1] == ":"):
        address += 1
        labels[line_list[0]] = address


for line in code:
    if (len(line) == 0):
        continue
    line_list = list(line.split())
    if line_list[0] == "var":
        address += 1
        variables[line_list[1]] = address


for line in code:
    
    if(len(line) == 0):
        continue

    line_list = list(line.split())


    if(len(line_list) > 1 and line_list[0] in labels):
        line_list.pop(0)

    if line_list[0] == "mov":
        if line_list[2][0] == "$":
            line_list[0] = "mov1"
        else:
            line_list[0] = "mov2"

    if line_list[0] in operation.keys():
      

        if typ[line_list[0]][0] == "A":

            print(typeA(line_list[0], line_list[1], line_list[2],line_list[3]))

        elif typ[line_list[0]][0] == "B":
            

            print(typeB(line_list[0], line_list[1], line_list[2][1:]))

        elif typ[line_list[0]][0] == "C":

            print(typeC(line_list[0], line_list[1], line_list[2]))

        elif typ[line_list[0]] == "D":
            print(typeD(line_list[0], line_list[1], line_list[2]))
            

        elif typ[line_list[0]][0] == "E":

            print(typeE(line_list[0], line_list[1]))

        elif typ[line_list[0]][0] == "F":

            print(typeF(line_list[0])) 




