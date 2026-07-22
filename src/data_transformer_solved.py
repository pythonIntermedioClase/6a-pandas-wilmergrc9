"""
src/data_transformer_solved.py
Soluciones de referencia para el instructor.
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
    df["nivel_riesgo"] = np.where(
        df["valor_declarado"] >= umbral_alto,
        "Alto",
        np.where(
            df["valor_declarado"] >= umbral_medio,
            "Medio",
            "Bajo",
        ),
    )
    return df


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
    df["identificador_periodo"] = df["nit"] + "_" + df["periodo"].astype(str)
    return df


def preparar_columnas_salida(df, columnas):
    """
    Retorna un nuevo DataFrame con solo las columnas indicadas, en ese orden.

    No modifica el DataFrame original.

    Args:
        df (pd.DataFrame): DataFrame de origen.
        columnas (list): Nombres de las columnas a incluir, en el orden deseado.

    Returns:
        pd.DataFrame: DataFrame con las columnas seleccionadas.

    Ejemplos:
        df_salida = preparar_columnas_salida(df, ["nit", "valor_declarado", "nivel_riesgo"])
    """
    return df[columnas]
