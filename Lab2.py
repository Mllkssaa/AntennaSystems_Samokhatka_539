import numpy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math

f = [400, 420, 440, 460, 480, 520, 540, 560, 580, 600, 620, 640, 630, 610, 600, 590, 580, 570, 560, 550, 540, 530, 520,
510, 500]
N = [6, 7, 8, 9, 12, 11, 10, 9, 8, 7, 6, 5, 12, 11, 10, 9, 8, 7, 6, 6, 7, 7, 8, 8, 9]

variant = 22
frequency = f[variant - 1]
number = N[variant - 1]

print(f"Варіант № {variant}")
print(f"Частота f = {frequency:.0f} МГц")
print(f"Число елементів антени N = {number}")

# розрахунок параметрів антени
wavelength = 299792458 / (frequency * 10**6)
d = 0.25 * wavelength
k = 2 * numpy.pi / wavelength

print(f"Довжина хвилі λ = {wavelength:.3f} м")
print(f"Відстань між елементами d = {d:.3f} м")
print(f"Хвильове число k = {k:.3f} рад/м")

# початкові масиви та змінні для розрахунку ДС
F1E = [1]
FH = [1]
FE = [1]
steps = [0]
SGP_H = 0
SGP_E = 0
level_H = 0
level_E = 0

max_x_H = []
max_y_H = []
max_x_E = []
max_y_E = []
min_x_H = []
min_y_H = []
min_x_E = []
min_y_E = []

# розрахунок нормованих діаграм спрямованості у площинах H та E
for theta in numpy.arange(0.01, numpy.pi / 2, 0.00001):
    F1 = abs(numpy.cos(numpy.pi / 2 * numpy.sin(theta)) / numpy.cos(theta))
    FH_value = abs(numpy.sin(number * k * d * (1 - numpy.cos(theta)) / 2) /
                   (number * numpy.sin(k * d * (1 - numpy.cos(theta)) / 2)))
    FE_value = F1 * FH_value

    F1E.append(F1)
    FH.append(FH_value)
    FE.append(FE_value)

    steps.append(math.degrees(theta))

# визначення ширини головної пелюстки на рівні 0,707
for i in range(len(FH) - 1):
    if FH[i] >= 0.707 and FH[i + 1] < 0.707:
        angle_H = steps[i] + (0.707 - FH[i]) * (steps[i + 1] - steps[i]) / (FH[i + 1] - FH[i])
        SGP_H = 2 * angle_H
        level_H = 0.707

    if FE[i] >= 0.707 and FE[i + 1] < 0.707:
        angle_E = steps[i] + (0.707 - FE[i]) * (steps[i + 1] - steps[i]) / (FE[i + 1] - FE[i])
        SGP_E = 2 * angle_E
        level_E = 0.707

# пошук максимумів та мінімумів ДС
for i in range(1, len(FH) - 1):
    if FH[i] > FH[i - 1] and FH[i] > FH[i + 1]:
        max_x_H.append(steps[i])
        max_y_H.append(FH[i])
    if FE[i] > FE[i - 1] and FE[i] > FE[i + 1]:
        max_x_E.append(steps[i])
        max_y_E.append(FE[i])

    if FH[i] < FH[i - 1] and FH[i] < FH[i + 1]:
        min_x_H.append(steps[i])
        min_y_H.append(FH[i])
    if FE[i] < FE[i - 1] and FE[i] < FE[i + 1]:
        min_x_E.append(steps[i])
        min_y_E.append(FE[i])

print("Ширина головної пелюстки в площині H = " + str(round(SGP_H, 2)) + '\u00b0')
print("Ширина головної пелюстки в площині E = " + str(round(SGP_E, 2)) + '\u00b0')

