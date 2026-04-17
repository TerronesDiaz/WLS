#!/usr/bin/env python3
"""
Recurso interactivo WLS (caso real de delivery).

- Compara OLS vs WLS en tiempo real.
- Permite ajustar pesos por zona (Z1..Z8).
- Permite variar la distancia objetivo y ver ETA estimada.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 13


def calcular_wls(x_data, y_data, w_data):
    """Retorna beta0 y beta1 para WLS."""
    sum_w = np.sum(w_data)
    sum_wx = np.sum(w_data * x_data)
    sum_wy = np.sum(w_data * y_data)
    sum_wx2 = np.sum(w_data * x_data**2)
    sum_wxy = np.sum(w_data * x_data * y_data)
    den = sum_w * sum_wx2 - sum_wx**2
    if abs(den) < 1e-12:
        return 0.0, 0.0
    beta1 = (sum_w * sum_wxy - sum_wx * sum_wy) / den
    beta0 = (sum_wy - beta1 * sum_wx) / sum_w
    return beta0, beta1


def calcular_ols(x_data, y_data):
    """OLS como caso particular con pesos iguales."""
    return calcular_wls(x_data, y_data, np.ones_like(x_data))


# Caso real: delivery por zonas (mas varianza en zonas menos estables)
x = np.array([2, 4, 6, 8, 10, 12, 14, 16], dtype=float)  # Distancia (km)
y = np.array([17, 24, 30, 36, 78, 47, 60, 66], dtype=float)  # ETA observado (min)
sigma2 = np.array([3, 3, 4, 6, 49, 12, 14, 16], dtype=float)  # Varianza por zona
w_original = 1 / sigma2


fig, ax = plt.subplots(figsize=(14, 9))
plt.subplots_adjust(left=0.08, bottom=0.38, right=0.95, top=0.90)

beta0_ols, beta1_ols = calcular_ols(x, y)
beta0_wls, beta1_wls = calcular_wls(x, y, w_original)

x_line = np.linspace(0, 17, 200)
y_ols = beta0_ols + beta1_ols * x_line
y_wls = beta0_wls + beta1_wls * x_line

sizes = 220 + 850 * (w_original / np.max(w_original))
colors = plt.cm.RdYlGn(1 - sigma2 / np.max(sigma2))
scatter = ax.scatter(
    x,
    y,
    s=sizes,
    c=colors,
    alpha=0.85,
    edgecolors='black',
    linewidth=2,
    zorder=5,
    label='Zonas (tamano segun peso)'
)

for i, (x_i, y_i) in enumerate(zip(x, y)):
    ax.annotate(
        f'Z{i+1}',
        (x_i, y_i),
        xytext=(6, 7),
        textcoords='offset points',
        fontsize=11,
        fontweight='bold'
    )

line_ols, = ax.plot(
    x_line, y_ols, 'r--', linewidth=3,
    label=f'OLS: y = {beta0_ols:.2f} + {beta1_ols:.2f}x', alpha=0.85
)
line_wls, = ax.plot(
    x_line, y_wls, 'g-', linewidth=3,
    label=f'WLS: y = {beta0_wls:.2f} + {beta1_wls:.2f}x'
)

distancia_inicial = 10.0
eta_ols = beta0_ols + beta1_ols * distancia_inicial
eta_wls = beta0_wls + beta1_wls * distancia_inicial
marker_ols, = ax.plot([distancia_inicial], [eta_ols], 'ro', markersize=8)
marker_wls, = ax.plot([distancia_inicial], [eta_wls], 'go', markersize=8)

ax.set_xlim(0, 17)
ax.set_ylim(10, 85)
ax.set_xlabel('Distancia del pedido (km)', fontsize=15, fontweight='bold')
ax.set_ylabel('Tiempo de entrega (min)', fontsize=15, fontweight='bold')
ax.set_title('WLS Interactivo 2 - Caso real de delivery', fontsize=18, fontweight='bold')
ax.grid(True, alpha=0.4)

info_text = ax.text(
    0.98,
    0.02,
    (f'Distancia objetivo: {distancia_inicial:.1f} km\n'
     f'ETA OLS: {eta_ols:.2f} min\n'
     f'ETA WLS: {eta_wls:.2f} min\n\n'
     f'Delta ETA (OLS-WLS): {eta_ols - eta_wls:.2f} min'),
    transform=ax.transAxes,
    fontsize=12,
    verticalalignment='bottom',
    horizontalalignment='right',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#f7f9f9',
              alpha=0.95, edgecolor='#34495e')
)
ax.legend(loc='upper left', fontsize=13, framealpha=0.95)

# Sliders de pesos
sliders = []
for i in range(8):
    row = i // 4
    col = i % 4
    ax_slider = plt.axes([0.10 + col * 0.22, 0.23 - row * 0.085, 0.18, 0.03])
    slider = Slider(
        ax_slider,
        f'Z{i+1}',
        0.01,
        0.60,
        valinit=w_original[i],
        valstep=0.01,
        color='#3498db',
        initcolor='none'
    )
    slider.label.set_fontsize(11)
    slider.valtext.set_fontsize(11)
    sliders.append(slider)

# Slider de distancia objetivo
ax_dist = plt.axes([0.10, 0.075, 0.62, 0.03])
slider_dist = Slider(
    ax_dist,
    'Distancia objetivo (km)',
    2.0,
    16.0,
    valinit=distancia_inicial,
    valstep=0.5,
    color='#8e44ad',
    initcolor='none'
)
slider_dist.label.set_fontsize(11)
slider_dist.valtext.set_fontsize(11)

# Botones
ax_reset = plt.axes([0.76, 0.02, 0.14, 0.05])
btn_reset = Button(ax_reset, 'Reset pesos', color='#e74c3c', hovercolor='#c0392b')
btn_reset.label.set_color('white')
btn_reset.label.set_fontweight('bold')
btn_reset.label.set_fontsize(12)

ax_destacar = plt.axes([0.76, 0.09, 0.14, 0.05])
btn_destacar = Button(ax_destacar, 'Destacar estables', color='#2ecc71', hovercolor='#27ae60')
btn_destacar.label.set_color('white')
btn_destacar.label.set_fontweight('bold')
btn_destacar.label.set_fontsize(12)


def update(_=None):
    w_actual = np.array([s.val for s in sliders])
    beta0_wls_new, beta1_wls_new = calcular_wls(x, y, w_actual)
    y_wls_new = beta0_wls_new + beta1_wls_new * x_line
    line_wls.set_ydata(y_wls_new)
    line_wls.set_label(f'WLS: y = {beta0_wls_new:.2f} + {beta1_wls_new:.2f}x')

    new_sizes = 220 + 850 * (w_actual / np.max(w_actual))
    scatter.set_sizes(new_sizes)

    d = slider_dist.val
    eta_ols_new = beta0_ols + beta1_ols * d
    eta_wls_new = beta0_wls_new + beta1_wls_new * d
    marker_ols.set_data([d], [eta_ols_new])
    marker_wls.set_data([d], [eta_wls_new])
    info_text.set_text(
        f'Distancia objetivo: {d:.1f} km\n'
        f'ETA OLS: {eta_ols_new:.2f} min\n'
        f'ETA WLS: {eta_wls_new:.2f} min\n\n'
        f'Delta ETA (OLS-WLS): {eta_ols_new - eta_wls_new:.2f} min'
    )

    ax.legend(loc='upper left', fontsize=13, framealpha=0.95)
    fig.canvas.draw_idle()


def reset_pesos(_):
    for i, slider in enumerate(sliders):
        slider.set_val(w_original[i])
    slider_dist.set_val(distancia_inicial)
    update()


def destacar_estables(_):
    pesos_demo = [0.55, 0.55, 0.45, 0.35, 0.05, 0.15, 0.12, 0.10]
    for i, slider in enumerate(sliders):
        slider.set_val(pesos_demo[i])
    update()


for slider in sliders:
    slider.on_changed(update)
slider_dist.on_changed(update)
btn_reset.on_clicked(reset_pesos)
btn_destacar.on_clicked(destacar_estables)

print("=" * 72)
print("WLS INTERACTIVO 2 - DELIVERY")
print("=" * 72)
print(f"OLS inicial: y = {beta0_ols:.4f} + {beta1_ols:.4f}x")
print(f"WLS inicial: y = {beta0_wls:.4f} + {beta1_wls:.4f}x")
print("Usa sliders Z1..Z8 para cambiar pesos y distancia objetivo.")
print("=" * 72)

plt.show()
