"""
src/data_transformer.py
Funciones de clasificación, derivación de variables y selección de columnas.
Sesión 6: Pandas I — Python Intermedio para Análisis de Datos · DIAN 2026
"""

import numpy as np
import pandas as pd


def clasificar_por_valor(df, umbral_alto, umbral_medio):
    """
    Agrega la columna "nivel_riesgo" al DataFrame según el valor declarado.

    Categorías asignadas:
        "Alto"  : valor_declarado >= umbral_alto
        "Medio" : valor_declarado >= umbral_medio
        "Bajo"  : los demás casos

    Args:
        df (pd.DataFrame): DataFrame con la columna "valor_declarado".
        umbral_alto (float): Valor mínimo para la categoría "Alto".
        umbral_medio (float): Valor mínimo para la categoría "Medio".

    Returns:
        pd.DataFrame: DataFrame con la columna "nivel_riesgo" agregada.

    Ejemplos:
        df = clasificar_por_valor(df, umbral_alto=10_000_000, umbral_medio=5_000_000)
    """
    pass


def agregar_identificador_periodo(df):
    """
    Agrega la columna "identificador_periodo" combinando nit y periodo.

    El formato resultante es: "{nit}_{periodo}"
    Por ejemplo: "900123456-1_202401"

    Args:
        df (pd.DataFrame): DataFrame con las columnas "nit" y "periodo".

    Returns:
        pd.DataFrame: DataFrame con la columna "identificador_periodo" agregada.

    Ejemplos:
        df = agregar_identificador_periodo(df)
        # df["identificador_periodo"].iloc[0] → "900123456-1_202401"
    """
    pass


def preparar_columnas_salida(df, columnas):
    """
    Retorna un nuevo DataFrame con solo las columnas indicadas en el párametro `columnas`, en ese orden.

    No modifica el DataFrame original.

    Args:
        df (pd.DataFrame): DataFrame de origen.
        columnas (list): Nombres de las columnas a incluir, en el orden deseado.

    Returns:
        pd.DataFrame: DataFrame con las columnas seleccionadas.

    Ejemplos:
        df_salida = preparar_columnas_salida(df, ["nit", "valor_declarado", "nivel_riesgo"])
    """
    pass


# =============================================================================
# BLOQUE DE PRUEBA
# Se ejecuta solo cuando corres este archivo directamente:
#   python src/data_transformer.py
# No se ejecuta cuando main.py importa las funciones.
# Actualiza las llamadas a medida que implementas cada función.
# =============================================================================
if __name__ == "__main__":
    df = pd.read_csv(
        "data/inputs/declaraciones_iva_2025.csv",
        dtype={"nit": str, "codigo_municipio": str},
    )
    df = clasificar_por_valor(df, umbral_alto=10_000_000, umbral_medio=5_000_000)
    df = agregar_identificador_periodo(df)
    columnas = [
        "identificador_periodo", "nit", "razon_social",
        "municipio", "periodo", "valor_declarado", "nivel_riesgo", "estado",
    ]
    df_salida = preparar_columnas_salida(df, columnas)
    print(df_salida.head())
    print(df["nivel_riesgo"].value_counts())
