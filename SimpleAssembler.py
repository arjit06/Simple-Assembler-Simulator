import sys
from string import ascii_letters


Opcode={"add":["10000","A"],"sub":["10001","A"],"mov_i":["10010","B"],
"mov_r":["10011","C"],"ld":["10100","D"],"st":["10101","D"],"mul":["10110","A"],
"div":["10111","C"],"rs":["11000","B"],"ls":["11001","B"],"xor":["11010","A"],
"or":["11011","A"],"and":["11100","A"],"not":["11101","C"],"cmp":["11110","C"],"jmp":["11111","E"],
"jlt":["01100","E"],"jgt":["01101","E"],"je":["01111","E"],"hlt":["01010","F"],"addf":["00000","A"],"subf":["00001","A"],"movf":["00010","B"]}

type_len={"A":4,"B":3,"C":3,"D":3,"E":2,"F":1}
instructions=["var","add","sub","mul","div","rs","ls","mov","ld","st","xor","and","or","not","cmp","jmp","jlt","jgt","je","hlt","addf","subf","movf"]
register=["R0","R1","R2","R3","R4","R5","R6"]

keywords=instructions.copy()
keywords.append(':')
keywords.append('FLAGS')
keywords.extend(register)



def check_keyword(file):
    file.seek(0)
    flag=0
    count_of_instruction=1
    for line in file:
        if (count_of_instruction>256):
            break
        l=line.split()
        if len(l)<2 :
            return True
        if l[0]=='var':

            if l[1] in keywords:
                y=f"Line Number {count_of_instruction} : The variable name is a reserved keyword"
                print(y)
                flag=1
            
        if l[0][-1]==':':
            if l[0][0:-1] in keywords:
                y=f"Line Number {count_of_instruction} : The label name is a reserved keyword"
                print(y)
                flag=1
        count_of_instruction+=1
    if flag==1:
        return False
    else:
        return True



def valid_instruction(inst, count_of_instruction):
    """
    Checks whether the length of the instruction is valid or not.
    """
    if(inst==[]):
        return True
    if inst[0] in instructions or inst[0]=="var":
        return True
    if ":" == inst[0][-1]:
        if(len(inst)==1):
            y=f"Line Number {count_of_instruction} : The input is not a valid instruction"
            print(y)
            return False
        inst = inst[1:]
    if inst[0] in instructions or inst[0]=="var":
        return True
    y=f"Line Number {count_of_instruction} : The input is not a valid instruction"
    print(y)
    return False

def valid_reg_help(reg):
    if reg in register:
        return True
    return False
#check is there are multiple label of same name
def morelabels(file):
    labellist=[]
    count=0
    flag=1
    file.seek(0)
    for line in file:
        count+=1
        if (count>256):
            break
        instrlist=line.split()
        if instrlist==[]:
            return True
        while(instrlist[0][-1]==':'):
            u=instrlist[0][0:-1]
            if(u not in labellist):
                labellist.append(u)
            else:
                flag=0
                print(f"Line number {count} : Label '{u}' is already declared ")

            instrlist=instrlist[1::]
            if(instrlist==[]):
                break
    if(flag==0):
        return False
    return True

def check_halt(file):
    file.seek(0)
    k=file.read()
    k=k.strip()
    rt=k.split('\n')
    count=0
    for a in range(0,len(rt)):
        count=count+1
        if (count>256):
            return True
           
        rt[a]=rt[a].strip()
        x=rt[a].split()
        if(len(x)<1):
            continue
        if rt[a]=='hlt' or  (len(x)>1 and x[0][-1]==":" and x[1]=="hlt")  :
            idx=a 
            break
    else:
        idx=-1

    if idx==-1:
        t= f"Line number {len(rt)} : hlt is not the last instruction"
        print(t)
        return False
    else:
        if len(rt)>idx+1:
            t= f"Line number {idx+1} : Instructions detected after hlt"
            print(t)
            return False
    return True

