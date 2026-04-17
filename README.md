# Recurso Interactivo: Minimos Cuadrados Ponderados (WLS)

**Autor:** Francisco Terrones  
**Proyecto:** Metodos de Minimos Cuadrados Ponderados  
**Equipo:** Nora, Ocampo, Pablo, Terrones

---

## Resumen

Este proyecto compara **OLS** y **WLS** con dos casos interactivos:

- **Caso 1 (sensores):** mediciones con distinta precision.
- **Caso 2 (delivery):** ETA vs distancia con zonas de distinta variabilidad.

Objetivo: mostrar por que WLS mejora el ajuste cuando hay heterocedasticidad.

---

## Archivos principales

| Archivo | Descripcion |
|---------|-------------|
| `menu_casos.py` | Menu principal para abrir los casos |
| `wls_interactivo.py` | Caso 1: sensores |
| `wls_interactivo2.py` | Caso 2: delivery |
| `requirements.txt` | Dependencias |

---

## Instalacion

```bash
pip install -r requirements.txt
```

`tkinter` es necesario para `menu_casos.py`. Si no esta disponible en tu entorno,
ejecuta los casos directamente por script.

---

## Ejecucion

### Recomendado (menu)

```bash
python menu_casos.py
```

### Directo por script

```bash
python wls_interactivo.py
python wls_interactivo2.py
```

---

## Casos

### Caso 1 - Sensores
- Problema: no todos los sensores tienen la misma precision.
- Controles: sliders `S1..S8` y botones de escenario.
- Idea: mayor varianza -> menor peso.

### Caso 2 - Delivery
- Problema: algunas zonas tienen ETA muy variable.
- Controles: sliders `Z1..Z8`, distancia objetivo y botones.
- Idea: WLS reduce el impacto de zonas ruidosas.

---

## Formulas clave

```text
S_WLS = sum( w_i * (y_i - y_hat_i)^2 )
w_i = 1 / sigma_i^2
```

Para `y = beta0 + beta1*x`:

```text
beta1 = [sum(w)*sum(wxy) - sum(wx)*sum(wy)] / [sum(w)*sum(wx^2) - (sum(wx))^2]
beta0 = [sum(wy) - beta1*sum(wx)] / sum(w)
```

---

Desarrollado con ayuda de Cursor e inspeccionado por Francisco Terrones.
