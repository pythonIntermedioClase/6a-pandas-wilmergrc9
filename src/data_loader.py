"""
src/data_loader.py
Funciones de carga e inspección de datos.
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
    # TODO: Usa pd.read_csv() para cargar el archivo desde `ruta`.
    # Fuerza las columnas "nit" y "codigo_municipio" a tipo str 
    # Si se recibe una lista en `columnas`, úsala
    # Si `columnas` es None, carga todas las columnas.
    # Retorna el DataFrame cargado.
    #pass
    df_datos=pd.read_csv(ruta)
    print(df_datos)
    return df_datos



def inspeccionar_datos(df):
    """
    Imprime un reporte de inspección del DataFrame.

    Muestra dimensiones, tipos de dato, conteo de valores faltantes
    por columna y total de filas duplicadas.

    Args:
        df (pd.DataFrame): DataFrame a inspeccionar.

    Returns:
        None
    """
    #pass
    #print (f"Dimensiones: {df.shape}")
    print (f"Tipos de dato: {df.dtypes}")
    print (f"Nulos por Columna: {df.isnull().sum()}")
    print (f"Total de celdas vacias: {df.isnull().sum().sum()}")
    print (f"Filas Duplicadas: {df.duplicated().sum()}")
    print (df.nunique())
    print (df.value_counts())


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
    # TODO: Recorre columnas_criticas con un ciclo for.
    # Para cada columna, calcula si hay algún valor faltante y si lo hay imprime el nombre de la columna 
    # y la cantidad de nulos encontrados.
    #pass
    for columna in columnas_criticas:
        nulos = df[columna].isnull().sum()
        if nulos > 0:
            print(f"⚠️  {columna}: {nulos} nulos")
        else:
            print(f"✓ {columna}: sin nulos")


# =============================================================================
# BLOQUE DE PRUEBA
# Se ejecuta solo cuando corres este archivo directamente:
#   python src/data_loader.py
# No se ejecuta cuando main.py importa las funciones.
# Actualiza las llamadas a medida que implementas cada función.
# =============================================================================
if __name__ == "__main__":
    df = cargar_declaraciones("data/input/declaraciones_iva_2025.csv")
    inspeccionar_datos(df)
    validar_nulos(df, ["nit", "valor_declarado", "estado"])
