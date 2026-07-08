"""
src/data_exporter_solved.py
Soluciones de referencia para el instructor — NO compartir con estudiantes.
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
        exportar_csv(df, "data/output", "declaraciones_clasificadas")
        # Genera: data/output/declaraciones_clasificadas_20260707.csv
    """
    fecha_hoy = date.today().strftime("%Y%m%d")
    nombre_archivo = f"{nombre_base}_{fecha_hoy}.csv"
    ruta_completa = f"{carpeta}/{nombre_archivo}"
    df.to_csv(ruta_completa, index=False)
    print(f"CSV guardado: {ruta_completa}")


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
        exportar_excel_por_categoria(df, "data/output", "declaraciones", "nivel_riesgo")
        # Genera hojas: Todos, Alto, Medio, Bajo
    """
    fecha_hoy = date.today().strftime("%Y%m%d")
    nombre_archivo = f"{nombre_base}_{fecha_hoy}.xlsx"
    ruta_completa = f"{carpeta}/{nombre_archivo}"

    with pd.ExcelWriter(ruta_completa, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Todos", index=False)

        categorias = df[columna_categoria].unique()
        for categoria in categorias:
            df_categoria = df[df[columna_categoria] == categoria]
            df_categoria.to_excel(writer, sheet_name=str(categoria), index=False)

    print(f"Excel guardado: {ruta_completa}")
