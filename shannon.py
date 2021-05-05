import re
import numpy as np
from PIL import Image
import collections
import time
import os

c = {}
def create_list(message):
    list = dict(collections.Counter(message))
    list_sorted = sorted(iter(list.items()), key = lambda k_v:(k_v[1],k_v[0]),reverse=True)
    final_list = []
    for key,value in list_sorted:
        final_list.append([key,value,''])
    return final_list

def divide_list(list):
    if len(list) == 2:
        return [list[0]],[list[1]]
    else:
        n = 0
        for i in list:
            n+= i[1]
        x = 0
        distance = abs(2*x - n)
        j = 0
        for i in range(len(list)):
            x += list[i][1]
            if distance < abs(2*x - n):
                j = i
    return list[0:j+1], list[j+1:]


def label_list(list):
    list1,list2 = divide_list(list)
    for i in list1:
        i[2] += '0'
        c[i[0]] = i[2]
    for i in list2:
        i[2] += '1'
        c[i[0]] = i[2]
    if len(list1)==1 and len(list2)==1:        #assigning values to the tree
        return
    label_list(list2)
    return c

def main(file, conn):
    filename = os.path.splitext(file)[0]
    msg = "Starting compress"+file
    conn.send(msg.encode())
    time.sleep(2)
    my_string = np.asarray(Image.open(file),np.uint8)
    sudhi = my_string
    shape = my_string.shape

    message = str(my_string.tolist())

    code = label_list(create_list(message))

    output = open("compressed_"+filename+".txt","w+")          # generating output binary
    letter_binary = []
    for key, value in code.items():
        letter_binary.append([key,value])
    msg = "Compressed file generated as compressed_"+filename+".txt"
    conn.send(msg.encode())
    time.sleep(2)

    for a in message:
        for key, value in code.items():
            if key in a:
                output.write(value)
    output = open("compressed_"+filename+".txt","r")
    intermediate = output.readlines()
    bitstring = ""
    for digit in intermediate:
        bitstring = bitstring + digit
    uncompressed_string =""
    code =""
    for digit in bitstring:
        code = code+digit
        pos=0
        for letter in letter_binary:               # decoding the binary and genrating original data
            if code ==letter[1]:
                uncompressed_string=uncompressed_string+letter_binary[pos] [0]
                code=""
            pos+=1

    temp = re.findall(r'\d+', uncompressed_string)
    res = list(map(int, temp))
    res = np.array(res)
    res = res.astype(np.uint8)
    res = np.reshape(res, shape)
    msg = "Input image dimensions:"+str(shape)
    conn.send(msg.encode())
    msg = "Output image dimensions:"+str(res.shape)
    conn.send(msg.encode())
    time.sleep(2)
    data = Image.fromarray(res)
    data.save('uncompressed_'+file)
    if sudhi.all() == res.all():
        msg = "Success"
        conn.send(msg.encode())
    return "Done"

# main('100px.jpg')