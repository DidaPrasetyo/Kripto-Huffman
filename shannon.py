import re
import numpy as np
from PIL import Image
import collections
import time
import os

c = {}

# Membuat list yang sudah diurutkan

def create_list(message):
    list = dict(collections.Counter(message))
    list_sorted = sorted(iter(list.items()), key = lambda k_v:(k_v[1],k_v[0]),reverse=True)
    final_list = []
    for key,value in list_sorted:
        final_list.append([key,value,''])
    return final_list

# Membagi list lalu digabungkan menjadi tree

def divide_list(list):
    if len(list) == 2:
        # Menggabungkan jalur tree
        return [list[0]],[list[1]]
    else:
        n = 0
        for i in list:
            n+= i[1]
        x = 0
        distance = abs(2*x - n)
        j = 0
        # Membuat struktur shannon tree
        for i in range(len(list)):
            x += list[i][1]
            if distance < abs(2*x - n):
                j = i
    # Menggabungkan jalur tree
    return list[0:j+1], list[j+1:]

# Memasukkan value ke dalam tree

def label_list(list):
    list1,list2 = divide_list(list)
    for i in list1:
        i[2] += '0'
        c[i[0]] = i[2]
    for i in list2:
        i[2] += '1'
        c[i[0]] = i[2]
    if len(list1)==1 and len(list2)==1:
        return
    label_list(list2)
    return c

def main(file, conn):
    filename = os.path.splitext(file)[0]
    # Memulai kompresi
    msg = "Starting compress"+file
    conn.send(msg.encode())
    time.sleep(2)
    # Mengubah input menjadi array
    my_string = np.asarray(Image.open(file),np.uint8)
    sudhi = my_string
    shape = my_string.shape
    # Mengubah my_string menjadi list
    message = str(my_string.tolist())
    # Menyimpan hasil label_list ke dalam code
    code = label_list(create_list(message))
    # Membuat output biner, disimpan dalam txt
    output = open("compressed_"+filename+".txt","w+")
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

    # Membaca output
    intermediate = output.readlines()
    bitstring = ""
    for digit in intermediate:
        bitstring = bitstring + digit
    uncompressed_string =""
    code =""
    for digit in bitstring:
        code = code+digit
        pos=0
        # Decoding kode biner menjadi data original
        for letter in letter_binary:
            if code ==letter[1]:
                uncompressed_string=uncompressed_string+letter_binary[pos] [0]
                code=""
            pos+=1

    temp = re.findall(r'\d+', uncompressed_string)
    # Convert string ke integer
    res = list(map(int, temp))
    # Mengubah res ke dalam bentuk array
    res = np.array(res)
    # Mengubah tipe data array
    res = res.astype(np.uint8)
    # Memberikan bentuk baru pada array
    res = np.reshape(res, shape)
    msg = "Input image dimensions:"+str(shape)
    conn.send(msg.encode())
    time.sleep(2)
    msg = "Output image dimensions:"+str(res.shape)
    conn.send(msg.encode())
    time.sleep(2)
    # Mengkontruksi image dari arrayy
    data = Image.fromarray(res)
    # Menyimpan image
    data.save('compressed_'+file)
    # Pesan sukses
    if sudhi.all() == res.all():
        msg = "Success"
        conn.send(msg.encode())
    time.sleep(2)
    return "Done"