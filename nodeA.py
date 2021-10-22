import os
import time
from Crypto.Cipher import AES

# Get IV and K'
with open('dataKM', 'rb') as fd:
    data = fd.read()
    
line = '\n'   
Kp, IV = data.split(line.encode('utf-8'), 1) 

# Send node B operation mode: ECB/CBC
print('''Alege modul de operare
1) ECB
2) CBC''')
opMode = input('Mod: ')

with open('dataAB', 'w') as fd:
    fd.write(opMode)

# Get K from node KM
with open('dataKM', 'w') as fd:
    fd.write('Gimme key')

originalTime = os.path.getmtime('dataKM')
notModified = True
while(notModified):
    if(os.path.getmtime('dataKM') > originalTime):
        with open('dataKM', 'rb') as fd:
            K = fd.read()
            notModified = False
    time.sleep(0.1)

# Send node B encrypted K
with open('dataAB', 'wb') as fd:
    fd.write(K)

cipher = AES.new(Kp)
K = cipher.decrypt(K)

# Wait for confirmation from node B
originalTime = os.path.getmtime('dataAB')
notModified = True
while(notModified):
    if(os.path.getmtime('dataAB') > originalTime):
        with open('dataAB', 'r') as fd:
            fd.read()
            notModified = False
    time.sleep(0.1)

# Get and process the message
with open('text.txt', 'r') as fd:
    text = fd.read()

data = []
for c in text:
    bits = bin(ord(c))[2:]
    bits = '00000000'[len(bits):] + bits
    data.extend([int(b) for b in bits])

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

data = list(chunks(data, 128))

if len(data[-1]) < 128: 
    temp = []
    for i in range(128-len(data[-1])):
        temp.append(0)
    
    for i in data[-1]:
        temp.append(i)
    
    data[-1] = temp

blocks = []
for i in data:
    bytes = ''.join([str(bit) for bit in i])
    blocks.append(bytes)

# Encrypt the message
cipher = AES.new(K)

if int(opMode) == 1:
    #ECB
    encryptedData = []
    for block in blocks:
        encryptedBlock = cipher.encrypt(block)
        encryptedData.append(encryptedBlock)
else:
    #CDC
    encryptedData = []
    encryptedBlock = blocks[0] ^ IV
    encryptedData.append(encryptedBlock)
    for i in range(1, len(blocks)):
        blocks[i] = blocks[i] ^ blocks[i-1]
        encryptedBlock = cipher.encrypt(blocks[i])
        encryptedData.append(encryptedBlock)
        print(encryptedBlock)

# Send the message to node B
with open('dataAB', 'wb') as fd:
    for block in encryptedData:
        fd.write(block)
