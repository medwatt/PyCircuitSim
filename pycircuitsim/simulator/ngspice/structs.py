from ctypes import (
    Structure,
    c_double,
    c_char_p,
    c_int,
    c_short,
    c_bool,
    POINTER,
    c_void_p,
)


class ngcomplex(Structure):
    _fields_ = [("cx_real", c_double), ("cx_imag", c_double)]


class vector_info(Structure):
    _fields_ = [
        ("v_name", c_char_p),
        ("v_type", c_int),
        ("v_flags", c_short),
        ("v_realdata", POINTER(c_double)),
        ("v_compdata", POINTER(ngcomplex)),
        ("v_length", c_int),
    ]


class vecinfo(Structure):
    _fields_ = [
        ("number", c_int),
        ("vecname", c_char_p),
        ("is_real", c_bool),
        ("pdvec", c_void_p),
        ("pdvecscale", c_void_p),
    ]


class vecinfoall(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("title", c_char_p),
        ("date", c_char_p),
        ("type", c_char_p),
        ("veccount", c_int),
        ("vecs", POINTER(POINTER(vecinfo))),
    ]


class vecvalues(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("creal", c_double),
        ("cimag", c_double),
        ("is_scale", c_bool),
        ("is_complex", c_bool),
    ]


class vecvaluesall(Structure):
    _fields_ = [
        ("veccount", c_int),
        ("vecindex", c_int),
        ("vecsa", POINTER(POINTER(vecvalues))),
    ]
