import ctypes
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, "libdice.so")
proto_ed_lib = ctypes.CDLL(lib_path)

proto_ed_lib.init.argtypes = []
proto_ed_lib.init.restype = None
proto_ed_lib.roll.argtypes = (ctypes.c_uint8, ctypes.c_uint8)
proto_ed_lib.roll.restype = ctypes.c_uint16

proto_ed_lib.init()

def zig_roll(x, y):
    return proto_ed_lib.roll(x, y)


