import ctypes
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

lib_path = os.path.join(script_dir, "libproto-ed.so")

proto_ed_lib = ctypes.CDLL(lib_path)

proto_ed_lib.roll.argtypes = (ctypes.c_uint8, ctypes.c_uint8)
proto_ed_lib.roll.restype = ctypes.c_uint8

def roll(x, y):
    return proto_ed_lib.roll(x, y)


