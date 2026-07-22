"""
src/data_exporter.py
Funciones de exportación a CSV y Excel.
Sesión 6: Pandas I — Python Intermedio para Análisis de Datos · DIAN 2026
"""

import pandas as pd
from datetime import date


def exportar_csv(df, carpeta, nombre_base):
    """
    Exporta un DataFrame a CSV con la fecha de hoy en el nombre del archivo.

    El nombre generado sigue el formato: "{nombre_base}_{YYYYMMDD}.csv"

    Args:
        df (pd.DataFrame): DataFrame a exportar.
        carpeta (str): Carpeta de destino. Debe existir antes de llamar la función.
        nombre_base (str): Nombre base del archivo, sin extensión ni fecha.

    Returns:
        None

    Ejemplos:
        exportar_csv(df, "resultados", "declaraciones_clasificadas")
        # Genera: resultados/declaraciones_clasificadas_20240131.csv
    """
    # TODO: Genera la fecha
    # Construye el nombre del archivo
    # Construye la ruta completa
    # Exporta el resultado
    pass


def exportar_excel_por_categoria(df, carpeta, nombre_base, columna_categoria):
    """
    Exporta un DataFrame a Excel con una hoja por cada categoría.

    Siempre incluye una hoja "Todos" con el DataFrame completo.
    Cada valor único en columna_categoria genera una hoja adicional
    con ese nombre como título.

    Args:
        df (pd.DataFrame): DataFrame a exportar.
        carpeta (str): Carpeta de destino. Debe existir antes de llamar la función.
        nombre_base (str): Nombre base del archivo, sin extensión ni fecha.
        columna_categoria (str): Columna cuyos valores únicos determinan las hojas.

    Returns:
        None

    Ejemplos:
        exportar_excel_por_categoria(df, "resultados", "declaraciones", "nivel_riesgo")
        # Genera hojas: Todos, Alto, Medio, Bajo
    """
    pass


# =============================================================================
# BLOQUE DE PRUEBA
# Se ejecuta solo cuando corres este archivo directamente:
#   python src/data_exporter.py
# No se ejecuta cuando main.py importa las funciones.
# Actualiza las llamadas a medida que implementas cada función.
# =============================================================================
if __name__ == "__main__":
    df = pd.read_csv(
        "data/inputs/declaraciones_iva_2025.csv",
        dtype={"nit": str, "codigo_municipio": str},
    )
    exportar_csv(df, "data/outputs", "declaraciones_prueba")
    exportar_excel_por_categoria(df, "data/outputs", "declaraciones_prueba", "estado")
