import array
from typing import Any

import comtrade
import numpy as np

# Пример сигнала: смесь синусоиды 50 Гц и 100 Гц
fs = 1000  # Частота дискретизации (Гц)


def filter_second_harmonic_relative_to_first(rec: comtrade.Comtrade):
    i_a = rec.analog[0]
    i_b = rec.analog[1]
    i_c = rec.analog[2]
    t = rec.time

    i_a_2 = second_harmonnic_filter(i_a)
    i_b_2 = second_harmonnic_filter(i_b)
    i_c_2 = second_harmonnic_filter(i_c)

    i_a_1 = first_harmonnic_filter(i_a)
    i_b_1 = first_harmonnic_filter(i_b)
    i_c_1 = first_harmonnic_filter(i_c)

    i_a_2_rms = RMS_calculator(i_a_2)
    i_b_2_rms = RMS_calculator(i_b_2)
    i_c_2_rms = RMS_calculator(i_c_2)

    i_a_1_rms = RMS_calculator(i_a_1)
    i_b_1_rms = RMS_calculator(i_b_1)
    i_c_1_rms = RMS_calculator(i_c_1)

    a = relative_harmonic_value(i_a_1_rms, i_a_2_rms)
    b = relative_harmonic_value(i_b_1_rms, i_b_2_rms)
    c = relative_harmonic_value(i_c_1_rms, i_c_2_rms)

    return a, b, c


def relative_harmonic_value(first_harmonic, second_harmonic):
    second_harmonic_relative_values = array.array('f')

    for i in range(len(second_harmonic)):
        if first_harmonic[i] != 0:
            x = second_harmonic[i] / first_harmonic[i] * 100
        elif first_harmonic[i] == 0 and second_harmonic[i] == 0:
            x = 0
        else:
            x = 100

        second_harmonic_relative_values.append(x)

    return second_harmonic_relative_values


# Выделение гармоник для сигнала

def second_harmonnic_filter(mass: array.array):
    result = array.array('f')
    N = 20
    target_freq = 100
    buffer_mass = [0] * N
    for i in range(len(mass)):
        buffer_mass[19] = mass[i]
        fft_result = np.fft.fft(buffer_mass)
        fft_freqs = np.fft.fftfreq(len(buffer_mass), 1 / fs)

        idx = np.argmin(np.abs(fft_freqs - target_freq))
        harmonic_amplitude = np.abs(fft_result[idx])
        if harmonic_amplitude >= 0.1:
            result.append(harmonic_amplitude)
        else:
            result.append(0)

        # смещение всех точек массива на одно положение влево
        for i in range(len(buffer_mass) - 1):
            buffer_mass[i] = buffer_mass[i + 1]

    return result


def first_harmonnic_filter(mass: array.array):
    result = array.array('f')
    N = 20
    target_freq = 50
    buffer_mass = [0] * N
    for i in range(len(mass)):
        buffer_mass[19] = mass[i]
        fft_result = np.fft.fft(buffer_mass)
        fft_freqs = np.fft.fftfreq(len(buffer_mass), 1 / fs)

        idx = np.argmin(np.abs(fft_freqs - target_freq))
        harmonic_amplitude = np.abs(fft_result[idx])
        result.append(harmonic_amplitude)

        # смещение всех точек массива на одно положение влево
        for i in range(len(buffer_mass) - 1):
            buffer_mass[i] = buffer_mass[i + 1]

    return result


def digital_signal_block_DZT(a: array, b: array, c: array):

    second_harmonic_setpoint = 15
    res = array.array('i')
    for i in range(len(a)):
        if a[i] >= second_harmonic_setpoint or b[i] >= second_harmonic_setpoint or c[i] >= second_harmonic_setpoint:
            res.append(1)
        else:
            res.append(0)

    return res

def RMS_calculator(mass: array):
    result = array.array('f')
    N = 20
    buffer_mass = [0] * N
    for i in range(len(mass)):
        buffer_mass[19] = mass[i]

        square_summ = 0
        for i in range(len(buffer_mass)):
            square_summ += np.power(buffer_mass[i], 2)

        rms = np.sqrt(square_summ/N)

        result.append(rms)

        # смещение всех точек массива на одно положение влево
        for i in range(len(buffer_mass) - 1):
            buffer_mass[i] = buffer_mass[i + 1]

    return result