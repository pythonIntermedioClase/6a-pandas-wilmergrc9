# Sesión 6 y 7: Pandas I — Declaraciones IVA

Proyecto de práctica del curso Python Intermedio para Análisis de Datos · DIAN 2026.

## Estructura del proyecto

```
sesion6_codigo/
├── src/
│   ├── __init__.py
│   ├── data_loader.py       # Funciones de carga e inspección
│   ├── data_transformer.py  # Clasificación, variables derivadas y selección de columnas
│   └── data_exporter.py     # Escritura a CSV y Excel
├── data/
│   ├── inputs/              # Archivos fuente — solo lectura
│   │   └── declaraciones_iva_2025.csv
│   └── outputs/             # Archivos generados — excluidos de git
├── main.py                  # Orquesta el flujo completo
├── requirements.txt
├── .gitignore
└── README.md
```

## Configuración del entorno

**1. Activa el ambiente virtual**

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**2. Instala las dependencias**

```bash
pip install -r requirements.txt
```

**3. Ejecuta el proyecto**

```bash
python main.py
```

## Regla de imports

Los imports van **siempre al inicio del archivo**, agrupados en un solo bloque, antes de cualquier otra línea de código.

```python
# Correcto
from src.data_loader import cargar_declaraciones
from src.data_transformer import clasificar_por_valor

RUTA_DATOS = "data/inputs/declaraciones_iva_2025.csv"
...
```

```python
# Incorrecto — nunca dentro de funciones ni distribuidos en el código
def ejecutar():
    from src.data_loader import cargar_declaraciones  # ← no hagas esto
    ...
```

Esta convención es un estándar de Python (PEP 8) y hace que sea fácil ver de un vistazo todas las dependencias del archivo.

## Flujo ETL

El proyecto sigue el patrón Extract–Transform–Load:

| Fase | Responsabilidad | Módulo |
|---|---|---|
| Extract | Cargar y validar los datos de entrada | `src/data_loader.py` |
| Transform | Clasificar, derivar variables, seleccionar columnas | `src/data_transformer.py` |
| Load | Escribir los resultados a disco | `src/data_exporter.py` |

`main.py` no hace ninguna de esas tres cosas: solo las coordina en secuencia.

# Sesión 6-7: Pandas
**Diccionarios, carga, inspección, transformación básica y exportación**

---

### ¿En qué archivo va cada cosa?

`main.py` orquesta el flujo: muestra el menú, recibe la opción del usuario y llama las funciones. No calcula nada por sí solo; delega todo el trabajo a funciones que viven en otros archivos.

Los archivos en `src/` son los módulos de trabajo: cada uno agrupa funciones relacionadas con una etapa del pipeline. `data_loader.py` sabe cargar e inspeccionar datos. `data_transformer.py` sabe clasificar y derivar columnas. `data_exporter.py` sabe escribir archivos. Cuando `main.py` necesita cargar datos, importa la función de `data_loader.py` en lugar de tener ese código dentro de sí mismo.

Los archivos en `src/` ya existen con las firmas de las funciones y un `pass` como cuerpo: tú abres cada archivo y escribes la implementación dentro a medida que avanzas. La progresión en cada sección sigue la misma lógica:

- **Básico / Intermedio**: implementas directamente en el módulo `src/` correspondiente y pruebas con el bloque `if __name__ == "__main__":` del mismo archivo. El objetivo es entender cómo funciona la herramienta antes de conectarla al menú.
- **Avanzado**: conectas esa implementación a `main.py` — descomentás el import y completás la opción del menú que corresponde.


## Tabla de contenido

