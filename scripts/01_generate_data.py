import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

def dim_time():
    fecha = pd.date_range(start='2025-01-01', end='2025-12-31', freq='D')
    df_time = pd.DataFrame({
        'time_id': np.arange(1, len(fecha) + 1),
        'fecha': fecha,
        'dia': fecha.day,
        'mes': fecha.month,
        'trimestre': fecha.quarter,
        'año': fecha.year
    })
    return df_time

def dim_item():
    item_id = np.arange(1, 51)
    df_item = pd.DataFrame({
        'item_id': item_id,
        'item_name': [f'Item {i}' for i in item_id],
        'category': rng.choice(['A', 'B', 'C', 'D'], size=50),
        'marca': rng.choice(['Marca1', 'Marca2', 'Marca3'], size=50)
    })
    return df_item

def dim_location():
    location_id = np.arange(1, 31)
    df_location = pd.DataFrame({
        'location_id': location_id,
        'city': [f'City {i}' for i in location_id],
        'state': rng.choice(['State1', 'State2', 'State3'], size=30),
        'country': rng.choice(['Country1', 'Country2'], size=30)
    })
    return df_location

def fact_sales(df_time, df_item, df_location):
    sales_id = np.arange(1, 10001)
    time_id = rng.choice(df_time['time_id'], size=10000)
    item_id = rng.choice(df_item['item_id'], size=10000)
    location_id = rng.choice(df_location['location_id'], size=10000)
    
    units_sold = rng.integers(1, 20, size=10000)
    ruido = rng.uniform(0.85, 1.15, size=10000)
    precio_base = 15.50
    dollar_sold = np.round(units_sold * precio_base * ruido, 2)
    df_sales = pd.DataFrame({
        'sales_id': sales_id,
        'time_id': time_id,
        'item_id': item_id,
        'location_id': location_id,
        'units_sold': units_sold,
        'dollar_sold': dollar_sold
    })  
    return df_sales


tabla_time = dim_time()
tabla_item = dim_item()
tabla_location = dim_location()
tabla_sales = fact_sales(tabla_time, tabla_item, tabla_location)

tabla_time.to_csv('./data/dim_time.csv', index=False)
tabla_item.to_csv('./data/dim_item.csv', index=False)
tabla_location.to_csv('./data/dim_location.csv', index=False)
tabla_sales.to_csv('./data/fact_sales.csv', index=False)

print("¡Esquema estrella generado y guardado en CSV con éxito!")