import os
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Generate IV, K and K'
IV = get_random_bytes(16)
Kp = get_random_bytes(16)
K = get_random_bytes(16)

# Encrypt K with K'
cipher = AES.new(Kp)
K = cipher.encrypt(K)

with open('dataKM', 'wb') as fd:
    fd.write(Kp)
    line = '\n'
    fd.write(line.encode('utf-8'))
    fd.write(IV)

# Wait for node A to request K
originalTime = os.path.getmtime('dataKM')
notModified = True

while(notModified):
    if(os.path.getmtime('dataKM') > originalTime):
        with open('dataKM', 'wb') as fd:
            fd.write(K)
            notModified = False
    time.sleep(0.1)