def stupid_syntax(input):
    varlist=[]
    labellist=[]
    flag=0
    count_of_instruction=0
    file.seek(0)
    for line in file:
        if (count_of_instruction>256):
            break
        count_of_instruction+=1
        instrlist=line.split()
        if (instrlist==[]):
            return True
        if(instrlist[0]=="var"):
            if (len(instrlist)<2):
                continue
            varlist.append(instrlist[1])
        if(instrlist[0][-1]==":"):
            if (len(instrlist)<2):
                continue
            labellist.append(instrlist[0][0:len(instrlist[0])-1])
    input.seek(0)
    input= input.read()
    p=ascii_letters + "$" + " " + "\n" +"1234567890" + "\t" +"."
    y=input.split("\n")
    flag=0
    count_of_instruction=1
    for i in y:
        if (count_of_instruction>256):
            break
        i=i.split()
        if  i==[] or ":" == i[0][-1] or i[0]=="var":
            count_of_instruction+=1
            continue
        for j in i:
            if ((j in labellist) or (j in varlist)):
                continue
            for k in j:
                opi=0
                if(k not in p):
                    print(f"Line number {count_of_instruction} : General invalid syntax")
                    opi=1
                    flag=1
                    break
                if (opi==1):
                    break
        count_of_instruction+=1
    if flag==0:
        return True
    return False

def check_var(input):

    t=input.split("\n")
    flag=0

    count_of_instruction=1
    for line in t:
        if (count_of_instruction>256):
            break
        line=line.strip()
        line=line.split(" ")
        if line[0] == "var":
            if (len(line)>2):
                print(f"Line number {count_of_instruction} : var name can not contain spaces")
                
                flag=1
            elif len(line)==1:
                print(f"Line number {count_of_instruction} : var name not specified")
                flag=1
        count_of_instruction+=1
    if flag==0:
        return True 
    return False

def undefined_variable(file):
    varlist=[]
    labellist=[]
    flag=0
    count=0
    file.seek(0)
    for line in file:
        count+=1
        if (count>256):
            break
        instrlist=line.split()
        if (instrlist==[]):
            return True
        if(instrlist[0]=="var"):
            if (len(instrlist)<2):
                continue
            varlist.append(instrlist[1])
        if(instrlist[0][-1]==":"):
            if (len(instrlist)<2):
                continue
            labellist.append(instrlist[0][0:len(instrlist[0])-1])
    file.seek(0)
    count=0
    for line in file:
        count+=1
        if (count>256):
            break
        line=line.split()
        if(line[0]=="ld" or line[0]=="st"):
            if(line[-1] not in varlist):
                if (line[-1] in labellist):
                    print(f"Line number {count}: Misuse of label as variable")
                    flag=1
                else:
                    print(f"Line number {count}: Undefined variables")
                    flag=1
    if (flag==1):return False
    return True

def valid_register(inst, count_of_instruction):
    """
    Checks whether a register name is valid or not.
    """

    if(inst[0]=="var" or ":" in inst[0]):
        return True
    if(inst[0] not in instructions):
        return True
    if (inst[0] == "mov"):
        if "$" in inst[2]:
            type="B"
        else:
            return True
    else:
        type = Opcode[inst[0]][1]
    if type == "A":
        if(len(inst)!=4):
            return True
        reg=[inst[1],inst[2],inst[3]]
    elif type == "B" or type=="D":
        if(len(inst)!=2):
            return True
        reg=[inst[1]]
    elif type == "C":
        if(len(inst)!=3):
            return True
        reg=[inst[1],inst[2]]
    else:
        return True
    # print("reg- ",*reg)
    for i in reg:
        # print("i-",i)
        if not valid_reg_help(i):
            if i=="FLAGS":
                continue
            else:
                t=f"Line Number {count_of_instruction} : Invalid register name- {i} is not a valid register"
                print(t)
            return False
    # print("hjgkg")
    return True

def illegal_flag(inst, count_of_instruction):
    """
    Checks if an instruction is an illegal use of flag in the instruction
    """
    if "FLAGS" not in inst:
        return True
    else:
        if len(inst)==3 and (inst[1]=="FLAGS") and (inst[0]=="mov") and (inst[2] in register):
            return True
    rt=f"Line Number : {count_of_instruction} Invalid use of FLAGS in the instruction"
    print(rt)
    return False

