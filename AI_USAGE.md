# Declaracion de uso de IA

## Herramientas usadas
- ChatGPT / Codex (OpenAI) - apoyo para interpretar la actividad, revisar la estructura del proyecto y mejorar el script de generacion de datos sinteticos.

## Que genere con IA
- [x] Orientacion inicial para generar el dataset sintetico: prompt usado fue "Ya esta el entorno, puedes ayudarme con la generacion del dataset sintetico, el documento menciona que puedo hacerlo con 'Generas datos sinteticos de ventas con pandas + numpy.', no me generes el codigo de esto aun, ayudame a intentarlo yo,puedes ayudarme ensenando como generarlo puedes usar un ejemplo pero que no sea el de la actividad". Resumen de la ayuda: recibi una explicacion conceptual, sin codigo completo, sobre como disenar dimensiones y tabla de hechos, usar `np.random.default_rng(42)`, crear catalogos controlados, muestrear llaves foraneas y hacer que `dollars_sold` dependiera de `units_sold` y del precio base del producto.
- [x] Revision y mejora de `scripts/01_generate_data.py`: prompt usado fue "ok quiero que cheques como construi el generate data, si puedes mejorarlo hazlo, Resumen de la ayuda: se reviso el script y se mejoro para que el dataset cumpliera mejor la consigna: 365 dias en `dim_time`, 50 productos en `dim_item`, 30 ciudades en `dim_location`, 10,000 ventas en `fact_sales`, al menos 5 categorias, mas de 3 paises, nombres de columnas compatibles con DuckDB y la medida `dollars_sold` calculada a partir de unidades, precio base, temporada, pais y ruido lognormal.
- [x] Explicacion de `read_csv_auto` y de la distribucion lognormal: prompt usado fue "puedes mostrarme como se usa read_csv_auto. tambien explicame el porque se menciona esto "Cambie la distribucion de dollars_sold de normal a lognormal porque...", Resumen de la ayuda: se explico como DuckDB puede leer CSVs con `read_csv_auto`, como crear tablas desde esos archivos, y por que una distribucion lognormal modela mejor montos de venta que una normal.

## Que entendi y modifique yo
- El dataset debe modelarse como esquema estrella: `fact_sales` concentra las ventas y se conecta con `dim_time`, `dim_item` y `dim_location` por llaves.
- La semilla `42` permite que los CSV generados sean reproducibles.

## Que NO supe explicar de lo que genero la IA
- Pendiente de completar despues de probar el notebook y preparar la defensa oral.