# виведення загальної таблиці результатів
lengths = [len(min_x_H), len(min_x_E), len(max_x_H), len(max_x_E)]
print("\nТаблиця. Аналіз ДС директорної антени в площинах H та E")
print("-------------------------------------------------------")
print("| № | 0min H | 0min E | 0max H | FH(0) | 0max E | FE(0) |")
for i in range(max(lengths)):
    v1 = f"{i + 1:2d}"
    v2 = f"{min_x_H[i]:7.2f}" if i < len(min_x_H) else "   -   "
    v3 = f"{min_x_E[i]:7.2f}" if i < len(min_x_E) else "   -   "
    v4 = f"{max_x_H[i]:7.2f}" if i < len(max_x_H) else "   -   "
    v5 = f"{max_y_H[i]:6.3f}" if i < len(max_y_H) else "  -   "
    v6 = f"{max_x_E[i]:7.2f}" if i < len(max_x_E) else "   -   "
    v7 = f"{max_y_E[i]:6.3f}" if i < len(max_y_E) else "  -   "
    print(f"|{v1}|{v2}|{v3}|{v4}|{v5}|{v6}|{v7}|")
print("-------------------------------------------------------")

# лінійний графік сформованих ДС
fig, ax = plt.subplots(figsize=(20 / 2.54, 12 / 2.54))
ax.plot(steps, F1E, linewidth=0.7, label="$F_{1E}(0)$")
ax.plot(steps, FH, linewidth=0.7, label="$F_H(0)$")
ax.plot(steps, FE, linewidth=0.7, label="$F_E(0)$")

if SGP_H:
    ax.plot(SGP_H / 2, level_H, "ro", markersize=4, label="Рівень 0,707 у площині H")
if SGP_E:
    ax.plot(SGP_E / 2, level_E, "go", markersize=4, label="Рівень 0,707 у площині E")

ax.plot(max_x_H, max_y_H, "o", markersize=4, color="black", label="Максимуми H")
ax.plot(max_x_E, max_y_E, "o", markersize=4, color="grey", label="Максимуми E")
ax.plot(min_x_H, min_y_H, "o", markersize=4, color="blue", label="Мінімуми H")
ax.plot(min_x_E, min_y_E, "o", markersize=4, color="purple", label="Мінімуми E")

ax.set_xlabel("θ, °", fontsize=10)
ax.set_ylabel("Нормована ДС", fontsize=10)
plt.xticks(numpy.arange(0, 91, 2), fontsize=7)
plt.yticks(numpy.arange(0, 1.1, 0.1), fontsize=7)
plt.ylim(-0.01, 1.01)
plt.xlim(0, 90)
plt.legend(loc="upper right", fontsize=7)
plt.grid(which="both", linestyle="--", linewidth=0.2, color="gray")
fig.savefig("ДС_лінійна_варіант_22.png", dpi=300)

# полярний(радіальний) графік ДС
fig2 = plt.figure(figsize=(20 / 2.54, 12 / 2.54))
ax2 = fig2.add_subplot(111, projection="polar")
theta_rad = numpy.radians(steps)
ax2.plot(theta_rad, FH, linewidth=0.8, color="blue", label="$F_H(θ)$")
ax2.plot(theta_rad, FE, linewidth=0.8, color="red", label="$F_E(θ)$")
ax2.plot(-theta_rad, FH, linewidth=0.8, color="blue", alpha=0.8)
ax2.plot(-theta_rad, FE, linewidth=0.8, color="red", alpha=0.8)

ax2.scatter(numpy.radians(max_x_H), max_y_H, color="black", s=18, label="Максимуми H")
ax2.scatter(numpy.radians(max_x_E), max_y_E, color="grey", s=18, label="Максимуми E")
ax2.set_theta_zero_location("N")
ax2.set_theta_direction(-1)
ax2.set_thetagrids(range(0, 360, 10))
ax2.set_title("Полярні діаграми спрямованості у площинах H та E", fontsize=12)
ax2.set_rlabel_position(90)
ax2.grid(True, linestyle="--", linewidth=0.3)
for label in ax2.get_xticklabels():
    label.set_fontsize(7)
ax2.legend(loc="lower left", fontsize=8)

fig2.savefig("ДС_полярна_варіант_22.png", dpi=300)