def check_len(inst, count_of_instruction): 
    """
    Checks whether the length of the instruction is valid or not.
    """
    if (count_of_instruction>256):
            return True
    if(inst[0] not in instructions):
        return True
    if(inst[0]=="var" or ":" in inst[0]):
        return True
    if(inst[0]!="var" and ":" not in inst[0]):
        if inst[0]=='mov':
            if len(inst)==3:
                return True
        else:
            type = Opcode[inst[0]][1]
            if len(inst)==type_len[type]:

                return True
        u=f"Line Number {count_of_instruction} : The length of the instruction is not valid"
        print(u)
        return False 
def invalid_immediate(inst, count_of_instruction):
    if(inst[0] not in instructions):
        return True
    if(inst[0]=="var" or ":" in inst[0]):
        return True
    if (inst[0] == "mov"):
        if (inst[2][0] != "$"):
            return True
        else:
            type= "B"
    else:
        type = Opcode[inst[0]][1]
    if (type != "B"):
        return True
    num=inst[2][1::] 
    if (inst[2][0] != "$"):
        print("The declaration of an immediate requires a $ symbol before it")
        return False
    if inst[0] == "movf":
        return True
    try: # try except checks if the num is actually a number or not
        if 0<=int(num)<256 :
            return True
        y=f"Line Number {count_of_instruction} : The value of immediate must be a whole number<=255 and >=0 "
        print(y)
        return False 
    except:

        y=f"Line Number {count_of_instruction} : The value of immediate must be a whole number<=255 and >=0 "
        print(y)
        return False

def invalid_floating_immediate(inst, count_of_instruction):
    if(inst[0] not in instructions):
        return True
    if(inst[0]=="var" or ":" in inst[0]):
        return True
    if (inst[0] == "movf" or inst[0]=="mov"):
        if (inst[2][0] != "$"):
            return True
        else:
            type= "B"
    else:
        type = Opcode[inst[0]][1]
    if (type != "B"):
        return True
    num=inst[2][1::] 
    if (inst[2][0] != "$"):
        print("The declaration of an immediate requires a $ symbol before it")
        return False
    try: # try except checks if the num is actually a number or not
        if inst[0] == "mov":
            return True
        if 0<int(num)<=252 and inst[0] == "movf":
            return True
        y=f"Line Number {count_of_instruction} : The value of immediate must be in range of [1,252] "
        print(y)
        return False 
    except:
        if inst[0]!="movf":
            y=f"Line Number {count_of_instruction} : The value of immediate must be in range of [1,252]"
            print(y)
            return False

#check variable at front
def checkatfirst(file):
    count=0
    flag1=0
    file.seek(0)
    for line in file:
        count+=1
        if (count>256):
            break
        line=line.split()
        if line==[]:
            return True
        if line[0]!="var":
            break
    count=0
    for line in file:
        count=count+1
        if (count>256):
            break
        line=line.split()
        if(line==[]):
            continue
        if (line[0]=="var"):      # if (line[0]=="var" and flag==1 and line[0][-1]==""):
            flag1=1
            print(f"Line number {count} : Variable declaration is not at the starting")
    if(flag1==0):
        return True        
    return False

# undefined labels
def checklabels(file):
    labellist=[]
    count=0
    flag=0
    file.seek(0)
    for line in file:
        count+=1
        if (count>256):
            break
        instrlist=line.split()
        if instrlist==[]:
            return True
        if(instrlist[0][-1]==':'):
            labellist.append(instrlist[0][0:len(instrlist[0])-1])
    file.seek(0)
    count=0
    for line in file:
        count=count+1
        if (count>256):
            break
        line=line.split()
        if(line[0] in ["je","jmp","jlt","jgt"]):
            if(line[1] not in labellist):
                flag=1
                print(f"Line number {count} : Undefined Label")
                
    if(flag==0):
        return True
    return False

#misuse of variables as label 
def misuse_var_as_labels(file):
    varlist=[]
    flag=0
    count=0
    file.seek(0)
    for line in file:
        count+=1
        if (count>256):
            break
        instrlist=line.split()
        if len(instrlist)<2 :
            return True

        if(instrlist[0]=="var"):
            varlist.append(instrlist[1])
    file.seek(0)
    count=0
    for line in file:
        count=count+1
        if (count>256):
            break
        line=line.split()
        if (line[0]==":"):
            if(line[0][0:len(line[0])-1] in varlist): #checking name of label in list of variable
                print(f"Line number {count} : Misuse of Variable as label")
                flag=1
        # if line==[]:
        #     break
                
    if(flag==0):
        return True        
    return False


