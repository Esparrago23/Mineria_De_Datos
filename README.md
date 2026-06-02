# Proyecto Data Warehouse - Mini Cubo DuckDB

Actividad 04 de Mineria de Datos. El proyecto construye un mini data warehouse de ventas con un esquema estrella, genera datos sinteticos con `pandas` y `numpy`, carga los datos en DuckDB y ejecuta operaciones OLAP sobre el cubo.

## Estructura

```text
proyecto_data_warehouse_233414_TorresHernandez_ChristianAlejandro/
|-- README.md
|-- notebook.ipynb
|-- requirements.txt
|-- AI_USAGE.md
|-- scripts/
|   |-- 01_generate_data.py
|   |-- 02_build_warehouse.sql
|-- data/
|   |-- dim_time.csv
|   |-- dim_item.csv
|   |-- dim_location.csv
|   |-- fact_sales.csv
```

## Requisitos

- Python 3.13 o compatible
- DuckDB
- pandas
- numpy
- Jupyter

Las dependencias estan listadas en `requirements.txt`.

## Instalacion

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Si el entorno virtual ya existe, solo activalo:

```powershell
.\.venv\Scripts\activate
```

## Generar el dataset sintetico

Ejecuta:

```powershell
python scripts\01_generate_data.py
```

El script genera cuatro CSV en `data/`:

- `dim_time.csv`: dimension de tiempo con dias de 2025.
- `dim_item.csv`: dimension de productos con marca y categoria.
- `dim_location.csv`: dimension geografica con ciudad, estado y pais.
- `fact_sales.csv`: tabla de hechos con llaves foraneas y medidas numericas.

El generador usa `np.random.default_rng(42)` para que el resultado sea reproducible.

## Construir y ejecutar el warehouse

Abre `notebook.ipynb` en JupyterLab, VS Code o Jupyter Notebook y ejecuta las celdas.

El notebook:

- crea el esquema estrella en DuckDB;
- carga los CSV con `read_csv_auto`;
- crea la vista `v_sales` como cubo logico;
- ejecuta roll-up, drill-down, slice & dice y pivot;
- materializa agregaciones con `CUBE`, `ROLLUP` y `GROUPING SETS`;
- compara `SUM` como medida distributiva contra `MEDIAN` como medida holistica;
- mide tiempos con `time.perf_counter()`;
- incluye la declaracion de uso de IA al final.

