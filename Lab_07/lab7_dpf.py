"""
Лабораторна робота №7
Тема: Дискретне перетворення Фур'є (ДПФ)

Програма:
1. Формує модельний дискретний сигнал.
2. Обчислює пряме ДПФ.
3. Будує амплітудний і фазовий спектри.
4. Виконує обернене ДПФ.
5. Перевіряє точність відновлення та зберігає графіки.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- Налаштування ---
N = 1000
n = np.arange(N)
OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Модельний сигнал з прикладу методички ---
# x[n] = 3*sin(n/5) + 3*sin(n/6)
x = 3 * np.sin(n / 5) + 3 * np.sin(n / 6)

# --- Пряме дискретне перетворення Фур'є ---
# X[k] містить комплексні спектральні коефіцієнти сигналу.
X = np.fft.fft(x)
freq = np.arange(N)

# --- Амплітудний і фазовий спектри ---
# Модуль комплексних коефіцієнтів — амплітудний спектр.
amplitude = np.abs(X)
# Аргумент комплексних коефіцієнтів — фазовий спектр у радіанах.
phase = np.angle(X)

# --- Обернене дискретне перетворення Фур'є ---
# Після оберненого ДПФ має бути відновлено початковий сигнал.
x_reconstructed = np.fft.ifft(X).real

# --- Перевірка точності відновлення ---
max_error = np.max(np.abs(x - x_reconstructed))
print(f"Кількість відліків N: {N}")
print(f"Максимальна абсолютна похибка відновлення: {max_error:.12e}")

# --- Рисунок 1: початковий сигнал ---
plt.figure(figsize=(12, 4))
plt.plot(n, x)
plt.title("Рис. 1. Графічний вираз функції")
plt.xlabel("n")
plt.ylabel("Амплітуда")
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "figure1_signal.png", dpi=150)
plt.close()

# --- Рисунок 2: фазовий спектр ---
plt.figure(figsize=(12, 4))
plt.plot(freq, phase)
plt.title("Рис. 2. Графік фази ДПФ")
plt.xlabel("k")
plt.ylabel("Фаза, рад")
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "figure2_phase.png", dpi=150)
plt.close()

# --- Рисунок 3: амплітудний спектр ---
# Логарифмічна шкала допомагає бачити як великі, так і малі значення.
plt.figure(figsize=(12, 4))
plt.semilogy(freq, np.maximum(amplitude, 1e-12))
plt.title("Рис. 3. Графік амплітуди ДПФ (логарифмічна шкала)")
plt.xlabel("k")
plt.ylabel("|X[k]|")
plt.grid(True, which="both")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "figure3_amplitude.png", dpi=150)
plt.close()

# --- Рисунок 4: порівняння сигналу та результату оберненого ДПФ ---
plt.figure(figsize=(12, 4))
plt.plot(n, x, label="Початковий сигнал", linewidth=1.5)
plt.plot(n, x_reconstructed, "--", label="Відновлений сигнал", linewidth=1)
plt.title("Рис. 4. Обернене перетворення Фур'є")
plt.xlabel("n")
plt.ylabel("Амплітуда")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "figure4_inverse.png", dpi=150)
plt.close()

# --- Загальний рисунок із чотирма графіками ---
fig, axes = plt.subplots(4, 1, figsize=(12, 12))
axes[0].plot(n, x)
axes[0].set_title("Рис. 1. Графічний вираз функції")
axes[0].set_xlabel("n")
axes[0].set_ylabel("Амплітуда")
axes[0].grid(True)

axes[1].plot(freq, phase)
axes[1].set_title("Рис. 2. Графік фази ДПФ")
axes[1].set_xlabel("k")
axes[1].set_ylabel("Фаза, рад")
axes[1].grid(True)

axes[2].semilogy(freq, np.maximum(amplitude, 1e-12))
axes[2].set_title("Рис. 3. Графік амплітуди ДПФ")
axes[2].set_xlabel("k")
axes[2].set_ylabel("|X[k]|")
axes[2].grid(True, which="both")

axes[3].plot(n, x, label="Початковий сигнал")
axes[3].plot(n, x_reconstructed, "--", label="Відновлений сигнал")
axes[3].set_title("Рис. 4. Обернене перетворення")
axes[3].set_xlabel("n")
axes[3].set_ylabel("Амплітуда")
axes[3].grid(True)
axes[3].legend()

fig.tight_layout()
fig.savefig(OUTPUT_DIR / "all_figures.png", dpi=150)
plt.show()