def ultimate_error_checker(file_object):
    # if our flag becomes False , we will stop executing
    f=file_object.read()
    flag=check_var(f) and undefined_variable(file_object)
    flag=checklabels(file_object) and flag
    flag=misuse_var_as_labels(file_object) and flag
    flag=checkatfirst(file_object) and flag
    flag=morelabels(file_object)  and flag
    flag=check_keyword(file_object)  and flag
    flag=stupid_syntax(file_object) and flag
    flag=check_halt(file_object) and flag

    count_of_instruction=1
    file_object.seek(0)
    for line in file_object:
        line=line.split()
        if(line==[]):
            continue
        flag=valid_instruction(line,count_of_instruction) and flag 
        flag=invalid_immediate(line,count_of_instruction) and flag
        flag=invalid_floating_immediate(line,count_of_instruction) and flag
        flag=valid_register(line,count_of_instruction) and flag 
        # print(flag)
        flag=illegal_flag(line,count_of_instruction)  and flag
        flag=check_len(line,count_of_instruction) and flag
        count_of_instruction+=1
        if (count_of_instruction>257):
            print("MEMORY LIMIT EXCEEDED")
            return False
    
    if flag==0:
        return False
    return True



def get_8bit_binary(bin):
    ans=''
    ans='0'*(8-len(bin))
    ans+=bin
    return ans

#for converting in 8 bit floating point format

def convert_fractional_number_into_binary(x):
    ans=""
    integer=int(x)
    fraction=(x)-integer 
    while(integer):
        help=integer%2
        ans+=str(help)
        integer//=2

    ans=ans[::-1]
    ans+="."
    x=5
    while(x):
        fraction*=2
        y=int(fraction)
        if(y==1):
            fraction-=y
            ans+="1"
        else:
            ans+="0"
        x-=1    
    return ans
def setting_in_format(x):
    cnt=-1
    ans=""
    for i in x:
        if(i=="."):
            break
        cnt+=1
        
    while(cnt):
        help=cnt%2
        ans+=str(help)
        cnt//=2
    
    while(len(ans)!=3):
        ans="0"+ans
    udit=""
    for i in range(len(x)):
        if(i==0 or x[i]=="."):
            continue
        else:
            udit=udit+x[i]
    udit=udit[0:5]
    return ans+udit
