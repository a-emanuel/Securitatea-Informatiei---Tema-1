import os
import time
from Crypto.Cipher import AES

# Get IV and K'
with open('dataKM', 'rb') as fd:
    data = fd.read()
    
line = '\n'   
Kp, IV = data.split(line.encode('utf-8'), 1) 

# Get operation mode from A
originalTime = os.path.getmtime('dataAB')
notModified = True
while(notModified):
    if(os.path.getmtime('dataAB') > originalTime):
        with open('dataAB', 'r') as fd:
            opMode = fd.read()
            notModified = False
    time.sleep(0.1)

# Get encrypted K from A
originalTime = os.path.getmtime('dataAB')
notModified = True
while(notModified):
    if(os.path.getmtime('dataAB') > originalTime):
        with open('dataAB', 'rb') as fd:
            K = fd.read()
            notModified = False
    time.sleep(0.1)

cipher = AES.new(Kp)
K = cipher.decrypt(K)

# Send node A confirmation
with open('dataAB', 'w') as fd:
    fd.write('We good')

# Wait for encrypted message
originalTime = os.path.getmtime('dataAB')
notModified = True
while(notModified):
    if(os.path.getmtime('dataAB') > originalTime):
        with open('dataAB', 'rb') as fd:
            encryptedData = fd.read()
            notModified = False
    time.sleep(0.5)

print(encryptedData)
# Decrypt data
cipher = AES.new(K)

if int(opMode) == 1:
    #ECB
    print()
else:
    #CDC
    print()
    