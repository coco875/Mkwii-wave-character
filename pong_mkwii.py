import dolphin_memory_engine as dolphin_memory
from math import sin,degrees, radians

dolphin_memory.hook()

def lwz(a, b):
    i = hex(a+b)[2:]
    i = i[-8:]
    i = int(i, 16)
    return dolphin_memory.read_word(i)

def stw(a, b, c):
    dolphin_memory.write_word(a+b, c)

def lhz(a, b):
    v = hex(lwz(a, b))[2:]
    return int(v[:4], 16)

def ori(a, b):
    a = hex(a)[2:]
    b = hex(b)[2:]
    return int(a[:-len(b)]+b, 16)

def sth(a, b, c):
    dolphin_memory.write_word(a+b, c)


def get_ori_from_address(r):
    a = dolphin_memory.read_bytes(r+136, 12)
    x = int.from_bytes(a[:4], "big")
    y = int.from_bytes(a[4:8], "big")
    z = int.from_bytes(a[8:12], "big")
    # a = x.to_bytes(4, "big")+y.to_bytes(4, "big")+z.to_bytes(4, "big")
    # dolphin_memory.write_bytes(r+136, a)
    return a


def get_xyz_from_address(r):
    a = dolphin_memory.read_bytes(r, 12)
    x = int.from_bytes(a[:4], "big")
    y = int.from_bytes(a[4:8], "big")
    z = int.from_bytes(a[8:12], "big")
    #a = x.to_bytes(4, "big")+y.to_bytes(4, "big")+z.to_bytes(4, "big")
    #dolphin_memory.write_bytes(r, a)
    return x,y,z


def set_xyz_from_address(x,y,z,r):
    a = x.to_bytes(4, "big")+y.to_bytes(4, "big")+z.to_bytes(4, "big")
    dolphin_memory.write_bytes(r, a)


def set_ori_from_address(x, y, z, r):
    a = x.to_bytes(4, "big")+y.to_bytes(4, "big")+z.to_bytes(4, "big")
    dolphin_memory.write_bytes(r+136, a)


def get_address_memory_bot(num):
    r11 = 0x809c0000
    r3 = lwz(r11, 0x18f8)
    r9 = lwz(0x0020, r3)
    r0 = num*4
    r9 = lwz(r0, r9)
    r9 = lwz(0, r9)
    r9 = lwz(0x0008, r9)
    r9 = lwz(0x0090, r9)
    r9 = lwz(0x0004, r9)
    r9 = r9 + 104
    return r9


def get_address_memory_player():
    r11 = 0x809c0000
    r3 = lwz(r11, 0x18f8)
    r5 = lwz(r3, 0x0020)
    r5 = lwz(0, r5)
    r5 = lwz(0, r5)
    r5 = lwz(0x8, r5)
    r5 = lwz(0x90, r5)
    r5 = lwz(0x4, r5)
    r5 = r5 + 104
    return r5


print(hex(get_address_memory_player()))
print(get_xyz_from_address(get_address_memory_player()))
num = 0
while True:
    set_xyz_from_address(1150000000, 1200000000, 3000000000,
                         get_address_memory_player())
    set_ori_from_address(0, 0, 0, get_address_memory_player())
    dolphin_memory.write_word(get_address_memory_player()+0x10, 0)
    for i in range(1,12):
        set_xyz_from_address(1150000000+int(sin(radians(num+(i*70)))*5000000), 1200000000, 1140000000+((i-1)*5000000),
                            get_address_memory_bot(i))
        set_ori_from_address(0, 0, 0, get_address_memory_bot(i))
        dolphin_memory.write_word(get_address_memory_bot(i)+0x10, 0)
    num+=1
