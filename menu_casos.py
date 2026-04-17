#!/usr/bin/env python3
"""
Menú principal para abrir los casos interactivos de WLS.
"""

from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


BASE_DIR = Path(__file__).resolve().parent


def abrir_script(nombre_script):
    """Abre un caso en un proceso Python aparte."""
    ruta_script = BASE_DIR / nombre_script
    if not ruta_script.exists():
        messagebox.showerror("Archivo no encontrado", f"No existe: {ruta_script.name}")
        return

    try:
        subprocess.Popen([sys.executable, str(ruta_script)], cwd=str(BASE_DIR))
    except Exception as exc:
        messagebox.showerror("Error", f"No se pudo abrir {ruta_script.name}\n\n{exc}")


def crear_menu():
    """Crea la ventana principal del menú."""
    root = tk.Tk()
    root.title("WLS - Menú de Casos")
    root.geometry("1280x860")
    root.resizable(False, False)
    root.configure(bg="#eef3f8")

    header = tk.Frame(root, bg="#1f3b57", height=110)
    header.pack(fill="x")
    header.pack_propagate(False)

    titulo = tk.Label(
        header,
        text="Laboratorio Interactivo WLS",
        font=("Segoe UI", 30, "bold"),
        fg="white",
        bg="#1f3b57"
    )
    titulo.pack(pady=(14, 0))

    subtitulo = tk.Label(
        header,
        text="Selecciona un caso para explorar OLS vs WLS",
        font=("Segoe UI", 17),
        fg="#d9e6f2",
        bg="#1f3b57"
    )
    subtitulo.pack()

    contenido = tk.Frame(root, bg="#eef3f8")
    contenido.pack(fill="both", expand=True, padx=28, pady=22)

    descripcion = tk.Label(
        contenido,
        text="Cada botón abre una ventana interactiva independiente.",
        font=("Segoe UI", 17),
        fg="#3b4b5a",
        bg="#eef3f8"
    )
    descripcion.pack(anchor="w", pady=(0, 10))

    card1 = tk.Frame(contenido, bg="white", highlightbackground="#d7e0ea", highlightthickness=1)
    card1.pack(fill="x", pady=(0, 12))

    caso1_titulo = tk.Label(
        card1,
        text="Caso 1 - Sensores de temperatura",
        font=("Segoe UI", 19, "bold"),
        fg="#1f3b57",
        bg="white"
    )
    caso1_titulo.pack(anchor="w", padx=14, pady=(12, 4))

    caso1_info = tk.Label(
        card1,
        text=(
            "Problema: varios sensores miden la misma variable con distinta precisión.\n"
            "Objetivo: ajustar una recta que priorice sensores confiables y reduzca el impacto\n"
            "de mediciones ruidosas mediante pesos."
        ),
        font=("Segoe UI", 15),
        fg="#334455",
        justify="left",
        anchor="w",
        bg="white",
        wraplength=950
    )
    caso1_info.pack(anchor="w", padx=14)

    btn_case_1 = tk.Button(
        card1,
        text="Abrir Caso 1 (wls_interactivo.py)",
        font=("Segoe UI", 16, "bold"),
        bg="#2f7dc1",
        fg="white",
        activebackground="#2769a2",
        activeforeground="white",
        width=36,
        height=2,
        relief="flat",
        cursor="hand2",
        command=lambda: abrir_script("wls_interactivo.py")
    )
    btn_case_1.pack(anchor="w", padx=14, pady=(10, 12))

    card2 = tk.Frame(contenido, bg="white", highlightbackground="#d7e0ea", highlightthickness=1)
    card2.pack(fill="x", pady=(0, 14))

    caso2_titulo = tk.Label(
        card2,
        text="Caso 2 - Delivery (\"ETA\" vs distancia)",
        font=("Segoe UI", 19, "bold"),
        fg="#1f3b57",
        bg="white"
    )
    caso2_titulo.pack(anchor="w", padx=14, pady=(12, 4))

    caso2_info = tk.Label(
        card2,
        text=(
            "Problema: estimar tiempo de entrega por distancia cuando algunas zonas tienen\n"
            "alta variabilidad por tráfico, clima y demanda.\n"
            "Objetivo: comparar OLS vs WLS para obtener predicciones de ETA\n"
            "(Estimated Time of Arrival) más robustas."
        ),
        font=("Segoe UI", 15),
        fg="#334455",
        justify="left",
        anchor="w",
        bg="white",
        wraplength=950
    )
    caso2_info.pack(anchor="w", padx=14)

    btn_case_2 = tk.Button(
        card2,
        text="Abrir Caso 2 (wls_interactivo2.py)",
        font=("Segoe UI", 16, "bold"),
        bg="#2ba86a",
        fg="white",
        activebackground="#228654",
        activeforeground="white",
        width=36,
        height=2,
        relief="flat",
        cursor="hand2",
        command=lambda: abrir_script("wls_interactivo2.py")
    )
    btn_case_2.pack(anchor="w", padx=14, pady=(10, 12))

    footer = tk.Frame(contenido, bg="#eef3f8")
    footer.pack(fill="x")

    btn_salir = tk.Button(
        footer,
        text="Salir",
        font=("Segoe UI", 15, "bold"),
        width=18,
        relief="groove",
        cursor="hand2",
        command=root.destroy
    )
    btn_salir.pack(anchor="e")

    root.mainloop()


if __name__ == "__main__":
    crear_menu()
