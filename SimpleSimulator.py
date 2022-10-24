# import sys
# sys.stdout=open('file.txt','w')

from sys import  stdin 
flag25=0
flag_jmp=0
def NOT(s):
    t=''
    for i in s:
        if i=='0':
            t+='1'
        else:
            t+='0'
    return t
def get_8bit(bin):
    ans=''
    ans='0'*(8-len(bin))
    ans+=bin
    return ans

def get_16bit(bin):
    ans=''
    ans='0'*(16-len(bin))
    ans+=bin
    return ans

def get_3bit(bin):
    ans=''
    ans='0'*(3-len(bin))
    ans+=bin
    return ans
 
memory=['0'*16]*256
registers=['0'*16]*8
pc=0

# handle FLAGS function call

# Opcode={"00000":"add", "00001":"sub", "00010":"mov_i", "00011":"mov_r", 
# "00100":"ld", "00101":"st", "00110":"mul", "00111":"div", "01000":"rs", 
# "01001":"ls", "01010":"xor", "01011":"or", "01100":"and", "01101":"not", 
# "01110":"cmp", "01111":"jmp", "10000":"jlt", "10001":"jgt", "10010":"je",
#  "10011":"hlt"}

Opcode={"10000":"add", "10001":"sub", "10010":"mov_i", "10011":"mov_r", 
"10100":"ld", "10101":"st", "10110":"mul", "10111":"div", "11000":"rs", 
"11001":"ls", "11010":"xor", "11011":"or", "11100":"and", "11101":"not", 
"11110":"cmp", "11111":"jmp", "01100":"jlt", "01101":"jgt", "01111":"je",
 "01010":"hlt","00000":"addf","00001":"subf","00010":"movf"}

branch_list=["11111","01100","01101","01111"]

addr_to_register={"000":"R0", "001":"R1", "010":"R2", "011":"R3", 
"100":"R4", "101":"R5", "110":"R6", "111":"FLAGS"}

