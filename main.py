import comtrade
import matplotlib.pyplot as plt

from SecondHarmonicFilter import filter_second_harmonic_relative_to_first, digital_signal_block_DZT
# парсинг comtrade-файла
name = "comtrade1"
cfg = "Comtrades\\" + name + ".cfg"
dat = "Comtrades\\" + name + ".dat"
rec = comtrade.load(cfg, dat)

print("Trigger time = {}s".format(rec.trigger_time))

# Значение второй гармоники относительно первой в сигнале
res = filter_second_harmonic_relative_to_first(rec)

# Логический сигнал срабатывания блокировки ДЗТ по уровню 2 гармоники
digit_signal_block_DZT = digital_signal_block_DZT(res)

# Построение графиков
plt.subplot(3, 1, 1)

plt.plot(rec.time, rec.analog[0])
plt.plot(rec.time, rec.analog[1])
plt.plot(rec.time, rec.analog[2])
plt.legend([rec.analog_channel_ids[0], rec.analog_channel_ids[1], rec.analog_channel_ids[2]])
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(rec.time, res)
plt.legend(["Уровень 2 гармоники"])
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(rec.time, digit_signal_block_DZT)
plt.legend(["Сигнал на блокировку ДЗТ по 2 гармонике"])
plt.grid(True)
plt.show()
