"""
src/data_loader_solved.py
Soluciones de referencia para el instructor.
Sesión 6: Pandas I — Python Intermedio para Análisis de Datos · DIAN 2026
"""

import pandas as pd


def cargar_declaraciones(ruta, columnas=None):
    """
    Carga un archivo CSV de declaraciones tributarias.

    Args:
        ruta (str): Ruta al archivo CSV.
        columnas (list, optional): Lista de columnas a cargar.
            Si es None, carga todas las columnas.

    Returns:
        pd.DataFrame: DataFrame con las declaraciones cargadas.

    Ejemplos:
        cargar_declaraciones("datos/declaraciones_iva_2025.csv")
        cargar_declaraciones("datos/declaraciones_iva_2025.csv", columnas=["nit", "valor_declarado"])
    """
    tipos = {"nit": str, "codigo_municipio": str}

    if columnas is not None:
        df = pd.read_csv(ruta, dtype=tipos, usecols=columnas, encoding="utf-8")
    else:
        df = pd.read_csv(ruta, dtype=tipos, encoding="utf-8")

    return df


def inspeccionar_datos(df):
    """
    Imprime un reporte de inspección del DataFrame.

    Muestra dimensiones, tipos de dato, conteo de valores faltantes
    por columna y total de filas duplicadas. Para columnas de texto
    con menos de 20 valores únicos, muestra además el conteo por valor;
    para las demás, solo el número de valores únicos.

    Args:
        df (pd.DataFrame): DataFrame a inspeccionar.

    Returns:
        None
    """
    print("=== Inspección del dataset ===")
    print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    print()
    print("Tipos de dato:")
    print(df.dtypes)
    print()
    print("Valores faltantes por columna:")
    print(df.isnull().sum())
    print()
    print(f"Filas duplicadas: {df.duplicated().sum()}")
    print()

    for columna in df.columns:
        if df[columna].dtype == object:
            cantidad_unicos = df[columna].nunique()
            if cantidad_unicos < 20:
                print(f"Valores únicos en '{columna}':")
                print(df[columna].value_counts())
                print()
            else:
                print(f"'{columna}': {cantidad_unicos} valores únicos")
                print()


def validar_nulos(df, columnas_criticas):
    """
    Revisa que las columnas críticas no tengan valores faltantes.

    Si alguna columna tiene nulos, imprime el nombre de la columna
    y la cantidad. No detiene la ejecución.

    Args:
        df (pd.DataFrame): DataFrame a validar.
        columnas_criticas (list): Columnas que no deben tener nulos.

    Returns:
        None

    Ejemplos:
        validar_nulos(df, ["nit", "valor_declarado", "estado"])
    """
    for columna in columnas_criticas:
        cantidad_nulos = df[columna].isnull().sum()
        if cantidad_nulos > 0:
            print(f"Aviso: '{columna}' tiene {cantidad_nulos} valor(es) faltante(s).")