register_name_to_addr={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

register_addr_to_value={"000":0, "001":0, "010":0, "011":0, 
"100":0, "101":0, "110":0, "111":0} # 1-overflow 2-greater 3- equal 4- less

#god program
# for i in registers:
#     print("\"",registers[i],"\"",":","\"",i,"\"",sep='',end=", ")


def RF(reg_name):
    return (register_addr_to_value[register_name_to_addr[reg_name]])

input=stdin.read()
input=input.strip()
input=input.split("\n") #list of binaries
var_cnt=0
var_addr_max='00000000'
var_list=[]
for i in range(0,len(input)):
    memory[i]=input[i]  #stores instructions in memory
    instr=Opcode[input[i][0:5]]
    if instr=='ld' or instr=='st':
        var_list.append(input[i][8:])
        var_cnt=var_cnt+1
        if input[i][8:] >var_addr_max:
            var_addr_max=input[i][8:]  #max adress of variable in instructions

curr=len(input)
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
if (var_cnt>0):
    i=get_8bit(bin(curr)[2:]) 
    while (i!=var_addr_max):
    #    try:
            memory[curr]=0
            # print(memory[curr])
            curr=curr+1
            i=get_8bit(bin(curr)[2:])
            
    #    except:
    #         print(f'curr - {curr}')
    memory[curr]=0

#memory done

def execution_engine(type):
    global pc,flag25,flag_jmp
    instr=input[pc]

    if type=='add':
        register_addr_to_value[instr[13:]]=register_addr_to_value[instr[7:10]]+ register_addr_to_value[instr[10:13]]
        if register_addr_to_value[instr[13:]]>65535:
            register_addr_to_value[instr[13:]]%=65536
            register_addr_to_value['111']=1
            flag25=1
    elif type=='addf':
        register_addr_to_value[instr[13:]]=register_addr_to_value[instr[7:10]]+ register_addr_to_value[instr[10:13]]
        print(register_addr_to_value[instr[10:13]])
        print(register_addr_to_value[instr[7:10]])
        print(register_addr_to_value[instr[13:]])
        if  (register_addr_to_value[instr[13:]]>253):
            register_addr_to_value[instr[13:]]=255
            register_addr_to_value['111']=1
            flag25=1
    elif type=='sub':
        register_addr_to_value[instr[13:]]=register_addr_to_value[instr[7:10]] - register_addr_to_value[instr[10:13]]
        if register_addr_to_value[instr[13:]]<0:
            register_addr_to_value[instr[13:]]=0
            register_addr_to_value['111']=1
            flag25=1
    elif type=="subf":
        register_addr_to_value[instr[13:]]=register_addr_to_value[instr[7:10]] - register_addr_to_value[instr[10:13]]
        if register_addr_to_value[instr[13:]]<=0:
            register_addr_to_value[instr[13:]]=0
            register_addr_to_value['111']=1
            flag25=1
    elif type=='mov_i':
        register_addr_to_value[instr[5:8]]=int(instr[8:],2)
    elif type=='movf':
        # print(int(instr[8:],2))
        x=int(instr[8:11],2)
        x=2**x
        mantissa=instr[11:16]
        ans=0
        for i in range(1,6):
            ans=ans+((2**(-i))*(int(mantissa[i-1])))
        ans=ans+1
        print(ans*x)
        register_addr_to_value[instr[5:8]]=ans*x
    elif type=='mov_r': 

        if instr[10:13]=='111':
            # flag25=1
            var=register_addr_to_value['111']
            if (register_addr_to_value['111']==1):
                 var=int('0000000000001000',2)
            elif register_addr_to_value['111']==2:
                 var=int('0000000000000010',2)
            elif register_addr_to_value['111']==3:
                 var=int('0000000000000001',2)
            elif register_addr_to_value['111']==4:
                 var=int('0000000000000100',2)

            elif register_addr_to_value['111']==0:
                 var=int('0000000000000000',2)

            register_addr_to_value[instr[13:]]=var
        else:
            register_addr_to_value[instr[13:]] = register_addr_to_value[instr[10:13]]

    elif type=='ld':
         register_addr_to_value[instr[5:8]]=memory[int(instr[8:],2)]

    elif type=='st':
        memory[int(instr[8:],2)]=register_addr_to_value[instr[5:8]]

    elif type=='mul':
        register_addr_to_value[instr[13:]]=register_addr_to_value[instr[10:13]] * register_addr_to_value[instr[7:10]]
        #handle_flag(1)
        if register_addr_to_value[instr[13:]]>65535:
            register_addr_to_value[instr[13:]]%=65536
            register_addr_to_value['111']=1
            flag25=1

    elif type=='div':
        register_addr_to_value['000']= register_addr_to_value[instr[10:13]] // register_addr_to_value[instr[13:]]
        register_addr_to_value['001']= register_addr_to_value[instr[10:13]] % register_addr_to_value[instr[13:]]

    elif type=='rs':
        imm=int(instr[8:],2)
        while imm!=0:
            register_addr_to_value[instr[5:8]]=register_addr_to_value[instr[5:8]]//2
            imm-=1

    elif type=='ls':
        register_addr_to_value[instr[5:8]]*=(2**int(instr[8:],2))

    elif type=='xor':
        register_addr_to_value[instr[13:]]=register_addr_to_value[instr[10:13]] ^ register_addr_to_value[instr[7:10]]

    elif type=='or':
        register_addr_to_value[instr[13:]]=register_addr_to_value[instr[10:13]] | register_addr_to_value[instr[7:10]]
    
    elif type=='and':
        register_addr_to_value[instr[13:]]=register_addr_to_value[instr[10:13]] & register_addr_to_value[instr[7:10]]

    elif type=='not':
        register_addr_to_value[instr[13:]]= int(NOT(get_16bit(bin(register_addr_to_value[instr[10:13]])[2:])),2)
        
    elif type=='cmp':
        flag25=1
        #handle flag
        x=register_addr_to_value[instr[10:13]]-register_addr_to_value[instr[13:]]
        if x>0:
            register_addr_to_value['111']=2
        elif x==0:
            register_addr_to_value['111']=3
        elif x<0:
            register_addr_to_value['111']=4
            # print('u')

    elif type in ['jmp','jlt','jgt','je']:
        flag25=1
    #     if (instr[:5]=='01111'):
    #         register_addr_to_value['111']=0
    #     elif (instr[:5]=='10000'):
    #         if register_addr_to_value['111']==4:
    #             register_addr_to_value['111']=0
    #     elif (instr[:5]=='10001'):
    #         if register_addr_to_value['111']==2:
    #             register_addr_to_value['111']=0
    #     elif (instr[:5]=='10010'):
    #         if register_addr_to_value['111']==3:
    #            register_addr_to_value['111']=0
        


    

def update_pc(instr):
    global pc,flag_jmp 
    if (instr[:5]=='11111'):

        pc=int(instr[8:],2)
        # flag_jmp=1

    elif (instr[:5]=='01100'):
        if register_addr_to_value['111']==4:
            # flag_jmp=1
            pc=int(instr[8:],2)
        else:pc+=1

    elif (instr[:5]=='01101'):
        if register_addr_to_value['111']==2:
            # print('ud',end='')
            pc=int(instr[8:],2)
            # flag_jmp=1
        else:pc+=1

    elif (instr[:5]=='01111'):
        if register_addr_to_value['111']==3:
            pc=int(instr[8:],2)
            # flag_jmp=1
        else:pc+=1

    else:
        pc+=1

instr=input[0]
#while instr[:5]!='10011':
count=0
# flag_store=-1
while True:
    Type=Opcode[input[pc][0:5]]    
    execution_engine(Type)
    if flag25!=1:
        register_addr_to_value['111']=0
    
    print(get_8bit(bin(pc)[2:]),end=' ')
    for i in range(0,7):
        # print(register_addr_to_value[get_3bit(bin(i)[2:])])
        if float(register_addr_to_value[get_3bit(bin(i)[2:])])!=int(register_addr_to_value[get_3bit(bin(i)[2:])]):
            print("00000000"+setting_in_format(convert_fractional_number_into_binary(register_addr_to_value[get_3bit(bin(i)[2:])])),end=' ')
        else:
            register_addr_to_value[get_3bit(bin(i)[2:])]=int(register_addr_to_value[get_3bit(bin(i)[2:])])
            print(get_16bit(bin(register_addr_to_value[get_3bit(bin(i)[2:])])[2:]),end=' ')

    print('0'*12,end='')
    if count==1 and Type!='cmp':
        print('0000')
    elif (register_addr_to_value['111']==1):
        print('1000')
    elif register_addr_to_value['111']==2:
        print('0010')
    elif register_addr_to_value['111']==3:
        print('0001')
    elif register_addr_to_value['111']==4:
        print('0100')

    elif register_addr_to_value['111']==0:
        print('0000')

    if instr[:5]=='01010':
        break
    
    update_pc(instr)
    if count==1 and Type!='cmp':
        register_addr_to_value['111']=0
    flag25=0
    instr=input[pc]
    if Type=='cmp':
        count=1
    else:count=0

c=0
for i in memory:
    c=c+1
    if (type(i)==str):
        print(i)
    else:
        print(get_16bit(bin(i)[2:]))

# sys.stdout.close()