opcodes={"add":["10000","A"],"sub":["10001","A"],"mov_i":["10010","B"],"mov_r":["10011","C"],"ld":["10100","D"],"st":["10101","D"],"mul":["10110","A"],"div":["10111","C"],"rs":["11000","B"],"ls":["11001","B"],"xor":["11010","A"],"or":["11011","A"],"and":["11100","A"],"not":["11101","C"],"cmp":["11110","C"],"jmp":["11111","E"],"jlt":["01100","E"],"jgt":["01101","E"],"je":["01111","E"],"hlt":["01010","F"],"addf":["00000","A"],"subf":["00001","A"],"movf":["00010","B"]}
registers={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

file=open('input.txt','w')
import sys
file.write(sys.stdin.read())
file.close()
file=open("input.txt",'r')
file2=open("output.txt",'w')



ins_count=0 #will store the count  of valid instructions excluding invalid and vars

memory_to_data={} #maps memory address to instruction or 16 bit value
var_to_memory={} # maps all var names to some memory address
label_to_memory={} # maps all labels to some memory address


flag=ultimate_error_checker(file)
file.seek(0)
if(flag!=0):
    
    for line in file: #to count the no of valid instructions excluding invalid and vars
        line=line.strip() # to ignore trailing left white spaces

        ins_l=line.split()

        if len(ins_l)==0: #if line is empty ignore
            continue
        
        while ins_l[0][-1]==":":  # for label instructions eg- loop: add R1 R2 R3 
            ins_l.pop(0)
        
        if ins_l[0]=='mov':       # to handle move 
            if ins_l[2][0]=="$":
                ins_l[0]='mov_i'
            else:
                ins_l[0]='mov_r'

        if ins_l[0] in opcodes:
            ins_count+=1

    file.seek(0)

    curr_empty_memory=ins_count #stores the first empty memory after the last filled one in decimal format

    for line in file: # to map variables to memory adresses
        line=line.strip() # to ignore trailing left white spaces
        ins_l=line.split()
        
        if len(ins_l)==0: #if line is empty ignore
            continue
        
        while ins_l[0][-1]==":":  # for label instructions eg- loop: var X 
            ins_l.pop(0)

        if (ins_l[0]=="var"):
            var_to_memory[ins_l[1]]=get_8bit_binary(bin(curr_empty_memory)[2:]) 
            curr_empty_memory+=1

    file.seek(0) 


    curr=0
    for line in file: # to map memory adresses to instructions or 16 bit value 
        flag=0 # flag will be 1 whem label command comes
        
        
        line=line.strip() # to ignore trailing left white spaces
        ins_l=line.split()
        cloned_ins_l=ins_l.copy()

        if len(ins_l)==0: #if line is empty ignore
            continue
        
        label_key=[]
        while cloned_ins_l[0][-1]==":":  # for label instructions eg- loop: var X 
            ins_l.pop(0)
            
            flag=1
            label_key.append(cloned_ins_l[0][0:len(cloned_ins_l[0])-1]) # in this eg stores loop
            cloned_ins_l.pop(0)
        

        changed_line=' '.join(ins_l)
        if ins_l[0]=='mov':       # to handle move 
            if ins_l[2][0]=="$":
                ins_l[0]='mov_i'
            else:
                ins_l[0]='mov_r'

        if ins_l[0] in opcodes:
            temp=get_8bit_binary(bin(curr)[2:])  # stores memory address of this instruction
            memory_to_data[get_8bit_binary(bin(curr)[2:])]=changed_line
            curr+=1
            if flag==1:  # maps label to the corresponding memory
                for a in label_key:
                    label_to_memory[a]=temp
            
        
            
        elif (ins_l[0]=='var'):
            temp=var_to_memory[ins_l[1]]
            memory_to_data[var_to_memory[ins_l[1]]]=0 # all variables initialized to zero
            if flag==1:   # maps label to the corresponding memory
                for a in label_key:
                    label_to_memory[a]=temp
            

    file.seek(0)

    for line in file:  # main conversion
    

        line=line.strip() # to ignore trailing left white spaces
        ins_l=line.split()      # a single instruction splitted on the bases of space
        
        
        if len(ins_l)==0: #if line is empty ignore
            continue

        while ins_l[0][-1]==":":  # for label instructions eg- loop: var X 
            ins_l.pop(0)

        if ins_l[0]!="mov" and ins_l[0]!='var':
            opcode=opcodes[ins_l[0]][0]
            type=opcodes[ins_l[0]][1]
        elif ins_l[0]=='mov':
            if ins_l[2][0]=="$":
                opcode=opcodes["mov_i"][0]
                type=opcodes["mov_i"][1] 
            else:
                opcode=opcodes["mov_r"][0]
                type=opcodes["mov_r"][1] 
        
        # type handling seperately

        if type=='A': #eg- add R1 R2 R3
            ans=opcode+'00'+registers[ins_l[1]]+registers[ins_l[2]]+registers[ins_l[3]]

        elif type=="B": #eg- mov R1 $10 
            if(ins_l[0]=="movf"):
                ans=opcode+registers[ins_l[1]]+setting_in_format(convert_fractional_number_into_binary(float(ins_l[2][1:])))
            else:
                ans=opcode+registers[ins_l[1]]+get_8bit_binary(bin(int(ins_l[2][1:]))[2:])

        elif type=='C': #eg- mov R1 R2 ,  div R3 R4
            ans=opcode+"00000"+registers[ins_l[1]]+registers[ins_l[2]]

        elif type=='D': #eg- ld R1 X
            ans=opcode+ registers[ins_l[1]] + var_to_memory[ins_l[2]]

        elif type=='E': #eg- jgt X
            ans=opcode+ '000'+ label_to_memory[ins_l[1]]

        elif type=='F':  #eg- hlt
            ans=opcode+'00000000000'
        
        
        if ins_l[0]!='var':
            file2.write(ans+'\n')
    file2.close()
    file2=open('output.txt','r')
    
    print(file2.read().strip())

    file.close()
    file2.close()