
code = []
with open("ans.txt", "r") as f:
    for line in f:
        code.append(line.strip())

print(code)
# Register addresses
rig={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","R7":"111"}

# operation codes

operation={ "add":"00000", "sub":"00001", "mov1":"00010","mov2":"00011", "ld":"00100", "st":"00101", "mul":"00110","div":"00111","rs":"01000","ls":"01001", "xor":"01010","Or":"01011", "and":"01100","not":"01101","cmp":"01110","jmp":"01111", "jlt":"11100", "jgt":"11101","je":"11111", "hlt":"11010", "addf":"10000", "subf":"10001", "movf":"10010"}

# code for type of instruction
typ={"add":"A","sub":"A","mov1":"B","mov2":"C","ld":"D","st":"D", "mul":"A","div":"C","rs":"B","ls":"B", "xor":"A","Or":"A","and":"A","not":"C","cmp":"C","jmp":"E","jlt":"E","jgt":"E","je":"E","hlt":"F","addf":"A","subf":"A","movf":"B"}

variable=[]
label={}
labels = {}
variables = {}

# function to convert decimal to binary
def get_binary(n):
    return format(int(n), '08b')
  
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
    n=12
    a = get_binary(n)
    machine_code = operation.get(value)
    i = 0
    while i < 2:
        machine_code += "0"
        i += 1
    machine_code += rig.get(r1) + a
    return machine_code


# function for type C

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
    while i<2:
        machine_code+="0"
        i+=1
    machine_code+=rig.get(r1)+get_binary(variables[var])
    return  machine_code

    
# function for type E
def typeE(value, label):
    machine_code = operation.get(value)
    i=0
    while i<5:
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



# print(code)

address = 0
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

