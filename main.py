"""
main.py
Flujo ETL: carga, inspección, clasificación y exportación de declaraciones IVA.
Sesión 6: Pandas I — Python Intermedio para Análisis de Datos · DIAN 2026
"""

# =============================================================================
# IMPORTS
# Todos los imports van aquí, al inicio del archivo, antes de cualquier otra
# línea de código. Nunca dentro de funciones ni distribuidos a lo largo del
# código. A medida que implementas cada módulo, descomenta el import
# correspondiente.
#import numpy as np
import pandas as pd
from datetime import date

# Sección 3:
# from src.data_loader import cargar_declaraciones
#
# Sección 4 — agrega las dos funciones nuevas al import de data_loader:
# from src.data_loader import cargar_declaraciones, inspeccionar_datos, validar_nulos
#
# Sección 5:
# from src.data_transformer import clasificar_por_valor, agregar_identificador_periodo, preparar_columnas_salida
#
# Sección 6:
# from src.data_exporter import exportar_csv, exportar_excel_por_categoria
# =============================================================================


# =============================================================================
# CONFIGURACIÓN
# =============================================================================

RUTA_DATOS = "data/inputs/declaraciones_iva_2025.csv"
CARPETA_RESULTADOS = "data/outputs"
COLUMNAS_CRITICAS = ["nit", "valor_declarado", "estado"]
COLUMNAS_SALIDA = [
    "identificador_periodo",
    "nit",
    "razon_social",
    "municipio",
    "periodo",
    "valor_declarado",
    "nivel_riesgo",
    "estado",
]


# =============================================================================
# MENÚ
# Esta función ya está implementada. Ejecútala, lee el código y úsala como
# referencia para entender el ciclo del programa.
# =============================================================================

def mostrar_menu():
    """Muestra el menú principal y retorna la opción elegida por el usuario."""
    print("\n" + "=" * 45)
    print("  Pipeline — Declaraciones IVA 2025")
    print("=" * 45)
    print("  1. Cargar datos")
    print("  2. Inspeccionar datos")
    print("  3. Transformar datos")
    print("  4. Exportar resultados")
    print("  5. Ejecutar pipeline completo")
    print("  0. Salir")
    print("=" * 45)
    return input("  Opción: ").strip()


# =============================================================================
# PIPELINE
# __main__ solo llama a main(). La lógica vive en funciones, no a nivel de
# módulo: así puedes importar main.py desde otros scripts sin efectos.
# =============================================================================

def main():
    """Ejecuta el pipeline interactivo de declaraciones IVA."""

    # df y df_salida se declaran aquí para que todas las opciones del menú
    # puedan leerlas y modificarlas. Arrancan en None hasta que se ejecute
    # la carga.
    df = None
    df_salida = None

    opcion = mostrar_menu()

    while opcion != "0":

        # -----------------------------------------------------------------
        # OPCIÓN 1: CARGA
        # El import ya está en el bloque de arriba, solo descoméntalo.
        # Completa los espacios marcados con ___ y ejecuta.
        # -----------------------------------------------------------------
        if opcion == "1":
            # df = cargar_declaraciones(___)
            # print(f"Filas cargadas: {___}")
            pass

        # -----------------------------------------------------------------
        # OPCIÓN 2: INSPECCIÓN
        # Tienes los nombres de las funciones. Escribe las llamadas completas.
        # Antes de llamar a inspeccionar_datos(), verifica que df no sea None;
        # si lo es, muestra un mensaje y vuelve al menú.
        # Funciones disponibles: inspeccionar_datos(), validar_nulos()
        # -----------------------------------------------------------------
        elif opcion == "2":
            pass

        # -----------------------------------------------------------------
        # OPCIÓN 3: TRANSFORMACIÓN
        # - Clasificar cada registro en nivel de riesgo (Alto / Medio / Bajo)
        #   con umbral_alto=10_000_000 y umbral_medio=5_000_000.
        # - Agregar la columna identificador_periodo.
        # - Guardar en df_salida solo las columnas de COLUMNAS_SALIDA.
        # Verifica que df no sea None antes de transformar.
        # -----------------------------------------------------------------
        elif opcion == "3":
            pass

        # -----------------------------------------------------------------
        # OPCIÓN 4: EXPORTACIÓN
        # Genera un CSV y un Excel en data/outputs/.
        # -----------------------------------------------------------------
        elif opcion == "4":
            pass

        # -----------------------------------------------------------------
        # OPCIÓN 5: PIPELINE COMPLETO
        # Ejecuta las cuatro etapas anteriores en secuencia.
        # -----------------------------------------------------------------
        elif opcion == "5":
            pass

        else:
            print("  Opción no válida. Intenta de nuevo.")

        opcion = mostrar_menu()

    print("  Hasta luego.")

def probar_acceso_diccionario():
    declaracion= {"nit":"800234567-0","estado":"Pendiente"}
    print (declaracion["valor_declarado"])
    
def revisar_declaracion (declaracion):
    declaracion = {
    "nit": "900123456-1",
    "razon_social": "Comercializadora Andina S.A.S",
    "valor_declarado": 4_500_000,
    "estado": "Presentada",
    "municipio": "Bogotá",

}

def probar_acceso_serie():
    serie = pd.Series([100,200,300])
    print (serie[5])

def explorar_dataframe():
    datos = {"nit":[109312556,1098534785,900235852,700000000],
             "razon_social":["PEPE PEREZ","JOSE JAIMES","ABC.SAS","DEF.LTA"],
             "municipio":["Cúcuta", "Rionegro","Pamplona","Malaga"],
             "valor_declarado":[1580000,25885000,256355262,2158235]}
    df= pd.DataFrame(datos)
    df.columns=df.columns.astype(object)
    print(df.index)
    print(df.columns)
    print(df.shape)

def analizar_serie(nits, valores):
    serie = pd.Series(valores, index=nits)
    print(f"Media:        {serie.mean()}")
    print(f"Máximo:       {serie.max()}")
    print(f"Mínimo:       {serie.min()}")
    print(f"NIT con mayor valor: {serie.idxmax()}")

def construir_dataframe(lista_declaraciones):
    df= pd.DataFrame(lista_declaraciones)
    print(f"Elementos de la lista: {len(lista_declaraciones)}")
    print(f"numero de filas en el Dataframe: {len(df)}")
    return df
    

# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================


if __name__ == "__main__":
    #probar_acceso_serie()

    #probar_acceso_diccionario()

    #explorar_dataframe()

    #nits    = ["900111222-0", "800333444-5", "700555666-1", "600777888-2", "500999000-3"]
    #valores = [4_500_000, 12_300_000, 2_100_000, 8_750_000, 15_200_000]
    #analizar_serie(nits, valores)

    declaraciones = [
    {"nit": "900111222-0", "razon_social": "Empresa A", "valor_declarado": 4_500_000},
    {"nit": "800333444-5", "razon_social": "Empresa B", "valor_declarado": 12_300_000},
    {"nit": "700555666-1", "razon_social": "Empresa C", "valor_declarado": 2_100_000},
    ]
    construir_dataframe(declaraciones)
    #main()
