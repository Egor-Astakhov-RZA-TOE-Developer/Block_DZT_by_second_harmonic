import array
from typing import Any

import comtrade
import numpy as np

OMEGA = 50


def filter_second_harmonic_relative_to_first(rec: comtrade.Comtrade):
    i_a = rec.analog[0]
    i_b = rec.analog[1]
    i_c = rec.analog[2]
    t = rec.time

    second_harmonic_relative_values = array.array('f')
    for i in range(len(rec.time)):
        x = second_harmonic_filter(i_a[i], i_b[i], i_c[i], t[i]) / first_harmonic_filter(i_a[i], i_b[i],
                                                                                         i_c[i], t[i]) * 100
        second_harmonic_relative_values.append(x)

    return second_harmonic_relative_values


def second_harmonic_filter(i_a, i_b, i_c, t):
    i_a_cmlx: complex | Any = i_a * (np.cos(OMEGA * t) + 1j * np.sin(OMEGA * t))
    i_b_cmlx: complex | Any = i_b * (np.cos(OMEGA * t - 120 / 180 * np.pi) + 1j * np.sin(OMEGA * t - 120 / 180 * np.pi))
    i_c_cmlx: complex | Any = i_c * (np.cos(OMEGA * t + 120 / 180 * np.pi) + 1j * np.sin(OMEGA * t + 120 / 180 * np.pi))
    a = -0.5 + 1j * np.sqrt(3) / 2

    return complex.__abs__(1 / 3 * (i_a_cmlx + i_b_cmlx * np.pow(a, 2) + i_c_cmlx * a))


def first_harmonic_filter(i_a, i_b, i_c, t):
    i_a_cmlx: complex | Any = i_a * (np.cos(OMEGA * t) + 1j * np.sin(OMEGA * t))
    i_b_cmlx: complex | Any = i_b * (np.cos(OMEGA * t - 120 / 180 * np.pi) + 1j * np.sin(OMEGA * t - 120 / 180 * np.pi))
    i_c_cmlx: complex | Any = i_c * (np.cos(OMEGA * t + 120 / 180 * np.pi) + 1j * np.sin(OMEGA * t + 120 / 180 * np.pi))
    a = -0.5 + 1j * np.sqrt(3) / 2

    return complex.__abs__(1 / 3 * (i_a_cmlx + i_b_cmlx * a + i_c_cmlx * np.pow(a, 2)))


def digital_signal_block_DZT(second_harmonic_relative_values: array):
    second_harmonic_setpoint = 15
    res = array.array('i')
    for elem in second_harmonic_relative_values:
        if elem >= second_harmonic_setpoint: res.append(1)
        eles: res.append(0)

    return res
