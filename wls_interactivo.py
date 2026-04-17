#!/usr/bin/env python3
"""
================================================================================
RECURSO INTERACTIVO: Minimos Cuadrados Ponderados (WLS) vs OLS
Autor: Francisco Terrones
Proyecto: Metodos de Minimos Cuadrados Ponderados
================================================================================

Este script crea una visualizacion interactiva que permite:
- Comparar OLS (Minimos Cuadrados Ordinarios) vs WLS (Ponderados)
- Ajustar los pesos de cada dato con sliders
- Observar como la recta WLS cambia segun los pesos
- Demostrar el concepto de heterocedasticidad

REQUISITOS:
    pip install numpy matplotlib

USO:
    python wls_interactivo.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# ==============================================================================
# CONFIGURACION DE ESTILO
# ==============================================================================
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 13

# ==============================================================================
# DATOS DE EJEMPLO: Sensores de temperatura con diferente precision
# ==============================================================================
# x = tiempo (horas)
# y = temperatura (°C)
# Cada sensor tiene una varianza diferente (precision distinta)

x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
# Sensores 4 y 5 (alta varianza) muestran mediciones mas ruidosas
y = np.array([20.5, 21.8, 23.2, 26.8, 22.9, 27.3, 28.9, 30.2])

# Varianzas de cada sensor:
# - Sensores 1, 2, 3: Muy precisos (baja varianza)
# - Sensores 4, 5: Poco precisos (alta varianza)  
# - Sensores 6, 7, 8: Precision media
sigma2_original = np.array([0.5, 0.3, 0.4, 5.0, 4.0, 1.5, 1.2, 0.8])

# Pesos = 1/varianza (formula clave de WLS)
w_original = 1 / sigma2_original

# ==============================================================================
# FUNCIONES MATEMATICAS
# ==============================================================================

def calcular_wls(x, y, w):
    """
    Calcula los coeficientes beta0 (intercepto) y beta1 (pendiente) 
    para Minimos Cuadrados Ponderados (WLS).
    
    Formula de los estimadores WLS:
        beta1 = [Σw * Σwxy - Σwx * Σwy] / [Σw * Σwx² - (Σwx)²]
        beta0 = [Σwy - beta1 * Σwx] / Σw
    
    Parametros:
        x: array de valores independientes
        y: array de valores dependientes
        w: array de pesos (w_i = 1/sigma_i²)
    
    Retorna:
        beta0, beta1: coeficientes de la recta y = beta0 + beta1*x
    """
    sum_w = np.sum(w)
    sum_wx = np.sum(w * x)
    sum_wy = np.sum(w * y)
    sum_wx2 = np.sum(w * x**2)
    sum_wxy = np.sum(w * x * y)
    
    denominador = sum_w * sum_wx2 - sum_wx**2
    
    if abs(denominador) < 1e-10:
        return 0, 0
    
    beta1 = (sum_w * sum_wxy - sum_wx * sum_wy) / denominador
    beta0 = (sum_wy - beta1 * sum_wx) / sum_w
    
    return beta0, beta1


def calcular_ols(x, y):
    """
    Calcula OLS (Minimos Cuadrados Ordinarios).
    OLS es un caso especial de WLS donde todos los pesos = 1.
    """
    return calcular_wls(x, y, np.ones_like(x))


# ==============================================================================
# CREAR FIGURA PRINCIPAL
# ==============================================================================
fig, ax = plt.subplots(figsize=(14, 9))
plt.subplots_adjust(left=0.08, bottom=0.34, right=0.95, top=0.90)

# Calcular rectas iniciales
beta0_ols, beta1_ols = calcular_ols(x, y)
beta0_wls, beta1_wls = calcular_wls(x, y, w_original)

# Rango para graficar las rectas
x_line = np.linspace(0, 9, 100)
y_ols = beta0_ols + beta1_ols * x_line
y_wls = beta0_wls + beta1_wls * x_line

# Graficar puntos con tamaño proporcional al peso
# Los puntos con mayor peso se ven mas grandes
sizes = 150 + 600 * (w_original / np.max(w_original))
colors = plt.cm.RdYlGn(1 - sigma2_original / np.max(sigma2_original))
scatter = ax.scatter(x, y, s=sizes, c=colors, alpha=0.8, 
                     edgecolors='black', linewidth=2, zorder=5, 
                     label='Datos (tamano proporcional al peso)')

# Etiquetas de cada sensor para relacionar puntos con sliders
for i, (x_i, y_i) in enumerate(zip(x, y)):
    ax.annotate(f'S{i+1}', (x_i, y_i), xytext=(8, 8), textcoords='offset points',
                fontsize=11, fontweight='bold', color='#2c3e50',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          alpha=0.75, edgecolor='none'))

# Graficar rectas
line_ols, = ax.plot(x_line, y_ols, 'r--', linewidth=3, 
                    label=f'OLS: y = {beta0_ols:.2f} + {beta1_ols:.2f}x', alpha=0.8)
line_wls, = ax.plot(x_line, y_wls, 'g-', linewidth=3, 
                    label=f'WLS: y = {beta0_wls:.2f} + {beta1_wls:.2f}x')

# Configuracion del grafico principal
ax.set_xlim(0, 9)
ax.set_ylim(18, 33)
ax.set_xlabel('Tiempo (horas)', fontsize=15, fontweight='bold')
ax.set_ylabel('Temperatura (°C)', fontsize=15, fontweight='bold')
ax.set_title('Minimos Cuadrados Ponderados (WLS) vs OLS\nRecurso Interactivo', 
             fontsize=18, fontweight='bold', pad=15)
ax.legend(loc='upper left', fontsize=13, framealpha=0.95)
ax.grid(True, alpha=0.4)

# ==============================================================================
# CREAR SLIDERS INTERACTIVOS (8 sliders, uno por cada punto)
# ==============================================================================
sliders = []
ax_sliders = []

for i in range(8):
    # Posicion de cada slider
    row = i // 4
    col = i % 4
    ax_slider = plt.axes([0.10 + col * 0.22, 0.18 - row * 0.09, 0.18, 0.035])
    
    slider = Slider(ax_slider, f'S{i+1}', 0.1, 10.0, 
                    valinit=w_original[i], valstep=0.1,
                    color='#3498db', initcolor='none')
    slider.label.set_fontsize(11)
    slider.valtext.set_fontsize(11)
    sliders.append(slider)
    ax_sliders.append(ax_slider)

# ==============================================================================
# BOTONES DE CONTROL
# ==============================================================================
ax_reset = plt.axes([0.12, 0.02, 0.14, 0.055])
ax_igualar = plt.axes([0.30, 0.02, 0.16, 0.055])
ax_destacar = plt.axes([0.50, 0.02, 0.18, 0.055])
ax_original = plt.axes([0.72, 0.02, 0.16, 0.055])

btn_reset = Button(ax_reset, 'REINICIAR', color='#e74c3c', hovercolor='#c0392b')
btn_reset.label.set_color('white')
btn_reset.label.set_fontweight('bold')
btn_reset.label.set_fontsize(12)

btn_igualar = Button(ax_igualar, 'Todos = 1 (OLS)', color='#3498db', hovercolor='#2980b9')
btn_igualar.label.set_color('white')
btn_igualar.label.set_fontweight('bold')
btn_igualar.label.set_fontsize(12)

btn_destacar = Button(ax_destacar, 'Destacar Precisos', color='#2ecc71', hovercolor='#27ae60')
btn_destacar.label.set_color('white')
btn_destacar.label.set_fontweight('bold')
btn_destacar.label.set_fontsize(12)

btn_original = Button(ax_original, 'Valores Originales', color='#9b59b6', hovercolor='#8e44ad')
btn_original.label.set_color('white')
btn_original.label.set_fontweight('bold')
btn_original.label.set_fontsize(12)

# ==============================================================================
# FUNCION DE ACTUALIZACION (se llama cuando se mueve un slider)
# ==============================================================================
def update(val=None):
    """Actualiza la grafica cuando cambian los pesos."""
    # Obtener pesos actuales
    w_current = np.array([s.val for s in sliders])
    
    # Recalcular WLS con los nuevos pesos
    beta0_wls_new, beta1_wls_new = calcular_wls(x, y, w_current)
    y_wls_new = beta0_wls_new + beta1_wls_new * x_line
    
    # Actualizar linea WLS
    line_wls.set_ydata(y_wls_new)
    line_wls.set_label(f'WLS: y = {beta0_wls_new:.2f} + {beta1_wls_new:.2f}x')
    
    # Actualizar tamaños de puntos segun pesos
    new_sizes = 150 + 600 * (w_current / np.max(w_current))
    scatter.set_sizes(new_sizes)
    
    # Actualizar leyenda
    ax.legend(loc='upper left', fontsize=13, framealpha=0.95)
    fig.canvas.draw_idle()

# Conectar sliders a la funcion de actualizacion
for slider in sliders:
    slider.on_changed(update)

# ==============================================================================
# FUNCIONES DE LOS BOTONES
# ==============================================================================
def reset_weights(event):
    """Restablecer todos los pesos a 1."""
    for slider in sliders:
        slider.set_val(1.0)
    update()

def igualar_pesos(event):
    """Todos los pesos = 1 (equivalente a OLS puro)."""
    for slider in sliders:
        slider.set_val(1.0)
    update()

def destacar_precisos(event):
    """
    Configuracion que destaca los datos precisos.
    Los sensores 1,2,3 (precisos) tienen peso alto.
    Los sensores 4,5 (imprecisos) tienen peso bajo.
    """
    pesos_destacados = [8.0, 8.0, 8.0, 0.5, 0.5, 4.0, 4.0, 4.0]
    for i, slider in enumerate(sliders):
        slider.set_val(pesos_destacados[i])
    update()

def valores_originales(event):
    """Volver a los valores originales del ejemplo."""
    for i, slider in enumerate(sliders):
        slider.set_val(w_original[i])
    update()

btn_reset.on_clicked(reset_weights)
btn_igualar.on_clicked(igualar_pesos)
btn_destacar.on_clicked(destacar_precisos)
btn_original.on_clicked(valores_originales)

# ==============================================================================
# PANEL INFORMATIVO
# ==============================================================================
info_text = (
    "DATOS DEL EJEMPLO:\n"
    "  Sensores 1,2,3: Muy precisos (baja varianza, alto peso)\n"
    "  Sensores 4,5:   Poco precisos (alta varianza, bajo peso)\n"
    "  Sensores 6,7,8: Precision media\n\n"
    "INSTRUCCIONES:\n"
    "  - Ajusta los sliders para cambiar los pesos w_i\n"
    "  - Observa como la recta WLS se mueve\n"
    "  - Compara con OLS (linea roja punteada)\n\n"
    "FORMULA CLAVE:  w_i = 1 / sigma_i^2"
)

props = dict(boxstyle='round,pad=0.6', facecolor='#ecf0f1', 
             alpha=0.95, edgecolor='#34495e', linewidth=2)
ax.text(0.98, 0.02, info_text, transform=ax.transAxes, fontsize=11,
        verticalalignment='bottom', horizontalalignment='right', 
        bbox=props, family='monospace', linespacing=1.3)

# ==============================================================================
# MOSTRAR RESULTADOS INICIALES
# ==============================================================================
print("=" * 70)
print("  RECURSO INTERACTIVO: Minimos Cuadrados Ponderados (WLS)")
print("=" * 70)
print()
print("Resultados iniciales:")
print(f"  OLS (todos los pesos = 1):  y = {beta0_ols:.4f} + {beta1_ols:.4f}x")
print(f"  WLS (pesos originales):     y = {beta0_wls:.4f} + {beta1_wls:.4f}x")
print()
print("Pesos originales (w_i = 1/sigma_i^2):")
for i in range(8):
    print(f"  w{i+1} = {w_original[i]:.2f}  (sigma_{i+1}^2 = {sigma2_original[i]:.1f})")
print()
print("Instrucciones:")
print("  - Usa los sliders para cambiar los pesos")
print("  - Presiona 'Destacar Precisos' para ver el efecto de WLS")
print("  - Presiona 'Todos = 1 (OLS)' para comparar con OLS")
print("=" * 70)

# ==============================================================================
# INICIAR INTERFAZ
# ==============================================================================
plt.show()
