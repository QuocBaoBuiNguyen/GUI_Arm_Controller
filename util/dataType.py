from ctypes import (
    Union, Array,
    c_uint8, c_uint32,
    c_float,
    cdll, CDLL
)

class uint8_array(Array):
    _type_ = c_uint8
    _length_ = 4

class arrayFloat(Union):
    _fields_ = ("float_num", c_float), ("float_arr", uint8_array)