1. [Diccionarios](#1-diccionarios)
2. [De NumPy a pandas: Series y DataFrame](#2-de-numpy-a-pandas-series-y-dataframe)
3. [Carga de datos con pd.read_csv()](#3-carga-de-datos-con-pdread_csv)
4. [Inspección del conjunto de datos](#4-inspección-del-conjunto-de-datos)
5. [Cálculos y clasificación de registros](#5-cálculos-y-clasificación-de-registros)
6. [Exportar resultados](#6-exportar-resultados)
7. [Patrón ETL: separar responsabilidades](#7-patrón-etl-separar-responsabilidades)

---

## 1. Diccionarios

Piensa en una fila de la planilla donde registras declaraciones: cada celda tiene un encabezado que describe su contenido. Un **diccionario** funciona igual. Asocia un nombre (la clave) con un dato (el valor), y accedes a cada dato por su nombre, no por su posición.

La diferencia con una lista se hace clara cuando tienes varios campos sobre el mismo registro:
``
```python
# Con lista: accedes por posición
declaracion_lista = ["900123456-1", "Comercializadora Andina S.A.S", 4_500_000, "Presentada"]
print(declaracion_lista[2])  # → 4500000, pero ¿qué era la posición 2?

# Con diccionario: accedes por nombre
declaracion = {
    "nit": "900123456-1",
    "razon_social": "Comercializadora Andina S.A.S",
    "valor_declarado": 4_500_000,
    "estado": "Presentada",
}
print(declaracion["valor_declarado"])  # → 4500000
```

Con la lista tienes que recordar o documentar en algún lugar que la posición 2 es `valor_declarado`. Con el diccionario, el nombre lo dice.

![Diccionarios en Python: estructura, acceso y comparación con lista](img/python_diccionario.svg)

Si imprimes el diccionario completo, ves todos los pares clave-valor en una sola línea:

```python
print(declaracion)
# {'nit': '900123456-1', 'razon_social': 'Comercializadora Andina S.A.S',
#  'valor_declarado': 4500000, 'estado': 'Presentada'}
```

Para acceder a un campo específico:

```python
print(declaracion["nit"])              # → 900123456-1
print(declaracion["valor_declarado"])  # → 4500000
```

Para recorrer todos los pares a la vez, `.items()` devuelve la clave y el valor en cada vuelta del ciclo:

```python
for clave, valor in declaracion.items():
    print(clave, ":", valor)
# nit : 900123456-1
# razon_social : Comercializadora Andina S.A.S
# valor_declarado : 4500000
# estado : Presentada
```

También puedes agregar o modificar campos después de crear el diccionario:

```python
declaracion["periodo"] = "202501"
declaracion["valor_declarado"] = 5_000_000
print(declaracion["periodo"])          # → 202501
print(declaracion["valor_declarado"])  # → 5000000
```

Los diccionarios son **mutables**: puedes agregar claves nuevas, modificar valores existentes o eliminar claves en cualquier momento después de crearlo. Esto los hace adecuados para construir registros progresivamente — por ejemplo, al procesar un archivo línea por línea y enriquecer cada registro con información calculada.

⚠️ Si intentas acceder a una clave que no existe, Python lanza `KeyError` y detiene la ejecución. El mensaje incluye la clave que buscaste:

```python
print(declaracion["municipio"])
# KeyError: 'municipio'
```

Cuando no estás seguro de si una clave existe, el método `.get()` es la alternativa segura. Si la clave existe devuelve su valor; si no existe, devuelve `None` por defecto (o el valor que tú definas como segundo argumento), sin lanzar error:

```python
print(declaracion.get("municipio"))             # → None  (sin error)
print(declaracion.get("municipio", "Desconocido"))  # → "Desconocido"
print(declaracion.get("nit", "sin nit"))        # → "900123456-1"  (la clave existe)
```

`.get()` es especialmente útil cuando procesas datos que pueden tener campos opcionales o cuando recibes registros de fuentes externas donde no controlas si todos los campos están presentes. En análisis de datos tributarios, por ejemplo, puede haber registros históricos con campos que no existían en versiones antiguas del formulario.

Otros métodos frecuentes:

- **`.keys()`**: devuelve todas las claves del diccionario, sin los valores. Útil para verificar qué campos tiene un registro.
- **`.values()`**: devuelve todos los valores, sin las claves.
- **`.update(otro_dict)`**: agrega o actualiza múltiples claves a la vez usando otro diccionario. Equivalente a asignar cada clave por separado, pero más conciso.

```python
print(list(declaracion.keys()))
# ['nit', 'razon_social', 'valor_declarado', 'estado', 'periodo']

declaracion.update({"municipio": "Bogotá", "codigo_municipio": "11001"})
print(len(declaracion))  # → 7  (dos claves nuevas agregadas)
```

**Por qué los diccionarios son rápidos.** Internamente, Python implementa los diccionarios como tablas hash: cuando guardas un par clave-valor, Python calcula un número (el "hash") a partir de la clave y usa ese número para determinar en qué posición de memoria guardar el valor. Cuando buscas una clave, Python calcula su hash nuevamente y va directamente a esa posición, sin recorrer las demás. Por eso, buscar una clave en un diccionario con 10 pares tarda exactamente lo mismo que en uno con 10 millones de pares: siempre es una sola operación. En las listas, en cambio, buscar si un valor existe requiere revisarlos uno por uno desde el principio. Para el trabajo con registros donde accedes por nombre de campo, los diccionarios son la estructura correcta — y pandas los usa internamente para organizar sus columnas.

Cuando construyes un DataFrame desde código, la forma habitual es pasar un diccionario: cada clave se convierte en el nombre de una columna, y la lista de valores asociada se convierte en los datos de esa columna. Lo verás en la siguiente sección.

> **Pausa y piensa:** Tienes el diccionario `declaracion` con cuatro campos. Sin ejecutar nada, ¿qué imprimiría `len(declaracion)`? ¿Y `list(declaracion.keys())`?

---

### Ejercicios

#### Inducción al error

Abre `main.py` y agrega esta función antes del bloque `if __name__ == '__main__':`. Luego en el bloque `__main__`, comenta la llamada actual al menú y agrega la llamada a esta función para probarla:

```python
def probar_acceso_diccionario():
    declaracion = {"nit": "800234567-0", "estado": "Pendiente"}
    print(declaracion["valor_declarado"])


if __name__ == "__main__":
    probar_acceso_diccionario()
    # main()  ← comentado mientras probamos
```

Ejecuta el script. ¿Qué dice el mensaje de error? ¿Qué información te da para saber exactamente dónde está el problema y cómo corregirlo?

Cuando termines, vuelve a dejar `main()` activo y comenta o elimina la llamada a `probar_acceso_diccionario()`.

> **Reto para quienes van adelantados:** en lugar de probar cada función por separado, escribe un menú en el bloque `__main__` que le pregunte al usuario qué función quiere ejecutar e invoque la que corresponda. 

#### Básico

📂 `main.py`

Escribe una función `revisar_declaracion(declaracion)` que reciba este diccionario:

```python
declaracion = {
    "nit": "900123456-1",
    "razon_social": "Comercializadora Andina S.A.S",
    "valor_declarado": 4_500_000,
    "estado": "Presentada",
    "municipio": "Bogotá",
}
```

La función debe hacer dos cosas en orden:

1. Recorrer todos los pares con `.items()` e imprimir cada campo en una línea.
2. Cambiar `"estado"` a `"Revisada"` e imprimir solo ese campo para confirmar el cambio.

```bash
La salida esperada al llamar `revisar_declaracion(declaracion)` es:
nit: 900123456-1
razon_social: Comercializadora Andina S.A.S
valor_declarado: 4500000
estado: Presentada
municipio: Bogotá
Estado actualizado: Revisada
```

Llama la función desde el bloque `__main__` para verificar que la salida coincide.

<details>
<summary>💡 Ver solución</summary>

```python
def revisar_declaracion(declaracion):
    for clave, valor in declaracion.items():
        print(f"{clave}: {valor}")
    declaracion["estado"] = "Revisada"
    print(f"\nEstado actualizado: {declaracion['estado']}")


if __name__ == "__main__":
    declaracion = {
        "nit": "900123456-1",
        "razon_social": "Comercializadora Andina S.A.S",
        "valor_declarado": 4_500_000,
        "estado": "Presentada",
        "municipio": "Bogotá",
    }
    revisar_declaracion(declaracion)
    # main()
```

</details>

#### Intermedio

📂 `main.py`

Escribe una función `resumen_declaraciones(lista_declaraciones)` que reciba una lista de diccionarios con los campos `"nit"` y `"valor_declarado"`, y calcule e imprima cuatro datos:

- Total de declaraciones en la lista de diccionarios (usa una función que aprendimos en sesiones anteriores)
- Suma de todos los valores declarados.
- Promedio de valor declarado.
- NIT de la declaración con el valor más alto.

> Para obtener el valor de un campo dentro de cada diccionario de la lista, usa la misma sintaxis de acceso por clave que viste en la sección anterior: `declaracion["valor_declarado"]` te da el número de esa declaración. Si recorres la lista con un ciclo `for`, en cada vuelta tendrás un diccionario distinto y podrás acceder a sus campos de la misma forma. Por ejemplo, `for dec in lista_declaraciones: print(dec["nit"])` imprimiría el NIT de cada elemento.

```python
declaraciones = [
    {"nit": "900111222-0", "valor_declarado": 1_200_000},
    {"nit": "800333444-5", "valor_declarado": 3_400_000},
    {"nit": "700555666-1", "valor_declarado":   850_000},
    {"nit": "600777888-2", "valor_declarado": 5_100_000},
]
```

La salida esperada al llamar `resumen_declaraciones(declaraciones)` es:
```bash
Total de declaraciones: 4
Suma total declarada:   10550000
Promedio declarado:     2637500.0
NIT con mayor valor:    600777888-2
```

Llama la función desde el bloque `__main__` con la lista de arriba y verifica que los números coinciden.

<details>
<summary>💡 Ver solución</summary>

```python
def resumen_declaraciones(lista_declaraciones):
    total = len(lista_declaraciones)
    suma = sum(dec["valor_declarado"] for dec in lista_declaraciones)
    promedio = suma / total
    nit_max = max(lista_declaraciones, key=lambda d: d["valor_declarado"])["nit"]
    print(f"Total de declaraciones: {total}")
    print(f"Suma total declarada:   {suma}")
    print(f"Promedio declarado:     {promedio}")
    print(f"NIT con mayor valor:    {nit_max}")


if __name__ == "__main__":
    declaraciones = [
        {"nit": "900111222-0", "valor_declarado": 1_200_000},
        {"nit": "800333444-5", "valor_declarado": 3_400_000},
        {"nit": "700555666-1", "valor_declarado":   850_000},
        {"nit": "600777888-2", "valor_declarado": 5_100_000},
    ]
    resumen_declaraciones(declaraciones)
    # main()
```

</details>

#### Avanzado

📂 `main.py`

Escribe dos funciones:

**`construir_declaracion(nit, razon_social, valor_declarado, municipio)`**
Construye y retorna un diccionario con esos cuatro campos más:
- `"estado"` con valor inicial `"Pendiente"`.
- `"nivel_riesgo"` calculado según el monto: `"Alto"` si `valor_declarado >= 10_000_000`, `"Medio"` si está entre 5 y 10 millones (inclusive el límite inferior), `"Bajo"` en los demás casos.

Llamadas de prueba y resultado esperado:

```python
construir_declaracion("900123456-1", "Comercializadora Andina", 12_500_000, "Bogotá")
# {
#   "nit": "900123456-1",
#   "razon_social": "Comercializadora Andina",
#   "valor_declarado": 12500000,
#   "municipio": "Bogotá",
#   "estado": "Pendiente",
#   "nivel_riesgo": "Alto"
# }

construir_declaracion("800234567-0", "Distribuidora del Valle", 6_800_000, "Cali")
# { ..., "nivel_riesgo": "Medio" }

construir_declaracion("700345678-9", "Inversiones Ríos", 950_000, "Medellín")
# { ..., "nivel_riesgo": "Bajo" }
```

**`imprimir_declaracion(declaracion)`**
Recorre el diccionario con `.items()` e imprime cada campo con el formato `"campo: valor"`. La salida para el primer ejemplo debe verse así:
```bash
nit: 900123456-1
razon_social: Comercializadora Andina
valor_declarado: 12500000
municipio: Bogotá
estado: Pendiente
nivel_riesgo: Alto
```

Prueba el flujo completo desde el bloque `__main__` con los tres montos para verificar que `nivel_riesgo` cambia correctamente en cada caso:

```python
if __name__ == "__main__":
    for monto in [12_500_000, 6_800_000, 950_000]:
        dec = construir_declaracion("900123456-1", "Empresa Ejemplo", monto, "Bogotá")
        imprimir_declaracion(dec)
        print("---")
    # main()
```

<details>
<summary>💡 Ver solución</summary>

```python
def construir_declaracion(nit, razon_social, valor_declarado, municipio):
    if valor_declarado >= 10_000_000:
        nivel = "Alto"
    elif valor_declarado >= 5_000_000:
        nivel = "Medio"
    else:
        nivel = "Bajo"
    return {
        "nit": nit,
        "razon_social": razon_social,
        "valor_declarado": valor_declarado,
        "municipio": municipio,
        "estado": "Pendiente",
        "nivel_riesgo": nivel,
    }


def imprimir_declaracion(declaracion):
    for clave, valor in declaracion.items():
        print(f"{clave}: {valor}")


if __name__ == "__main__":
    for monto in [12_500_000, 6_800_000, 950_000]:
        dec = construir_declaracion("900123456-1", "Empresa Ejemplo", monto, "Bogotá")
        imprimir_declaracion(dec)
        print("---")
    # main()
```

</details>

🔁 **Ciclo git**

```bash
git add .
git commit -m "Sesión: diccionarios — acceso, cálculos y construcción dinámica"
git push
```
---

## 2. De NumPy a pandas: Series y DataFrame
**1. Agrega las dependencias a `requirements.txt`**

Abre el archivo `requirements.txt` y agrega estas dos líneas:

```
pandas
openpyxl
```

**2. Activa el ambiente virtual**

En la terminal, desde la raíz del proyecto:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Cuando el ambiente está activo, verás el nombre del entorno al inicio de la línea del prompt: `(.venv)`.

**3. Instala las dependencias**

Con el ambiente virtual activo, ejecuta:

```bash
pip install -r requirements.txt
```

**4. Agrega los imports al inicio de `main.py`**

Abre `main.py` y agrega estas dos líneas al bloque de imports, junto con las demás que ya están comentadas:

```python
import numpy as np
import pandas as pd
```

Estas líneas van siempre activas (sin comentar), porque `numpy` y `pandas` se usan en las funciones de exploración y prueba desde el inicio de la sesión, no solo en los módulos de `src/`.

### ¿Por qué pandas?

NumPy resolvió un problema enorme: operaciones matemáticas rápidas sobre arrays de números. Sin embargo, los datos reales rara vez son solo números en una rejilla uniforme. Tienen columnas con nombres descriptivos, filas con identificadores propios, valores faltantes, mezcla de tipos (texto en unas columnas, números en otras, fechas en otras), y estructuras que se asemejan más a una tabla de base de datos que a una matriz matemática. NumPy no fue diseñado para eso, y trabajar con datos tabulares usando solo NumPy requería código difícil de leer y propenso a errores.

Wes McKinney creó pandas en 2008 mientras trabajaba en AQR Capital Management, un fondo de inversión cuantitativo en Nueva York. Necesitaba analizar series de precios financieros en Python con la misma comodidad que ofrecía R (el lenguaje estadístico de referencia en ese momento) o una hoja de cálculo, pero con la velocidad de NumPy y la flexibilidad de Python. La primera versión pública apareció en 2009. Hoy pandas es la librería de análisis de datos más descargada del ecosistema Python, presente en bancos, laboratorios farmacéuticos, agencias gubernamentales, plataformas de comercio electrónico y científicos de datos de todo el mundo.

El nombre es una contracción de **"panel data"**, un término de econometría para datasets que observan las mismas entidades (empresas, países, contribuyentes) en múltiples periodos de tiempo. Ese era el caso de uso original: series de precios para múltiples instrumentos financieros en múltiples fechas. Con el tiempo pandas se generalizó para cualquier tipo de datos tabulares.

Pandas agrega sobre NumPy:
- **Columnas con nombres**: en lugar de acceder a `arr[:, 2]` (la tercera columna de un array), escribes `df["valor_declarado"]`. El nombre de la columna es la clave de acceso, no su posición.
- **Índices explícitos**: cada fila tiene una etiqueta que viaja con ella cuando filtras, ordenas o combinas DataFrames. No hay que rastrear manualmente en qué posición quedó cada registro.
- **Soporte nativo para valores faltantes**: NumPy no tiene una forma estándar de representar "este dato no existe". pandas usa `NaN` (Not a Number) y ofrece funciones para detectarlo y manejarlo.
- **Lectura y escritura de archivos**: `pd.read_csv()`, `df.to_excel()` — en una sola línea lo que en NumPy requeriría varias.
- **Operaciones de agrupación, combinación y pivote**: similares a SQL, o tablas dinámicas de Excel pero en Python.

En la práctica, NumPy y pandas se usan juntos: pandas almacena sus datos internamente en arrays de NumPy, y funciones de NumPy como `np.where` operan sobre columnas de pandas sin necesidad de conversión. La línea `import numpy as np` junto a `import pandas as pd` es la combinación estándar en cualquier script de análisis de datos.

---

### Series

En la sesión anterior trabajaste con arrays de NumPy: una estructura que guarda valores en orden y te permite acceder a ellos por posición (`arr[0]`, `arr[1]`). El índice de un array siempre es numérico: 0, 1, 2…

Una **Series** de pandas agrega la posibilidad de ponerle una etiqueta propia a cada valor, en vez de depender solo de la posición. 
Eso es lo que significa "índice nombrado": en lugar de referirte al tercer elemento como `serie[2]`, puedes referirte a él por un NIT, una fecha o cualquier identificador que tenga sentido para tus datos. 
El acceso por posición sigue funcionando y la etiqueta también llamado `index` es un camino adicional.

```python
import numpy as np
import pandas as pd

valores = np.array([4_500_000, 12_300_000, 2_100_000])
serie = pd.Series(valores, index=["900123456-1", "800234567-0", "700345678-9"])

print(serie)
# 900123456-1     4500000
# 800234567-0    12300000
# 700345678-9     2100000
# dtype: int64
```

Lo que ves al imprimir: la columna izquierda es el **index** (los NITs que asignaste), la columna derecha son los valores, y `dtype: int64` es el tipo de dato que pandas infirió.

Cda valor queda relacionado a su index. Si filtras la Serie para quedarte solo con algunos registros, pandas no renumera desde cero; conserva el NIT original junto con el valor. Eso evita que al combinar dos Series se mezclen filas equivocadas: pandas une por index (index), no por posición.

Las series también tienen métodos para calcular estadísticas básicas sobre los valores, como suma, promedio, máximo y mínimo.
A continuación, algunos ejemplos de uso:

```python
print(serie["800234567-0"])  # → 12300000
print(serie.mean())          # → 6300000.0
print(serie.sum())           # → 18900000
print(serie.max())           # → 12300000
print(serie.idxmax())        # → '800234567-0'  (index del valor máximo)
```

`.idxmax()` retorna el índice (el index, no la posición) donde está el valor máximo. Útil cuando el índice es un NIT o un identificador y quieres saber a qué registro corresponde el máximo sin tener que recorrer la Serie manualmente.

> Si conoces los diccionarios, la Series puede parecerte similar: ambas asocian una etiqueta con un valor. 
> La diferencia está en lo que puedes hacer después. 
> Un diccionario es una estructura de búsqueda: lo recorres, accedes por clave, actualizas valores. 
> Una Serie es una estructura de cálculo: puedes sumar todas las declaraciones con .sum(), calcular el promedio con .mean(), encontrar el máximo con .max(), y hacerlo sobre toda la columna en una sola operación sin escribir ciclos. 
> Además, cuando filtras una Serie o la combinas con otra, pandas alinea los valores por index automáticamente — algo que con un diccionario tendrías que hacer a mano. 
> La Serie es la evolución cuando necesitas además de guardar datos con nombre operar sobre ellos.

### DataFrame

Un **DataFrame** es una tabla, igual a las que manejas en Excel. Tiene cuatro partes:

- **Columnas**: cada campo de datos tiene un nombre. En el ejemplo de abajo serían `nit`, `municipio`, `valor_declarado` y `estado`.
- **Filas**: cada registro. Para el ejmplo, una fila es una declaración completa de un contribuyente.
- **Celdas**: el valor en la intersección de una columna y una fila. Por ejemplo, el valor `4500000` en la columna `valor_declarado` de la primera fila es una celda.
- **Índice de filas**: el index que identifica cada fila. Si no defines uno, pandas asigna números enteros desde cero (0, 1, 2…) automáticamente.

Las columnas son la pieza central del DataFrame. Todo lo que haces con los datos pasa por ellas: accedes a una columna por su nombre (`df["valor_declarado"]`), calculas sobre ella, la filtras, la transformas y la exportas. El nombre de la columna no es solo una etiqueta visual: es la clave con la que el código la identifica en cualquier parte del programa. Si el nombre cambia en el archivo fuente, el código que depende de ese nombre falla.

El orden de las columnas también importa. Cuando exportas a CSV o Excel, las columnas aparecen en el orden en que están en el DataFrame. Un archivo donde la primera columna es `identificador_periodo` y la segunda es `nit` comunica algo distinto a uno donde esas columnas están al final. Controlar ese orden antes de exportar es parte del trabajo de preparación de datos.

Para construir un DataFrame desde código pasas un diccionario: cada clave es el nombre de una columna y cada lista corresponde a los valores de esa columna, uno por fila:

```python
datos = {
    "nit": ["900123456-1", "800234567-0", "700345678-9"],
    "municipio": ["Bogotá", "Cali", "Medellín"],
    "valor_declarado": [4_500_000, 12_300_000, 2_100_000],
    "estado": ["Presentada", "Presentada", "Pendiente"],
}

df = pd.DataFrame(datos)
print(df)

#            nit  municipio  valor_declarado     estado   ← nombres de columna
# 0  900123456-1     Bogotá          4500000  Presentada  ← fila 0
# 1  800234567-0       Cali         12300000  Presentada  ← fila 1
# 2  700345678-9   Medellín          2100000   Pendiente  ← fila 2
# ↑
# índice de filas (asignado automáticamente)
```
Cada columna es internamente una Serie, así que las operaciones que viste en la sección anterior funcionan igual sobre columnas del DataFrame. Puedes verificarlo:

```python
print(type(df["valor_declarado"]))
# <class 'pandas.core.series.Series'>
```

Trabajando con DataFrames vas a encontrar tres formas distintas de interactuar con ellos, y es fácil confundirlas porque se ven parecidas.

- **Funciones independientes** como `pd.read_csv()` no pertenecen a ningún DataFrame: viven en el módulo `pd`, reciben argumentos entre paréntesis y devuelven un DataFrame nuevo. Las llamas antes de tener el objeto.

- **Atributos** como `df.shape` o `df.columns` son propiedades que el DataFrame ya tiene calculadas. Se leen sin paréntesis porque no ejecutan nada, más bien permiten acceder a un valor que ya existe.

- **Métodos** como `df.info()` o `df.describe()` sí llevan paréntesis porque ejecutan una operación sobre el DataFrame en el momento en que los llamas.

> Un error común es escribir `df.shape()` con paréntesis. Python interpreta eso como "llama a `shape` como si fuera una función" y lanza `TypeError: 'tuple' object is not callable` porque `shape` no es una función sino un valor que ya está ahí.

`df.shape` devuelve una tupla con dos números: `(filas, columnas)`. En el ejemplo, `(3, 4)` significa que el DataFrame tiene 3 filas y 4 columnas. 

Para saber cuántos registros tiene el DataFrame puedes usar `df.shape[0]`, que accede al primer elemento de la tupla, o `len(df)`, que hace lo mismo de forma más directa. Cualquiera de las dos formas es válida:

```python
print(df.shape[0])  # → 3  (número de filas)
print(df.shape[1])  # → 4  (número de columnas)
print(len(df))      # → 3  (equivalente a df.shape[0])
```

`len(df)` es la forma más común cuando solo necesitas el conteo de filas, por ejemplo para verificar cuántos registros cargaste o cuántos quedaron después de un filtro.

```python
print(df.shape)    # → (3, 4)   ← atributo: tupla (filas, columnas)
print(df.index)    # → RangeIndex(start=0, stop=3, step=1)
print(df.columns)  # → Index(['nit', 'municipio', 'valor_declarado', 'estado'], dtype='object')
print(df.values)
# [['900123456-1' 'Bogotá' 4500000 'Presentada']
#  ['800234567-0' 'Cali' 12300000 'Presentada']
#  ['700345678-9' 'Medellín' 2100000 'Pendiente']]
print(df.dtypes)
# nit                object
# municipio          object
# valor_declarado     int64
# estado             object
# dtype: object
```

`.values` devuelve los datos del DataFrame como un array de NumPy, sin los nombres de columna ni el índice. Es útil cuando necesitas pasar los datos a una función que espera un array.

```python
df.info()              # ← imprime internamente; no necesita print()
print(df.describe())   # ← retorna un DataFrame; sí necesita print()
```

* `df.info()` imprime un reporte de la estructura del DataFrame: cuántas filas tiene, qué columnas existen, qué tipo de dato tiene cada una y cuántos valores no nulos hay por columna. Conviene llamarlo justo después de cargar un archivo — en una sola pantalla muestra si los tipos quedaron bien asignados y si hay columnas con datos faltantes.

* `df.describe()` opera sobre las columnas numéricas y calcula ocho estadísticas por cada una: cantidad de valores no nulos, promedio, desviación estándar, mínimo, máximo y los tres cuartiles (25 %, 50 % y 75 %). Con ese reporte puedes ver si el mínimo de `valor_declarado` es negativo, si el máximo está muy por encima del promedio, o si la mediana (50 %) difiere mucho del promedio — lo que indicaría valores extremos que jalan la media hacia arriba o hacia abajo.

> `df.info()` describe la **estructura** del DataFrame (tipos, nulos, dimensiones); `df.describe()` describe el **contenido numérico** (rangos, dispersión, distribución). Usados juntos cubren el diagnóstico inicial de cualquier dataset.
---

### Ejercicios

> **Reto para quienes van adelantados:** en lugar de llamar cada función por separado, escribe un menú en el bloque `__main__` que le pregunte al usuario qué quiere explorar — Series, DataFrame o ambos — y llame la función correspondiente. 

#### Inducción al error

En `main.py`, escribe esta función e insértala justo antes del bloque `if __name__ == '__main__':`. 
Llámala dentro del bloque `__main__` para probarla. Comenta el código del menú mientras pruebas la función

```python
def probar_acceso_serie():
    serie = pd.Series([100, 200, 300])
    print(serie[5])

if __name__ == "__main__":
    probar_acceso_serie()
    # main()  ← comentado mientras probamos
```

¿Qué pasa si accedes a una posición que no existe? ¿Qué tipo de error aparece?

Cuando termines, vuelve a dejar `main()` activo y comenta o elimina la llamada a `probar_acceso_serie()`.

#### Básico

📂 `main.py`

Escribe una función `explorar_dataframe()` que construya un DataFrame con datos de cuatro contribuyentes, cada fila con los campos `nit`, `razon_social`, `municipio` y `valor_declarado`, e imprima `.index`, `.columns` y `.shape`.

La salida esperada es:

```bash
RangeIndex(start=0, stop=4, step=1)
Index(['nit', 'razon_social', 'municipio', 'valor_declarado'], dtype='object')
(4, 4)
```

Llama la función desde el bloque `__main__` para verificar que la salida coincide:

```python
if __name__ == "__main__":
    explorar_dataframe()
    # main()
```

<details>
<summary>💡 Ver solución</summary>

```python
def explorar_dataframe():
    datos = {
        "nit": ["900123456-1", "800234567-0", "700345678-9", "600456789-8"],
        "razon_social": ["Empresa A", "Empresa B", "Empresa C", "Empresa D"],
        "municipio": ["Bogotá", "Cali", "Medellín", "Barranquilla"],
        "valor_declarado": [4_500_000, 12_300_000, 2_100_000, 8_750_000],
    }
    df = pd.DataFrame(datos)
    print(df.index)
    print(df.columns)
    print(df.shape)


if __name__ == "__main__":
    explorar_dataframe()
    # main()
```

</details>

#### Intermedio

📂 `main.py`

Escribe una función `analizar_serie(nits, valores)` que reciba una lista de NITs y una lista de valores declarados, construya una Serie usando los NITs como índice, e imprima la media, el máximo, el mínimo y el NIT con el valor más alto usando las funciones que la liberería tiene definidas

La salida esperada para estos datos:

```python
nits   = ["900111222-0", "800333444-5", "700555666-1", "600777888-2", "500999000-3"]
valores = [4_500_000, 12_300_000, 2_100_000, 8_750_000, 15_200_000]
```

es:
```bash
Media:        8570000.0
Máximo:       15200000
Mínimo:       2100000
NIT con mayor valor: 500999000-3
```

Llama la función desde el bloque `__main__`:

```python
if __name__ == "__main__":
    analizar_serie(nits, valores)
    # main()
```

<details>
<summary>💡 Ver solución</summary>

```python
def analizar_serie(nits, valores):
    serie = pd.Series(valores, index=nits)
    print(f"Media:        {serie.mean()}")
    print(f"Máximo:       {serie.max()}")
    print(f"Mínimo:       {serie.min()}")
    print(f"NIT con mayor valor: {serie.idxmax()}")


if __name__ == "__main__":
    nits    = ["900111222-0", "800333444-5", "700555666-1", "600777888-2", "500999000-3"]
    valores = [4_500_000, 12_300_000, 2_100_000, 8_750_000, 15_200_000]
    analizar_serie(nits, valores)
    # main()
```

</details>

#### Avanzado

📂 `main.py`

Escribe una función `construir_dataframe(lista_declaraciones)` que reciba una lista de diccionarios y retorne un DataFrame. Dentro de la función, verifica que el número de filas del DataFrame resultante coincide con el número de elementos de la lista e imprime ambos números para confirmarlo.

```python
declaraciones = [
    {"nit": "900111222-0", "razon_social": "Empresa A", "valor_declarado": 4_500_000},
    {"nit": "800333444-5", "razon_social": "Empresa B", "valor_declarado": 12_300_000},
    {"nit": "700555666-1", "razon_social": "Empresa C", "valor_declarado": 2_100_000},
]
```

La salida esperada es:

```bash
Elementos en la lista: 3
Filas en el DataFrame: 3
```

Llama la función desde el bloque `__main__`:

```python
if __name__ == "__main__":
    construir_dataframe(declaraciones)
    # main()
```

<details>
<summary>💡 Ver solución</summary>

```python
def construir_dataframe(lista_declaraciones):
    df = pd.DataFrame(lista_declaraciones)
    print(f"Elementos en la lista: {len(lista_declaraciones)}")
    print(f"Filas en el DataFrame: {len(df)}")
    return df


if __name__ == "__main__":
    declaraciones = [
        {"nit": "900111222-0", "razon_social": "Empresa A", "valor_declarado": 4_500_000},
        {"nit": "800333444-5", "razon_social": "Empresa B", "valor_declarado": 12_300_000},
        {"nit": "700555666-1", "razon_social": "Empresa C", "valor_declarado": 2_100_000},
    ]
    construir_dataframe(declaraciones)
    # main()
```

</details>

🔁 **Ciclo git**

```bash
git add .
git commit -m "Sesión: Series y DataFrame — construcción e inspección de atributos"
git push
```

---

## 3. Carga de datos con pd.read_csv()

Construir el DataFrame manualmente funciona para ejemplos pequeños. Con un archivo de miles de filas usas `pd.read_csv()`. La carga más simple es:

```python
df = pd.read_csv("data/inputs/declaraciones_iva_2025.csv")
```

Imprime las primeras filas para verificar que cargó bien:

```python
print(df.head())
#            nit                    razon_social municipio  codigo_municipio  periodo  valor_declarado  valor_pagado      estado  actividad_economica
# 0  900123456-1   Comercializadora Andina S.A.S    Bogotá             11001   202401          4500000       4500000  Presentada                 4711
# 1  800234567-0    Distribuidora del Valle Ltda      Cali             76001   202401         12300000      12300000  Presentada                 4641
# 2  700345678-9    Inversiones Ríos y Ríos S.A  Medellín              5001   202401          2100000             0   Pendiente                 6810
# ...
```

Ahora revisa los tipos de dato que pandas infirió:

```python
print(df.dtypes)
# nit                      object
# razon_social             object
# municipio                object
# codigo_municipio          int64   ← problema potencial
# periodo                   int64
# valor_declarado           int64
# valor_pagado              int64
# estado                   object
# actividad_economica       int64
```

`codigo_municipio` quedó como `int64`. En este archivo el código `11001` es correcto, pero en datasets donde un municipio tiene código `05001` (Medellín), pandas lo lee como `5001` y el cero a la izquierda desaparece. El parámetro `dtype` corrige eso al momento de carga, antes de que ocurra el problema:

```python
df = pd.read_csv(
    "data/inputs/declaraciones_iva_2025.csv",
    dtype={"nit": str, "codigo_municipio": str},
)

print(df["codigo_municipio"].dtype)    # → object
print(df["codigo_municipio"].iloc[0])  # → '11001'  (cadena, no entero)
# .iloc[0] accede a la primera fila por posición (índice 0).
# Es la forma de revisar un valor concreto sin imprimir toda la columna.
```

Si solo necesitas parte de las columnas, `usecols` le dice a pandas qué leer. En archivos grandes esto reduce el tiempo de carga y la memoria usada; en archivos pequeños como el de esta sesión el efecto es menor:

```python
df_reducido = pd.read_csv(
    "data/inputs/declaraciones_iva_2025.csv",
    dtype={"nit": str, "codigo_municipio": str},
    usecols=["nit", "razon_social", "municipio", "valor_declarado", "estado"],
)

print(df.shape)           # → (20, 9)
print(df_reducido.shape)  # → (20, 5)
```

⚠️ Si el archivo tiene tildes o la `ñ` y ves texto ilegible (`RazÃ³n Social` en lugar de `Razón Social`), el problema es el encoding. Prueba con `encoding="latin-1"` o `encoding="cp1252"`. Los archivos exportados desde Excel en Windows casi siempre usan `cp1252`.

⚠️ Si el archivo tiene tildes o la `ñ` y ves texto ilegible (`RazÃ³n Social` en lugar de `Razón Social`), el problema es el **encoding** — la forma en que el archivo convierte caracteres a bytes. 

Distintos sistemas y programas usan convenciones distintas: `utf-8` es el estándar moderno y el que Python usa por defecto, pero Excel en Windows históricamente guarda los archivos con `cp1252` (también llamado `latin-1`), que representa los caracteres del español de forma diferente. 
Cuando pandas intenta leer un archivo `cp1252` como si fuera `utf-8`, los caracteres especiales aparecen corruptos. 
La solución es indicarle explícitamente el encoding correcto:

```python
df = pd.read_csv("archivo.csv", encoding="latin-1")
# o equivalentemente:
df = pd.read_csv("archivo.csv", encoding="cp1252")
```

> Si no sabes qué encoding tiene un archivo, `latin-1` es un buen primer intento para archivos exportados desde Excel en Windows. Para archivos generados por sistemas modernos o descargados de portales web, `utf-8` suele ser el correcto, y como es el valor por defecto de pandas, en esos casos no necesitas especificar nada.
---

### Ejercicios

#### Inducción al error

En `main.py`, escribe esta función e insértala justo antes del bloque `if __name__ == '__main__':`. La llamada al final del bloque se ejecuta al correr el script, antes del menú:

```python
def probar_carga_archivo():
    df = pd.read_csv("data/inputs/archivo_inexistente.csv")

probar_carga_archivo()
```

¿Qué dice el error? ¿Qué información te da para encontrar el problema?

#### Básico

📂 `src/data_loader.py`

Abre el archivo y reemplaza el `pass` de `cargar_declaraciones()` con una primera versión: carga el archivo con `pd.read_csv(ruta)` y retorna el DataFrame. No te preocupes todavía por `dtype` ni `columnas`.

Para probar sin pasar por el menú, el bloque `if __name__ == "__main__":` ya existe al final del archivo. En esta etapa puede quedar así:

```python
if __name__ == "__main__":
    df = cargar_declaraciones("data/inputs/declaraciones_iva_2025.csv")
    print(df.shape)
    print(df.head())
```

```bash
python src/data_loader.py
```

La salida esperada es:

```
(20, 9)
           nit                    razon_social municipio  ...
0  900123456-1   Comercializadora Andina S.A.S    Bogotá  ...
```

<details>
<summary>💡 Ver solución</summary>

```python
def cargar_declaraciones(ruta, columnas=None):
    df = pd.read_csv(ruta)
    return df
```

</details>

#### Intermedio

📂 `src/data_loader.py`

Extiende `cargar_declaraciones()` con dos mejoras:

1. Agrega `dtype={"nit": str, "codigo_municipio": str}` para que esas columnas siempre lleguen como texto.
2. Si `columnas` no es `None`, úsala como `usecols` en `pd.read_csv()`. Si es `None`, carga todas las columnas.

Actualiza el bloque `if __name__ == "__main__":` para probar las dos variantes:

```python
if __name__ == "__main__":
    df_completo = cargar_declaraciones("data/inputs/declaraciones_iva_2025.csv")
    df_reducido = cargar_declaraciones(
        "data/inputs/declaraciones_iva_2025.csv",
        columnas=["nit", "valor_declarado", "estado"],
    )
    print("Completo:", df_completo.shape)
    print("Reducido:", df_reducido.shape)
    print("Tipo de nit:", df_completo["nit"].dtype)  # → object
```

La salida esperada es:

```
Completo: (20, 9)
Reducido: (20, 3)
Tipo de nit: object
```

<details>
<summary>💡 Ver solución</summary>

```python
def cargar_declaraciones(ruta, columnas=None):
    if columnas is not None:
        df = pd.read_csv(
            ruta,
            dtype={"nit": str, "codigo_municipio": str},
            usecols=columnas,
        )
    else:
        df = pd.read_csv(
            ruta,
            dtype={"nit": str, "codigo_municipio": str},
        )
    return df
```

</details>

#### Avanzado

📂 `main.py` — la función ya funciona; ahora conéctala al menú.

Descomenta el import de la Sección 3 y completa la opción 1:

```python
# En el bloque de imports, descomenta:
from src.data_loader import cargar_declaraciones

# Dentro de if opcion == "1":
df = cargar_declaraciones(RUTA_DATOS)
print(f"Filas cargadas: {len(df)}")
```

La salida esperada al elegir la opción 1 es:

```
Filas cargadas: 20
```

<details>
<summary>💡 Ver solución</summary>

```python
# En el bloque de imports (descomenta):
from src.data_loader import cargar_declaraciones

# Dentro de elif opcion == "1":
elif opcion == "1":
    df = cargar_declaraciones(RUTA_DATOS)
    print(f"Filas cargadas: {len(df)}")
```

</details>

🔁 **Ciclo git**

```bash
git add .
git commit -m "Sesión: carga de datos con pd.read_csv() implementada"
git push
```

---

> ▶ **Pausa — 15 minutos**

---

## 4. Inspección del conjunto de datos

Cada vez que recibes un archivo de datos nuevo, el primer trabajo es entender qué hay ahí antes de calcular nada. No importa si el archivo viene de un sistema interno, de un proveedor externo o de una descarga del portal de datos abiertos: siempre puede haber sorpresas. Estos seis pasos forman un protocolo que puedes aplicar sistemáticamente, independientemente del archivo o del dominio. Ejecutarlos antes de cualquier transformación te ahorra el tiempo que cuesta corregir un análisis hecho sobre datos malentendidos.

### Paso 1: verificar que la carga funcionó

```python
print(df.shape)      # (filas, columnas)
print(df.head())     # primeras 5 filas
print(df.tail())     # últimas 5 filas
print(df.sample(5))  # 5 filas aleatorias
```

La pregunta central de este paso es: ¿el DataFrame que cargaste coincide con el archivo que esperabas? Revisa el número de filas contra la fuente, comprueba que los encabezados de columna son los correctos y confirma que los valores se ven como datos reales (no como errores de encoding o separadores mal interpretados).

`head()` y `tail()` solo muestran los extremos. Si el archivo está ordenado o tiene un patrón (por ejemplo, todas las declaraciones pendientes al inicio), los extremos pueden no ser representativos. `sample(5)` elige filas al azar y da una visión más equilibrada del conjunto.

Si `df.head()` muestra todo en una sola columna larga en lugar de varias columnas separadas, el problema casi siempre es el separador: el archivo usa `;` o `\t` en lugar de `,`. En ese caso, pasa el argumento `sep=";"` o `sep="\t"` a `pd.read_csv()`.

### Paso 2: revisar tipos de dato

```python
print(df.dtypes)
df.info()
```

pandas asigna un tipo de dato a cada columna durante la carga, basándose en los valores que encuentra. El problema es que esa inferencia automática no siempre produce el tipo correcto para tu caso de uso.

Los tipos más comunes son `int64` (entero), `float64` (decimal), `object` (texto o mezcla) y `bool` (verdadero/falso). El tipo `object` merece atención especial: es el tipo genérico de pandas para columnas de texto, pero también aparece cuando una columna numérica tiene valores faltantes o valores mixtos que Python no pudo interpretar de forma consistente.

Lo que importa es pensar en qué operaciones necesitas sobre cada columna. Un NIT leído como `int64` ya perdió el guion y posiblemente los ceros a la izquierda. Una fecha leída como `object` no se puede ordenar cronológicamente ni calcular diferencias de días. Un código de municipio como `05001` leído como entero se convierte en `5001`, rompiendo cualquier cruce posterior con tablas de referencia geográfica. Detectar estos problemas aquí, antes de cualquier cálculo, evita errores silenciosos: errores que no lanzan excepción pero producen resultados incorrectos.

`df.info()` complementa `df.dtypes` porque también muestra cuántos valores no nulos tiene cada columna. Si una columna tiene 18 valores no nulos en un DataFrame de 20 filas, hay 2 nulos, incluso si `dtypes` no lo indica.

### Paso 3: detectar valores faltantes

```python
df.isnull().sum()
```

Un valor faltante en pandas se representa como `NaN` (Not a Number), un valor especial del estándar IEEE 754 para aritmética de punto flotante. `NaN` no es cero, no es una cadena vacía, no es `None` — es la ausencia de un valor. Pandas hereda `NaN` de NumPy y lo usa de forma consistente para representar celdas vacías, independientemente del tipo de la columna.

`isnull()` devuelve un DataFrame de booleanos del mismo tamaño que el original: `True` donde hay `NaN`, `False` donde hay un valor. Aplicar `.sum()` sobre ese DataFrame suma los `True` (que valen 1) por columna:

```python
df.isnull().sum()
# nit                    0
# razon_social           0
# municipio              0
# codigo_municipio       0
# periodo                0
# valor_declarado        2   ← dos filas sin valor en esta columna
# valor_pagado           0
# estado                 1
# actividad_economica    0
# dtype: int64
```

Para saber si hay algún nulo en todo el DataFrame en un solo número:

```python
df.isnull().sum().sum()
```

El primer `.sum()` produce una Serie (un número de nulos por columna). El segundo `.sum()` suma esa Serie y da el total de celdas vacías en todo el DataFrame. Si el resultado es `0`, no hay nulos en ninguna parte.

Para verificar columnas específicas sin leer el reporte completo:

```python
df["nit"].isnull().sum()              # nulos en nit
df["valor_declarado"].isnull().sum()  # nulos en valor_declarado
```

Lo que importa en este paso es interpretar los nulos en contexto. Un nulo en `nit` es un problema grave: sin identificador, no puedes relacionar esa fila con ningún contribuyente. Un nulo en `valor_declarado` puede significar que la declaración no tiene monto (quizás fue anulada) o que hubo un error de digitación. Un nulo en una columna calculada que tú mismo vas a agregar es esperado antes de que la calcules. Anotar cuáles columnas tienen faltantes y cuántos, antes de operar, evita que esos nulos se propaguen silenciosamente a los resultados.

⚠️ Las operaciones aritméticas sobre `NaN` producen `NaN`: `NaN + 5` es `NaN`, no `5`. Si tienes nulos en `valor_declarado` y calculas `df["valor_declarado"].sum()`, el resultado puede ser incorrecto si no los manejaste antes.

### Paso 4: detectar duplicados

```python
print(df.duplicated().sum())
```

`df.duplicated()` recorre las filas de arriba hacia abajo y marca como `True` cada fila que es una copia exacta de alguna fila anterior. La primera ocurrencia de un registro siempre queda como `False`; las repeticiones quedan como `True`. `.sum()` cuenta cuántas filas están repetidas.

```python
print(df.duplicated())
# 0     False
# 1     False
# ...
# 19    False
# dtype: bool
```

Si quisieras que también la primera ocurrencia quedara marcada (para ver todos los registros involucrados en la duplicación, no solo los repetidos), usarías `df.duplicated(keep=False)`. Para el protocolo de inspección básico, el comportamiento por defecto es suficiente.

Los duplicados en datos reales pueden tener varias causas. Los más comunes son: errores en el proceso de exportación del sistema fuente que generó el archivo (el mismo registro se incluyó dos veces), errores de integración si el archivo proviene de la combinación de dos fuentes, o simplemente el hecho esperado de que el mismo contribuyente aparezca en varios periodos — en cuyo caso las filas no son duplicadas reales sino repeticiones legítimas. Por eso, antes de eliminar duplicados, vale preguntarse por qué están.

### Paso 5: explorar columnas categóricas

```python
df["estado"].value_counts()    # conteo por categoría
df["municipio"].nunique()      # número de valores distintos
df["municipio"].value_counts() # distribución de municipios
```

Las columnas categóricas son las que tienen un número limitado de valores distintos posibles: `estado` (Presentada, Pendiente, Rechazada), `municipio`, `actividad_economica`. `value_counts()` muestra cuántas filas pertenecen a cada categoría, ordenadas de mayor a menor.

Esto es útil por dos razones. Primero, para verificar que los valores son los esperados: si esperas `"Presentada"` y `"Pendiente"` pero `value_counts()` muestra además `"presentada"` (minúscula) o `"Presentadas"` (con "s"), esas son categorías distintas para pandas aunque representen lo mismo. Cualquier filtro o agrupación posterior que use ese campo producirá resultados incompletos. Segundo, para detectar valores raros: un valor que aparece solo una o dos veces en un campo que debería tener categorías bien definidas suele ser un error de digitación o de exportación.

`nunique()` devuelve el número de valores distintos sin listarlos. Útil para columnas con muchas categorías como `municipio` o `actividad_economica`, donde `value_counts()` produciría una lista muy larga.

### Paso 6: revisar distribución de columnas numéricas

```python
print(df.describe())
#        codigo_municipio       periodo  valor_declarado  valor_pagado  actividad_economica
# count          20.000000     20.00000        20.000000     20.000000            20.000000
# mean        43751.300000  202401.00000   9060000.000000   7192500.000000         5020.150000
# std         30211.987310       0.00000   8021553.678000   7891234.000000         1823.456789
# min         05001.000000  202401.00000    850000.000000         0.000000         1010.000000
# 25%         11001.000000  202401.00000   2662500.000000         0.000000         4641.000000
# 50%         50001.000000  202401.00000   6875000.000000   5750000.000000         4711.000000
# 75%         76001.000000  202401.00000  13575000.000000  12975000.000000         6810.000000
# max         76001.000000  202401.00000  31200000.000000  31200000.000000         7523.000000
```

`describe()` calcula ocho estadísticas por cada columna numérica. Entender qué significa cada una te permite leer la tabla con criterio:

- **count**: cuántos valores no nulos hay. Si es menor que el número de filas del DataFrame, hay nulos en esa columna — complementa el paso 3.
- **mean**: el promedio. Sensible a valores extremos: un solo registro con un valor inusualmente alto sube el promedio de toda la columna.
- **std** (desviación estándar): qué tan dispersos están los valores alrededor del promedio. Una `std` grande relativa al `mean` indica mucha variación entre registros; una `std` de cero significa que todos los valores son iguales (como `periodo` en este dataset, donde todos son 202401).
- **min / max**: el valor mínimo y el máximo. Un `min` negativo en una columna de valores declarados sería un error; un `max` de varios órdenes de magnitud por encima del `mean` puede indicar un valor atípico o un error de digitación.
- **25%, 50%, 75%** (cuartiles): el 25% indica que una cuarta parte de los registros tienen un valor por debajo de ese número. El 50% es la **mediana**: exactamente la mitad de los registros están por encima y la mitad por debajo. El 75% indica que tres cuartas partes tienen un valor por debajo. La mediana es más robusta que el promedio ante valores extremos: si hay un registro con un valor declarado de mil millones en un dataset donde todos los demás están entre un millón y veinte millones, la mediana apenas se mueve mientras que el promedio se dispara.

`describe()` solo opera sobre columnas numéricas. Las de tipo `object` no aparecen en el resultado; para ellas usa `value_counts()` como se vio en el paso anterior.

Qué buscar en el resultado: valores mínimos negativos donde el campo debe ser positivo, máximos muy alejados del promedio (posibles errores de digitación o unidades incorrectas), y diferencias grandes entre `mean` y `50%` que indiquen distribuciones asimétricas. En el ejemplo, el promedio de `valor_declarado` es 9 millones pero la mediana es 6.875 millones — la distribución está sesgada hacia arriba por algunos valores altos.

> Estos seis pasos no garantizan que los datos estén correctos, pero sí que conoces los problemas antes de operar sobre ellos. Documentar lo que encontraste — aunque sea en un comentario en el código — es parte del trabajo de análisis.

---

### Ejercicios

#### Inducción al error

En `main.py`, escribe esta función e insértala justo antes del bloque `if __name__ == '__main__':`. La llamada al final del bloque se ejecuta al correr el script, antes del menú:

```python
def probar_atributo_shape():
    df = pd.read_csv("data/inputs/declaraciones_iva_2025.csv")
    print(df.shape())

probar_atributo_shape()
```

¿Por qué falla? ¿Cuál es la diferencia entre `df.shape` y `df.shape()`?

#### Básico

📂 `src/data_loader.py`

Abre el archivo y reemplaza el `pass` de `inspeccionar_datos(df)`. La función debe imprimir un reporte con encabezados:

- Dimensiones (`df.shape`)
- Tipos de dato (`df.dtypes`)
- Nulos por columna (`df.isnull().sum()`)
- Total de celdas vacías (`df.isnull().sum().sum()`)
- Filas duplicadas (`df.duplicated().sum()`)

Actualiza el bloque `if __name__ == "__main__":` del archivo para probarla:

```python
if __name__ == "__main__":
    df = cargar_declaraciones("data/inputs/declaraciones_iva_2025.csv")
    inspeccionar_datos(df)
```

La salida esperada comienza así:

```
=== Dimensiones ===
(20, 9)

=== Tipos de dato ===
nit                object
razon_social       object
municipio          object
...

=== Nulos por columna ===
nit    0
...

=== Total celdas vacías ===
0

=== Filas duplicadas ===
0
```

<details>
<summary>💡 Ver solución</summary>

```python
def inspeccionar_datos(df):
    print("=== Dimensiones ===")
    print(df.shape)
    print("\n=== Tipos de dato ===")
    print(df.dtypes)
    print("\n=== Nulos por columna ===")
    print(df.isnull().sum())
    print("\n=== Total celdas vacías ===")
    print(df.isnull().sum().sum())
    print("\n=== Filas duplicadas ===")
    print(df.duplicated().sum())
```

</details>

🔁 **Ciclo git**

```bash
git add .
git commit -m "Sesión: protocolo de inspección implementado en data_loader"
git push
```

#### Intermedio

📂 `src/data_loader.py`

Extiende `inspeccionar_datos(df)` e implementa `validar_nulos()`.

**1. Extiende `inspeccionar_datos(df)`**

Agrega al reporte: para cada columna de tipo `object`, muestra cuántos valores únicos tiene con `.nunique()`. Si tiene menos de 20, imprime también cuáles son con `.value_counts()`. Si tiene 20 o más, imprime solo la cantidad.

**2. Implementa `validar_nulos(df, columnas_criticas)`**

```python
def validar_nulos(df, columnas_criticas):
    # TODO: Recorre columnas_criticas con un ciclo for.
    # Para cada columna, calcula df[columna].isnull().sum().
    # Si el resultado es mayor que 0, imprime el nombre de la columna
    # y la cantidad de nulos encontrados.
    pass
```

Reemplaza el `pass`. La función recorre la lista de columnas y avisa si alguna tiene nulos — sin detener la ejecución.

Actualiza el bloque de prueba:

```python
if __name__ == "__main__":
    df = cargar_declaraciones("data/inputs/declaraciones_iva_2025.csv")
    inspeccionar_datos(df)
    validar_nulos(df, ["nit", "valor_declarado", "estado"])
```

La salida esperada de `validar_nulos` con el dataset sin nulos es:

```
✓ nit: sin nulos
✓ valor_declarado: sin nulos
✓ estado: sin nulos
```

<details>
<summary>💡 Ver solución</summary>

```python
def inspeccionar_datos(df):
    print("=== Dimensiones ===")
    print(df.shape)
    print("\n=== Tipos de dato ===")
    print(df.dtypes)
    print("\n=== Nulos por columna ===")
    print(df.isnull().sum())
    print("\n=== Total celdas vacías ===")
    print(df.isnull().sum().sum())
    print("\n=== Filas duplicadas ===")
    print(df.duplicated().sum())
    print("\n=== Columnas de texto ===")
    for col in df.select_dtypes(include="object").columns:
        n = df[col].nunique()
        print(f"{col}: {n} valores únicos")
        if n < 20:
            print(df[col].value_counts())


def validar_nulos(df, columnas_criticas):
    for columna in columnas_criticas:
        nulos = df[columna].isnull().sum()
        if nulos > 0:
            print(f"⚠️  {columna}: {nulos} nulos")
        else:
            print(f"✓ {columna}: sin nulos")
```

</details>

🔁 **Ciclo git**

```bash
git add .
git commit -m "Sesión: inspeccionar_datos extendida y validar_nulos implementada"
git push
```

#### Avanzado

📂 `main.py` — las funciones ya funcionan; ahora conéctalas al menú.

Descomenta el import de la Sección 4 y completa la opción 2:

```python
# En el bloque de imports, descomenta:
from src.data_loader import cargar_declaraciones, inspeccionar_datos, validar_nulos

# Dentro de elif opcion == "2":
inspeccionar_datos(df)
validar_nulos(df, COLUMNAS_CRITICAS)
```

La salida esperada al elegir la opción 2 comienza con el mismo reporte de `inspeccionar_datos` seguido de las tres líneas de validación.

<details>
<summary>💡 Ver solución</summary>

```python
# En el bloque de imports (descomenta):
from src.data_loader import cargar_declaraciones, inspeccionar_datos, validar_nulos

# Dentro de elif opcion == "2":
elif opcion == "2":
    if df is None:
        print("Primero carga los datos con la opción 1.")
    else:
        inspeccionar_datos(df)
        validar_nulos(df, COLUMNAS_CRITICAS)
```

</details>

🔁 **Ciclo git**

```bash
git add .
git commit -m "Sesión: inspección del conjunto de datos implementada"
git push
```

#### Extensión: aplica el protocolo a una fuente nueva

Busca un archivo CSV del portal de datos abiertos del gobierno: [datos.gov.co](https://www.datos.gov.co). Descárgalo, guárdalo como `data/inputs/fuente_externa.csv` y aplica los seis pasos del protocolo sobre ese archivo.

1. Carga el archivo con `pd.read_csv()`. Si falla con el encoding por defecto, prueba `encoding="latin-1"`.
2. Ejecuta los seis pasos en orden.
3. Anota en un comentario al final del script al menos dos diferencias que encuentras entre este archivo y `declaraciones_iva_2025.csv`: tipos de dato distintos, columnas con nulos, categorías inesperadas, etc.

No hay una respuesta esperada. El objetivo es aplicar el protocolo sobre datos que no conocías de antemano.

---

## 5. Cálculos y clasificación de registros

### Cálculos sobre columnas numéricas

Las mismas operaciones que usaste sobre arrays de NumPy funcionan sobre columnas de un DataFrame, porque una columna es un array internamente:

```python
print(df["valor_declarado"].sum())   # → 181200000
print(df["valor_declarado"].mean())  # → 9060000.0
print(df["valor_declarado"].max())   # → 31200000
print(df["valor_declarado"].min())   # → 850000
```

Puedes verificar el resultado del `sum()` mentalmente: son 20 declaraciones con un promedio de 9,06 millones, lo que da aproximadamente 181 millones en total.

### Clasificación con np.where

#### Por qué no usamos ciclos `for` para clasificar filas

Imagina que necesitas asignar un texto a cada declaración según su valor declarado. En Python estándar, harías algo así:

```python
etiquetas = []
for valor in df["valor_declarado"]:
    if valor >= 10_000_000:
        etiquetas.append("Alto")
    else:
        etiquetas.append("Bajo")
df["nivel_riesgo"] = etiquetas
```

Esto funciona correctamente. El problema es la velocidad. Python ejecuta el cuerpo del ciclo una vez por fila: con 20 declaraciones eso es trivial, pero con 500.000 declaraciones el ciclo puede tardar varios segundos porque Python tiene un overhead significativo por cada iteración (verificar tipos, reservar memoria para cada valor, manejar el estado del ciclo).

pandas y NumPy ofrecen una alternativa llamada **operación vectorizada**: en lugar de iterar en Python, le pasan toda la columna a una función escrita en C o Fortran (los lenguajes de bajo nivel en que están implementadas estas librerías), que procesa todos los valores de una sola vez, aprovechando instrucciones del procesador diseñadas para operar sobre bloques de datos. El resultado puede ser 10 a 100 veces más rápido que el ciclo equivalente en Python.

>Regla: si puedes expresar una operación como una acción sobre una columna completa — suma, comparación, texto, condición — prefiere la versión vectorizada. El ciclo `for` sobre filas de un DataFrame es casi siempre el camino más lento y generalmente tiene una alternativa en pandas o NumPy.

`np.where` es la herramienta vectorizada para asignar valores según una condición.

Para explorar los ejemplos de esta sección, trabaja directamente en el bloque `if __name__ == "__main__":` de `src/data_transformer.py`. Ese bloque ya carga el dataset y llama a las funciones del módulo; es el lugar correcto para experimentar con `np.where` antes de implementarlo dentro de `clasificar_por_valor()`.

Antes de usar `np.where`, observa qué devuelve una condición sobre una columna:

```python
condicion_alto = df["valor_declarado"] >= 10_000_000
print(condicion_alto.head())
# 0    False
# 1     True
# 2    False
# 3    False
# 4     True
# Name: valor_declarado, dtype: bool
```

El resultado es una Serie de booleanos: un `True` o `False` por cada fila. `np.where` toma esa Serie y asigna un valor de texto a cada posición según el resultado:

```python
df["nivel_riesgo"] = np.where(condicion_alto, "Alto", "Bajo")
print(df[["nit", "valor_declarado", "nivel_riesgo"]].head())
#            nit  valor_declarado nivel_riesgo
# 0  900123456-1          4500000         Bajo
# 1  800234567-0         12300000         Alto
# 2  700345678-9          2100000         Bajo
# 3  600456789-8          8750000         Bajo
# 4  500567890-7         15200000         Alto
```

Para tres categorías, el tercer argumento (el caso "si no") puede ser otro `np.where`:

```python
df["nivel_riesgo"] = np.where(
    df["valor_declarado"] >= 10_000_000,
    "Alto",
    np.where(
        df["valor_declarado"] >= 5_000_000,
        "Medio",
        "Bajo",
    ),
)
```

Verifica el resultado con `value_counts()`:

```python
print(df["nivel_riesgo"].value_counts())
# Bajo     8
# Alto     6
# Medio    6
# Name: nivel_riesgo, dtype: int64
```

El total es 20: todas las filas del dataset recibieron el texto correspondiente. Si el total fuera distinto, habría filas con nulos en `valor_declarado`.

> **Pausa y piensa:** Antes de ejecutar el anidado, estima cuántas declaraciones esperas en cada categoría mirando los valores del archivo. Compara tu estimación con `value_counts()`. Si los números no coinciden, revisa los umbrales.

⚠️ Con más de tres niveles el anidamiento se vuelve difícil de seguir. En ese punto, una función auxiliar aplicada con `.apply()` es más clara.

### Texto con el accesor .str

Para columnas de texto, el accesor **`.str`** da acceso a métodos de cadena que operan sobre toda la columna a la vez. Sin él, tendrías que recorrer fila por fila con un ciclo.

```python
# Pasa a mayúsculas
print(df["razon_social"].str.upper().head(3))
# 0    COMERCIALIZADORA ANDINA S.A.S
# 1     DISTRIBUIDORA DEL VALLE LTDA
# 2       INVERSIONES RÍOS Y RÍOS S.A
# Name: razon_social, dtype: object
```

```python
# Elimina espacios invisibles al inicio y al final (frecuente en archivos exportados)
df["razon_social"] = df["razon_social"].str.strip()
```

```python
# Combina dos columnas de texto para crear un identificador único por declaración
df["identificador_periodo"] = df["nit"] + "_" + df["periodo"].astype(str)
print(df["identificador_periodo"].head(3))
# 0    900123456-1_202401
# 1    800234567-0_202401
# 2    700345678-9_202401
# Name: identificador_periodo, dtype: object
```

`df["periodo"].astype(str)` convierte la columna numérica a texto antes de concatenar. Sin eso, Python lanzaría `TypeError` porque no puede sumar texto con número.

### Selección y reordenamiento de columnas

Para generar una salida con solo las columnas que necesitas, en el orden que necesitas, usas el DataFrame como si fuera un diccionario al que le pides una lista de claves:

```python
columnas_salida = [
    "identificador_periodo",
    "nit",
    "razon_social",
    "municipio",
    "periodo",
    "valor_declarado",
    "nivel_riesgo",
    "estado",
]
df_salida = df[columnas_salida]

print(df_salida.shape)           # → (20, 8)
print(df_salida.columns.tolist())
# ['identificador_periodo', 'nit', 'razon_social', 'municipio',
#  'periodo', 'valor_declarado', 'nivel_riesgo', 'estado']
```

`df_salida` es un nuevo DataFrame. El original `df` no cambia: sigue teniendo las nueve columnas del archivo más las que agregaste durante la transformación.

---

### Ejercicios

#### Inducción al error

En `main.py`, escribe esta función e insértala justo antes del bloque `if __name__ == '__main__':`. La llamada al final del bloque se ejecuta al correr el script, antes del menú:

```python
def probar_np_where():
    df = pd.read_csv("data/inputs/declaraciones_iva_2025.csv")
    df["categoria"] = np.where(df["valor_declarado"] >= 5_000_000, "Alto", "Bajo", "Medio")

probar_np_where()
```

¿Qué dice el error? ¿Por qué `np.where` no acepta tres valores de resultado como argumentos posicionales?

#### Básico

📂 `src/data_transformer.py`

Abre el archivo y reemplaza el `pass` de `clasificar_por_valor()` con una primera versión de dos categorías: `"Alto"` si `valor_declarado >= umbral_alto`, `"Bajo"` en los demás casos.

```python
df["nivel_riesgo"] = np.where(
    df["valor_declarado"] >= umbral_alto,
    "Alto",
    "Bajo",
)
return df
```

El bloque `if __name__ == "__main__":` ya existe al final del archivo. Actualízalo para probar solo `clasificar_por_valor()` en esta etapa:

```python
if __name__ == "__main__":
    df = pd.read_csv(
        "data/inputs/declaraciones_iva_2025.csv",
        dtype={"nit": str, "codigo_municipio": str},
    )
    df = clasificar_por_valor(df, umbral_alto=10_000_000, umbral_medio=5_000_000)
    print(df[["nit", "valor_declarado", "nivel_riesgo"]].head(10))
    print(df["nivel_riesgo"].value_counts())
```

```bash
python src/data_transformer.py
```

La salida esperada es:

```
           nit  valor_declarado nivel_riesgo
0  900123456-1          4500000         Bajo
1  800234567-0         12300000         Alto
...
Bajo    14
Alto     6
```

<details>
<summary>💡 Ver solución</summary>

```python
def clasificar_por_valor(df, umbral_alto, umbral_medio):
    df["nivel_riesgo"] = np.where(
        df["valor_declarado"] >= umbral_alto,
        "Alto",
        "Bajo",
    )
    return df
```

</details>

#### Intermedio

📂 `src/data_transformer.py`

Extiende las tres funciones del módulo.

**1. Agrega la categoría "Medio" a `clasificar_por_valor()`**

El `np.where` externo evalúa la condición más restrictiva. Si no la cumple, el segundo `np.where` evalúa la condición media:

```python
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
```

**2. Implementa `agregar_identificador_periodo(df)`**

```python
def agregar_identificador_periodo(df):
    # TODO: Concatena df["nit"] + "_" + df["periodo"].astype(str).
    # Asigna el resultado a df["identificador_periodo"] y retorna df.
    pass
```

Reemplaza el `pass`. El resultado para la primera fila debería ser `"900123456-1_202401"`.

**3. Implementa `preparar_columnas_salida(df, columnas)`**

```python
def preparar_columnas_salida(df, columnas):
    # TODO: Retorna df[columnas].
    pass
```

Esta función selecciona y reordena columnas en una sola línea. La lista `columnas` define tanto cuáles incluir como el orden en que aparecen en el archivo exportado.

Actualiza el bloque de prueba para verificar las tres funciones:

```python
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
```

La salida esperada es:

```
  identificador_periodo          nit        razon_social  ...  nivel_riesgo     estado
0   900123456-1_202401  900123456-1  Comercializadora...  ...          Bajo  Presentada
...
Bajo     8
Alto     6
Medio    6
```

<details>
<summary>💡 Ver solución</summary>

```python
def clasificar_por_valor(df, umbral_alto, umbral_medio):
    df["nivel_riesgo"] = np.where(
        df["valor_declarado"] >= umbral_alto,
        "Alto",
        np.where(df["valor_declarado"] >= umbral_medio, "Medio", "Bajo"),
    )
    return df


def agregar_identificador_periodo(df):
    df["identificador_periodo"] = df["nit"] + "_" + df["periodo"].astype(str)
    return df


def preparar_columnas_salida(df, columnas):
    return df[columnas]
```

</details>

🔁 **Ciclo git**

```bash
git add .
git commit -m "Sesión: clasificación, identificador y selección de columnas implementados"
git push
```

#### Avanzado

📂 `main.py` — las tres funciones ya funcionan; ahora conéctalas al menú.

Descomenta el import de la Sección 5 y completa la opción 3:

```python
# En el bloque de imports, descomenta:
from src.data_transformer import clasificar_por_valor, agregar_identificador_periodo, preparar_columnas_salida

# Dentro de elif opcion == "3":
df = clasificar_por_valor(df, umbral_alto=10_000_000, umbral_medio=5_000_000)
df = agregar_identificador_periodo(df)
df_salida = preparar_columnas_salida(df, COLUMNAS_SALIDA)
print(df_salida.head())
```

La salida esperada al elegir la opción 3 muestra el DataFrame con las 8 columnas en el orden de `COLUMNAS_SALIDA`.

<details>
<summary>💡 Ver solución</summary>

```python
# En el bloque de imports (descomenta):
from src.data_transformer import clasificar_por_valor, agregar_identificador_periodo, preparar_columnas_salida

# Dentro de elif opcion == "3":
elif opcion == "3":
    if df is None:
        print("Primero carga los datos con la opción 1.")
    else:
        df = clasificar_por_valor(df, umbral_alto=10_000_000, umbral_medio=5_000_000)
        df = agregar_identificador_periodo(df)
        df_salida = preparar_columnas_salida(df, COLUMNAS_SALIDA)
        print(df_salida.head())
```

</details>

#### Libre

📂 `src/data_transformer.py`

Identifica una variable que tenga sentido derivar a partir de los datos disponibles — por ejemplo, la diferencia entre `valor_declarado` y `valor_pagado`, o una clasificación por `actividad_economica`. Escribe la función completa con docstring en `data_transformer.py`, agrégala al bloque `if __name__ == "__main__":`, ejecútala y haz commit.

Ciclo: función con docstring → probar en el bloque `__main__` → import en `main.py` → commit.

🔁 **Ciclo git**

```bash
git add .
git commit -m "Sesión: clasificación y transformación de registros implementada"
git push
```

---

## 6. Exportar resultados

Cuando el análisis termina, los datos transformados tienen que salir del programa de alguna forma
útil: un archivo que otro sistema pueda leer, un Excel que un colega pueda abrir, una tabla que
alimente un dashboard. A ese paso se le llama **exportar** los datos — escribir el contenido de
un DataFrame a un archivo en disco.

pandas ofrece métodos de exportación que son el espejo de los de carga: así como `pd.read_csv()`
trae un CSV a un DataFrame, `df.to_csv()` hace el camino inverso. La misma lógica aplica para
Excel: `pd.read_excel()` carga, `df.to_excel()` exporta. 

Para exportar a Excel, pandas necesita una librería que sepa escribir el formato `.xlsx`:
**openpyxl**. pandas se encarga de la lógica de datos — qué columnas van, en qué orden, en qué
hoja — y openpyxl se encarga del archivo en sí: crear el contenedor `.xlsx`, escribir las celdas
y cerrar el archivo correctamente. La división es transparente para quien escribe el código:
llamas a `df.to_excel()` y pandas invoca openpyxl por debajo sin que tengas que interactuar con
él directamente. Solo necesitas tenerlo instalado; de ahí la línea `openpyxl` en
`requirements.txt` que agregaste al inicio de la sesión.

Los métodos principales que usarás son:

| Método | Qué genera |
|---|---|
| `df.to_csv(ruta)` | Archivo de texto plano con valores separados por coma |
| `df.to_excel(ruta)` | Archivo Excel (.xlsx) con una hoja |
| `pd.ExcelWriter(ruta)` | Contenedor para escribir varias hojas en un mismo Excel |

Los tres reciben `index=False` para evitar que pandas escriba la columna de índice numérico
(0, 1, 2…) como primera columna del archivo — esa columna no tiene significado para quien
recibe el archivo y generaría una columna sin nombre que confunde.

La elección entre CSV y Excel depende de a quién va el archivo.

### CSV

```python
df_salida.to_csv("data/outputs/declaraciones_clasificadas.csv", index=False)
```

`index=False` evita que pandas escriba la columna de índice numérico (0, 1, 2...) como primera columna del archivo. Esa columna no tiene significado fuera del DataFrame y generaría una columna sin nombre que confunde a quien procese el archivo después.

Para incluir la fecha en el nombre y no sobreescribir el archivo de la semana anterior:

> Agrega `from datetime import date` al bloque de imports al inicio de `main.py`, junto con los demás imports. Los imports nunca van dentro de funciones ni a mitad del archivo.

```python
fecha_hoy = date.today().strftime("%Y%m%d")
nombre_archivo = f"declaraciones_clasificadas_{fecha_hoy}.csv"
df_salida.to_csv(f"data/outputs/{nombre_archivo}", index=False)
# Genera, por ejemplo: data/outputs/declaraciones_clasificadas_20250715.csv
```

Después de correr esto, verifica en la carpeta `data/outputs/` que el archivo aparece con el nombre esperado y ábrelo brevemente para confirmar que las columnas están bien.

### Excel con múltiples hojas

Cuando el resultado va a personas que trabajan en Excel, tiene sentido organizar el archivo en hojas por categoría.

`pd.ExcelWriter` actúa como un contenedor: abre el archivo, escribe todas las hojas dentro del bloque `with`, y lo cierra al salir. El archivo queda completo solo cuando el bloque termina.

```python
ruta_excel = f"data/outputs/declaraciones_{fecha_hoy}.xlsx"

with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
    df_salida.to_excel(writer, sheet_name="Todos", index=False)

    # df_salida[df_salida["nivel_riesgo"] == "Alto"] filtra las filas donde
    # la columna "nivel_riesgo" es exactamente "Alto". El resultado es un
    # DataFrame nuevo con solo esas filas.
    df_alto = df_salida[df_salida["nivel_riesgo"] == "Alto"]
    df_alto.to_excel(writer, sheet_name="Riesgo_Alto", index=False)

    df_medio = df_salida[df_salida["nivel_riesgo"] == "Medio"]
    df_medio.to_excel(writer, sheet_name="Riesgo_Medio", index=False)
# El archivo queda con tres hojas: Todos (20 filas), Riesgo_Alto (6 filas), Riesgo_Medio (6 filas)
```

Si llamas `.to_excel()` fuera de un `ExcelWriter`, sin el bloque `with`, cada llamada abre y sobreescribe el archivo completo. Al terminar solo queda la última hoja.

⚠️ Para exportar a Excel necesitas `openpyxl`. Si no está instalado, `.to_excel()` lanza `ModuleNotFoundError`. Actualiza `requirements.txt` e instálalo siguiendo el compando `pip install -r requirements.txt`.

---

### Ejercicios

#### Inducción al error

En `main.py`, escribe esta función e insértala justo antes del bloque `if __name__ == '__main__':`. La llamada al final del bloque se ejecuta al correr el script, antes del menú:

```python
def probar_exportar_excel():
    df = pd.DataFrame({"a": [1, 2]})
    df.to_excel("data/outputs/prueba.xlsx", index=False)

probar_exportar_excel()
```

Ejecuta esto sin tener `openpyxl` instalado. ¿Qué dice el error? ¿Cómo lo resuelves?

#### Básico

📂 `src/data_exporter.py`

Abre el archivo y reemplaza el `pass` de `exportar_csv()`. Genera la fecha de hoy, construye el nombre del archivo, construye la ruta completa y exporta el archivo. Intenta también hacer cambios y prueba los resultados.

```python
def exportar_csv(df, carpeta, nombre_base):
    # TODO: Genera la fecha con date.today().strftime("%Y%m%d").
    # Construye el nombre del archivo: f"{nombre_base}_{fecha_hoy}.csv"
    # Construye la ruta completa: f"{carpeta}/{nombre_archivo}"
    # Llama a df.to_csv() con index=False.
    pass
```

El bloque `if __name__ == "__main__":` ya existe al final del archivo. Actualízalo para probar solo `exportar_csv()` en esta etapa:

```python
if __name__ == "__main__":
    df = pd.read_csv(
        "data/inputs/declaraciones_iva_2025.csv",
        dtype={"nit": str, "codigo_municipio": str},
    )
    exportar_csv(df, "data/outputs", "declaraciones_prueba")
```

```bash
python src/data_exporter.py
```

La salida esperada en consola es:

```
CSV guardado: data/outputs/declaraciones_prueba_20260708.csv
```

<details>
<summary>💡 Ver solución</summary>

```python
def exportar_csv(df, carpeta, nombre_base):
    fecha_hoy = date.today().strftime("%Y%m%d")
    nombre_archivo = f"{nombre_base}_{fecha_hoy}.csv"
    ruta_completa = f"{carpeta}/{nombre_archivo}"
    df.to_csv(ruta_completa, index=False)
    print(f"CSV guardado: {ruta_completa}")
```

</details>

#### Intermedio

📂 `src/data_exporter.py`

Implementa `exportar_excel_por_categoria()`. Sigue los siguientes pasos

```python
def exportar_excel_por_categoria(df, carpeta, nombre_base, columna_categoria):
    # TODO: Genera la fecha y construye la ruta del archivo Excel.
    # Usa pd.ExcelWriter con engine="openpyxl" dentro de un bloque with.
    # Escribe la hoja "Todos" con el DataFrame completo.
    # Obtén los valores únicos de columna_categoria con unique().
    # Para cada valor único, filtra el DataFrame y escribe una hoja con ese nombre.
    pass
```

`df[columna_categoria].unique()` devuelve los valores distintos de esa columna. Recórrelos con un ciclo `for`: para cada uno, filtra el DataFrame con `df[df[columna_categoria] == categoria]` y escribe una hoja.

Actualiza el bloque de prueba:

```python
if __name__ == "__main__":
    df = pd.read_csv(
        "data/inputs/declaraciones_iva_2025.csv",
        dtype={"nit": str, "codigo_municipio": str},
    )
    exportar_csv(df, "data/outputs", "declaraciones_prueba")
    exportar_excel_por_categoria(df, "data/outputs", "declaraciones_prueba", "estado")
```

La salida esperada en consola es:

```
CSV guardado: data/outputs/declaraciones_prueba_20260708.csv
Excel guardado: data/outputs/declaraciones_prueba_20260708.xlsx
```

<details>
<summary>💡 Ver solución</summary>

```python
def exportar_excel_por_categoria(df, carpeta, nombre_base, columna_categoria):
    fecha_hoy = date.today().strftime("%Y%m%d")
    nombre_archivo = f"{nombre_base}_{fecha_hoy}.xlsx"
    ruta_completa = f"{carpeta}/{nombre_archivo}"

    with pd.ExcelWriter(ruta_completa, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Todos", index=False)
        for categoria in df[columna_categoria].unique():
            df[df[columna_categoria] == categoria].to_excel(
                writer, sheet_name=str(categoria), index=False
            )

    print(f"Excel guardado: {ruta_completa}")
```

</details>

🔁 **Ciclo git**

```bash
git add .
git commit -m "Sesión: exportación a CSV y Excel implementada en data_exporter"
git push
```

#### Avanzado

📂 `main.py` — las dos funciones ya funcionan; ahora conéctalas al menú.

Descomenta el import de la Sección 6 y completa la opción 4:

```python
# En el bloque de imports, descomenta:
from src.data_exporter import exportar_csv, exportar_excel_por_categoria

# Dentro de elif opcion == "4":
exportar_csv(df_salida, CARPETA_RESULTADOS, "declaraciones_clasificadas")
exportar_excel_por_categoria(df_salida, CARPETA_RESULTADOS, "declaraciones", "nivel_riesgo")
print("Archivos generados en", CARPETA_RESULTADOS)
```

La salida esperada al ejecutar opción 1 → 3 → 4:

```
CSV guardado: data/outputs/declaraciones_clasificadas_20260708.csv
Excel guardado: data/outputs/declaraciones_20260708.xlsx
Archivos generados en data/outputs
```

<details>
<summary>💡 Ver solución</summary>

```python
# En el bloque de imports (descomenta):
from src.data_exporter import exportar_csv, exportar_excel_por_categoria

# Dentro de elif opcion == "4":
elif opcion == "4":
    if df_salida is None:
        print("Primero transforma los datos con la opción 3.")
    else:
        exportar_csv(df_salida, CARPETA_RESULTADOS, "declaraciones_clasificadas")
        exportar_excel_por_categoria(df_salida, CARPETA_RESULTADOS, "declaraciones", "nivel_riesgo")
        print("Archivos generados en", CARPETA_RESULTADOS)
```

</details>

🔁 **Ciclo git**

```bash
git add .
git commit -m "Sesión: pipeline completo conectado al menú"
git push
```

---

## 7. Patrón ETL: separar responsabilidades

El trabajo de esta sesión sigue una estructura que tiene nombre en el mundo de los datos: **ETL** (Extract, Transform, Load). Este patrón es un concepto importante en ingeniería y análisis de datos y se explica a continuación.

### ¿Qué es ETL y de dónde viene?

El término ETL surgió en los años setenta y ochenta, cuando las organizaciones empezaron a construir los primeros **almacenes de datos** (data warehouses): bases de datos especializadas que consolidaban información de múltiples sistemas operativos — contabilidad, ventas, recursos humanos — en un solo lugar para facilitar el análisis y la toma de decisiones. Antes de eso, cada sistema guardaba sus datos en un formato propio, y cruzar información entre sistemas requería trabajo manual enorme.

**Bill Inmon**, ingeniero estadounidense, es considerado el "padre del data warehouse" y en los años noventa formalizó el concepto de almacén de datos como una colección de datos orientada por tema, integrada, variante en el tiempo y no volátil. **Ralph Kimball**, también de los años noventa, desarrolló la metodología dimensional (el modelo "estrella" y "copo de nieve") que sigue siendo la referencia práctica en diseño de almacenes de datos. Ambos describieron ETL como una columna clave dentro del proceso: sin una extracción limpia, una transformación consistente y una carga confiable, el almacén de datos es inútil. El acrónimo ETL se volvió estándar en la industria y hoy describe un **patrón arquitectónico** que es una solución estándar y reutilizable para resolver problemas comunes en el diseño de software a gran escala

Este patrón actualmente lo usan entidades financieras para consolidar transacciones de múltiples sucursales, hospitales para integrar registros clínicos de distintos sistemas, plataformas de comercio electrónico para actualizar inventarios y calcular métricas de ventas, entre otras organizaciones.

---

### E — Extract: extraer los datos de su fuente

La fase de extracción es el primer contacto con los datos en su estado original. El objetivo es sacarlos de donde están — un archivo CSV, una base de datos, una API, un formulario web — y cargarlos en memoria de forma íntegra y correcta, **sin modificar todavía ningún contenido**. La palabra clave es "en su forma original" pues la extracción no limpia, no calcula, no clasifica, sino que solo trae los datos.

En la práctica, "extraer" implica varias decisiones que pueden parecer menores pero tienen consecuencias:

**¿Qué formato tiene la fuente?** CSV, Excel, JSON, una base de datos relacional, una API REST — cada formato tiene sus propias particularidades. Un CSV con separador `;` en lugar de `,` puede fallar si no se revisa porque pandas por defecto lo carga pero pone todo en una sola columna. Un CSV con encoding `cp1252` en un sistema que espera `utf-8` produce caracteres ilegibles.

**¿Qué columnas cargar?** Traer todo el archivo siempre es tentador, pero en archivos con cientos de columnas y millones de filas puede agotar la memoria. El parámetro `usecols` de `pd.read_csv()` permite seleccionar solo las columnas que el análisis necesita, reduciendo el uso de memoria desde el primer momento.

**¿Qué tipos de dato forzar?** Los tipos que pandas infiere automáticamente no siempre son los correctos para el dominio. Un código de municipio leído como entero pierde los ceros a la izquierda. Un NIT leído como número no puede tener el guion. Declarar `dtype` en la carga es parte de la extracción: se le está diciendo explícitamente a pandas qué tipo debe tener cada columna.

**¿Están los datos íntegros?** La validación inicial — número de filas esperado, columnas presentes, valores de encabezado correctos, nulos en columnas críticas — también pertenece a esta fase. Es mejor detectar un archivo incompleto o malformado antes de transformar nada.

En esta sesión, `data_loader.py` implementa la fase Extract: `cargar_declaraciones()` extrae los datos del CSV aplicando los tipos correctos, e `inspeccionar_datos()` y `validar_nulos()` verifican su integridad antes de pasarlos a la siguiente etapa.

---

### T — Transform: transformar los datos

La fase de transformación es donde ocurre el trabajo analítico. Los datos que vienen de la fuente rara vez llegan exactamente en la forma que el análisis necesita: hay columnas que sobran, columnas que faltan, valores que necesitan calcularse, categorías que necesitan asignarse. La transformación puede incluir varias operaciones distintas:

**Limpieza**: eliminar filas duplicadas, corregir espacios invisibles al inicio y al final de campos de texto (el `.str.strip()` que viste), estandarizar categorías escritas de formas inconsistentes. Esta operación no agrega información nueva sino que corrige lo que llegó mal.

**Derivación de variables**: calcular columnas nuevas que no existen en la fuente pero que el análisis requiere. En esta sesión, `nivel_riesgo` e `identificador_periodo` son variables derivadas: no estaban en el CSV original, pero se calculan a partir de columnas que sí estaban (`valor_declarado`, `nit`, `periodo`). Una variable derivada no modifica los datos originales sino que agrega una columna nueva al DataFrame.

**Clasificación y enriquecimiento**: asignar valores, rangos o categorías a registros individuales basándose en reglas de negocio definidas. La lógica de umbrales que implementa `clasificar_por_valor()` es una forma de enriquecimiento: le agrega a cada declaración una clasificación de riesgo que no estaba en el dato original pero que tiene valor para el análisis posterior.

**Selección y reordenamiento de columnas**: preparar el DataFrame con exactamente las columnas que el destinatario final necesita, en el orden correcto. `preparar_columnas_salida()` hace esto. Un archivo de salida bien ordenado — con el identificador al inicio, los campos de valor en el centro, el estado al final — comunica mejor que uno con las columnas en el orden en que llegaron.

Si la operación **modifica el contenido** del dato (calcula algo, asigna una etiqueta, cambia el tipo de una columna) pertenece a Transform. Si solo **mueve el dato** de un lugar a otro sin cambiarlo, no es Transform.

En esta sesión, `data_transformer.py` implementa esta fase completa.

---

### L — Load: cargar los resultados en el destino

La fase de carga escribe los datos transformados en el destino final. "Load" en ETL no significa "cargar en memoria" (ese es Extract); significa "cargar en el sistema de destino": un archivo CSV para pasar a otro proceso, un Excel para un analista, una base de datos para consultas en tiempo real, un sistema de inteligencia de negocios para visualización. En todos los casos, la fase de carga toma el DataFrame limpio y transformado que salió de Transform y lo persiste en alguna forma duradera.

La fase Load toma decisiones sobre el formato de salida. ¿CSV o Excel? ¿Un solo archivo o uno por categoría? ¿Con la fecha en el nombre para no sobreescribir versiones anteriores? Estas son decisiones de Load, no de Transform. Transform no sabe ni le importa a dónde van los datos, sino que solo los prepara correctamente.

Por otra parte, la fase Load no sabe cómo se calcularon los datos ni de dónde vienen. Solo recibe un DataFrame listo y lo escribe. Si mañana quisieras cambiar el formato de salida de CSV a JSON, o escribir directamente a una base de datos PostgreSQL, solo cambiarías `data_exporter.py`. Las fases Extract y Transform no necesitan saber nada de ese cambio.

En esta sesión, `data_exporter.py` implementa la fase Load: `exportar_csv()` y `exportar_excel_por_categoria()` escriben el resultado a disco.

---

### ¿Por qué importa separar las tres fases?

En un script de unas pocas decenas de líneas, puedes mezclar las tres fases pero mezclar el código cuando el código crece, cuando hay múltiples personas trabajando sobre el mismo proceso, o cuando algo falla en producción ( donde otros usuarios usan el código) trae consecuencias. Por ejemplo:

**Localización de errores**: imagina que el proceso se corre todos los lunes a las 6 a.m. y esta semana el archivo de declaraciones llegó con el nombre distinto. El proceso falla. Si tienes una función `cargar_declaraciones()` separada, el error queda localizado en `data_loader.py` y sabes exactamente dónde buscar. Si la carga, la transformación y la exportación están mezcladas en 300 líneas el error puede estar en cualquier parte.

**Reproducibilidad**: si guardas el archivo fuente original y el código de transformación por separado, puedes reproducir exactamente el mismo resultado meses después. Puedes cambiar los umbrales de clasificación, volver a correr la transformación y comparar los resultados antes y después del cambio. Sin separación, es difícil saber qué datos entraron ni qué lógica se aplicó.

**Composición y reutilización**: una vez que cada función hace bien una sola cosa, puedes combinarlas de formas distintas. `exportar_csv()` puede recibir cualquier DataFrame, no solo el resultado de `clasificar_por_valor()`. `cargar_declaraciones()` puede usarse en otro script que analice retenciones. Las funciones compuestas por responsabilidad son más fáciles de reutilizar que el código monolítico.

### El patrón en esta sesión

| Fase | Responsabilidad | Módulo | Funciones |
|---|---|---|---|
| **Extract** | Cargar los datos desde la fuente y validar que llegaron bien | `src/data_loader.py` | `cargar_declaraciones()`, `inspeccionar_datos()`, `validar_nulos()` |
| **Transform** | Clasificar, derivar variables, seleccionar columnas | `src/data_transformer.py` | `clasificar_por_valor()`, `agregar_identificador_periodo()`, `preparar_columnas_salida()` |
| **Load** | Escribir los resultados a disco | `src/data_exporter.py` | `exportar_csv()`, `exportar_excel_por_categoria()` |

`main.py` no hace ninguna de esas tres cosas sino que solo las coordina en secuencia y decide el orden en que se llaman las funciones.
Si completaste los ejercicios avanzados de las secciones anteriores, cada opción del menú en `main.py` ya tiene su implementación y los imports del bloque superior están descomentados. La opción 5 (pipeline completo) llama a todas las etapas en secuencia:

```python
# dentro de elif opcion == "5":
df = cargar_declaraciones(RUTA_DATOS)
print(f"Filas cargadas: {len(df)}")

inspeccionar_datos(df)
validar_nulos(df, COLUMNAS_CRITICAS)

df = clasificar_por_valor(df, umbral_alto=10_000_000, umbral_medio=5_000_000)
df = agregar_identificador_periodo(df)
df_salida = preparar_columnas_salida(df, COLUMNAS_SALIDA)

exportar_csv(df_salida, CARPETA_RESULTADOS, "declaraciones_clasificadas")
exportar_excel_por_categoria(df_salida, CARPETA_RESULTADOS, "declaraciones", "nivel_riesgo")
print("Archivos generados en", CARPETA_RESULTADOS)
```

---

### Ejercicios

#### Uno

Describe con tus palabras qué hace cada módulo y por qué es útil separarlos en archivos distintos en lugar de tener todo en `main.py`.

<details>
<summary>💡 Ver respuesta de referencia</summary>

`data_loader.py` lee el archivo y verifica que los datos llegaron bien. `data_transformer.py` aplica la lógica de negocio: asignar `nivel_riesgo`, crear `identificador_periodo`, ordenar columnas. `data_exporter.py` escribe los resultados a disco. Separar las tres responsabilidades hace que cuando algo falle sepas exactamente en qué módulo buscar, y que puedas cambiar el formato de salida sin tocar la lógica de transformación.

</details>

#### Dos

Revisa el código que escribiste en las secciones 3–6 y traza el flujo completo: ¿qué entra y qué sale de cada módulo? ¿Qué pasaría si `cargar_declaraciones()` retornara `None` en lugar de un DataFrame? ¿En qué opción del menú fallaría primero y con qué error?

<details>
<summary>💡 Ver respuesta de referencia</summary>

Entra: una ruta de archivo. Sale: un DataFrame. Si `cargar_declaraciones()` retorna `None`, la opción 2 fallaría al llamar `inspeccionar_datos(None)` con `AttributeError: 'NoneType' object has no attribute 'shape'`. La opción 3 fallaría igual al intentar `clasificar_por_valor(None, ...)`. El error siempre aparece en la función que recibe `None` como primer argumento.

</details>

#### Tres

Implementa la opción 5 del menú en `main.py` (`# OPCIÓN 5: PIPELINE COMPLETO`): llama en secuencia a las funciones de carga, inspección, transformación y exportación que ya implementaste en las opciones anteriores. Ejecuta el pipeline completo desde el menú y verifica que los archivos aparecen en `data/outputs/` con los nombres y columnas esperados.

La salida esperada al elegir la opción 5:

```
Filas cargadas: 20
=== Dimensiones ===
(20, 9)
...
✓ nit: sin nulos
✓ valor_declarado: sin nulos
✓ estado: sin nulos
CSV guardado: data/outputs/declaraciones_clasificadas_20260708.csv
Excel guardado: data/outputs/declaraciones_20260708.xlsx
Archivos generados en data/outputs
```

<details>
<summary>💡 Ver solución</summary>

```python
elif opcion == "5":
    df = cargar_declaraciones(RUTA_DATOS)
    print(f"Filas cargadas: {len(df)}")

    inspeccionar_datos(df)
    validar_nulos(df, COLUMNAS_CRITICAS)

    df = clasificar_por_valor(df, umbral_alto=10_000_000, umbral_medio=5_000_000)
    df = agregar_identificador_periodo(df)
    df_salida = preparar_columnas_salida(df, COLUMNAS_SALIDA)

    exportar_csv(df_salida, CARPETA_RESULTADOS, "declaraciones_clasificadas")
    exportar_excel_por_categoria(df_salida, CARPETA_RESULTADOS, "declaraciones", "nivel_riesgo")
    print("Archivos generados en", CARPETA_RESULTADOS)
```

</details>

---

🔁 **Ciclo git — cierre de sesión**

```bash
git add .
git commit -m "Sesión: carga, clasificación y exportación de declaraciones IVA con patrón ETL"
git push
```

---

## Referencias

### Documentación oficial

- **pandas** — documentación completa, guías de usuario y referencia de API:
  [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)

- **pandas — User Guide (Getting started)** — punto de entrada recomendado para quienes aprenden pandas:
  [https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)

- **NumPy — `numpy.where`** — referencia del parámetro y ejemplos:
  [https://numpy.org/doc/stable/reference/generated/numpy.where.html](https://numpy.org/doc/stable/reference/generated/numpy.where.html)

- **NumPy — User Guide** — conceptos de arrays, tipos de dato y operaciones vectorizadas:
  [https://numpy.org/doc/stable/user/](https://numpy.org/doc/stable/user/)

- **Python — Diccionarios** — referencia oficial del tipo `dict`:
  [https://docs.python.org/3/library/stdtypes.html#mapping-types-dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)

- **Python — `datetime.date`** — referencia del módulo `datetime`, incluyendo `strftime`:
  [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)

- **openpyxl** — librería para escribir y leer archivos Excel (.xlsx):
  [https://openpyxl.readthedocs.io/](https://openpyxl.readthedocs.io/)

### Datos abiertos

- **Datos Abiertos Colombia** — portal de datasets del gobierno colombiano; fuente para la extensión del protocolo de inspección:
  [https://www.datos.gov.co](https://www.datos.gov.co)

- **DIAN — Estadísticas tributarias** — datos y reportes estadísticos de declaraciones y recaudo:
  [https://www.dian.gov.co/dian/cifras/Paginas/EstadisticasTributarias.aspx](https://www.dian.gov.co/dian/cifras/Paginas/EstadisticasTributarias.aspx)

### Lecturas sobre ETL y arquitectura de datos

- **Wes McKinney — "Python for Data Analysis"** (O'Reilly) — el libro escrito por el creador de pandas; cubre Series, DataFrame y los patrones de trabajo con datos tabulares en profundidad. La tercera edición (2022) está actualizada para pandas 1.x y 2.x.
- **dbt (data build tool) — What is ETL?** — explicación práctica y moderna del patrón ETL y su evolución a ELT, con ejemplos del mundo real:
  [https://www.getdbt.com/analytics-engineering/etl/what-is-etl](https://www.getdbt.com/analytics-engineering/etl/what-is-etl)

### Para profundizar en pandas

- **"Effective Pandas" — Matt Harrison** — libro conciso y práctico sobre pandas idiomático; cubre operaciones vectorizadas, agrupación y limpieza de datos.

- **pandas Cheat Sheet (oficial)** — referencia rápida de las operaciones más comunes en una página:
  [https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
