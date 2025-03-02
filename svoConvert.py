import binascii
import os
import re

svoFileList = []
for i,j,k in os.walk("svo"):
    for t in k:
        svoFileList.append(f"svo/{t}")

for temp in svoFileList:
    with open(f'{temp}', 'rb') as f:
        hexData = f.read().hex()
        f.close()
    hexData = re.sub(r"(.{32})", "\\1\r\n", hexData)
    DDSposition = []
    for substr in re.finditer("444453", hexData):
        DDSposition.append(substr.span())
    tnum = 0
    DDSdata = []
    print(DDSposition)
    lastT = 0
    for t in DDSposition:
        if tnum == 0:
            tnum += 1
            lastT = t
            continue
        if tnum != (len(DDSposition)-1):
            DDS = hexData[lastT[0]-1:t[0]]
            DDSdata.append(DDS)
            lastT = t
        else:
            DDSdata.append(hexData[t[0]:len(hexData)])
            lastT = t
        tnum += 1
    tnum = 0
    for t in DDSdata:
        t = t.replace("\n","").replace("\r","")
        #print(t)
        #break
        with open(f'{temp.replace(".svo","").replace("svo","out")}-{tnum}.dds', 'wb') as file:
            binData = bytes.fromhex(t)
            file.write(binData)
            tnum += 1
            file.close()