from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
N_SALES = 10_000
DATA_DIR = Path("data")


def dim_time() -> pd.DataFrame:
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    return pd.DataFrame(
        {
            "time_id": np.arange(1, len(dates) + 1),
            "day": dates.date,
            "month": dates.month,
            "quarter": dates.quarter,
            "year": dates.year,
        }
    )


def dim_item(rng: np.random.Generator) -> pd.DataFrame:
    categories = {
        "Electronics": ["NovaTech", "Voltix", "PixelPro"],
        "Home": ["CasaNorte", "Domus", "Habita"],
        "Sports": ["AurumFit", "Montiva", "SprintX"],
        "Beauty": ["Luma", "DermaPlus", "NaturaLab"],
        "Grocery": ["CampoVivo", "BuenSabor", "FreshCo"],
    }

    rows = []
    item_id = 1
    for category, brands in categories.items():
        for item_number in range(1, 11):
            brand = rng.choice(brands)
            base_price = rng.lognormal(mean=3.2, sigma=0.45)
            rows.append(
                {
                    "item_id": item_id,
                    "item_name": f"{category} Item {item_number:02d}",
                    "brand": brand,
                    "category": category,
                    "base_price": round(float(base_price), 2),
                }
            )
            item_id += 1

    return pd.DataFrame(rows)


def dim_location() -> pd.DataFrame:
    locations = [
        ("Tuxtla Gutierrez", "Chiapas", "Mexico"),
        ("San Cristobal", "Chiapas", "Mexico"),
        ("Tapachula", "Chiapas", "Mexico"),
        ("Merida", "Yucatan", "Mexico"),
        ("Valladolid", "Yucatan", "Mexico"),
        ("Cancun", "Quintana Roo", "Mexico"),
        ("Playa del Carmen", "Quintana Roo", "Mexico"),
        ("Guadalajara", "Jalisco", "Mexico"),
        ("Zapopan", "Jalisco", "Mexico"),
        ("Monterrey", "Nuevo Leon", "Mexico"),
        ("San Pedro", "Nuevo Leon", "Mexico"),
        ("Austin", "Texas", "USA"),
        ("Dallas", "Texas", "USA"),
        ("Houston", "Texas", "USA"),
        ("San Antonio", "Texas", "USA"),
        ("Los Angeles", "California", "USA"),
        ("San Diego", "California", "USA"),
        ("San Jose", "California", "USA"),
        ("Miami", "Florida", "USA"),
        ("Orlando", "Florida", "USA"),
        ("Bogota", "Cundinamarca", "Colombia"),
        ("Soacha", "Cundinamarca", "Colombia"),
        ("Medellin", "Antioquia", "Colombia"),
        ("Envigado", "Antioquia", "Colombia"),
        ("Cali", "Valle del Cauca", "Colombia"),
        ("Palmira", "Valle del Cauca", "Colombia"),
        ("Santiago", "Metropolitana", "Chile"),
        ("Puente Alto", "Metropolitana", "Chile"),
        ("Valparaiso", "Valparaiso", "Chile"),
        ("Vina del Mar", "Valparaiso", "Chile"),
    ]

    return pd.DataFrame(
        [
            {
                "location_id": location_id,
                "city": city,
                "state": state,
                "country": country,
            }
            for location_id, (city, state, country) in enumerate(locations, start=1)
        ]
    )


def fact_sales(
    df_time: pd.DataFrame,
    df_item: pd.DataFrame,
    df_location: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    sales_id = np.arange(1, N_SALES + 1)
    time_id = rng.choice(df_time["time_id"], size=N_SALES)
    item_id = rng.choice(df_item["item_id"], size=N_SALES)
    location_id = rng.choice(df_location["location_id"], size=N_SALES)

    item_lookup = df_item.set_index("item_id")
    location_lookup = df_location.set_index("location_id")
    time_lookup = df_time.set_index("time_id")

    categories = item_lookup.loc[item_id, "category"].to_numpy()
    countries = location_lookup.loc[location_id, "country"].to_numpy()
    months = time_lookup.loc[time_id, "month"].to_numpy()
    base_prices = item_lookup.loc[item_id, "base_price"].to_numpy()

    category_units = {
        "Electronics": 1.4,
        "Home": 2.0,
        "Sports": 2.4,
        "Beauty": 3.2,
        "Grocery": 5.5,
    }
    expected_units = np.array([category_units[category] for category in categories])
    units_sold = rng.poisson(lam=expected_units) + 1

    country_multiplier = {
        "Mexico": 1.00,
        "USA": 1.18,
        "Colombia": 0.88,
        "Chile": 1.05,
    }
    season_multiplier = np.where(np.isin(months, [11, 12]), 1.22, 1.00)
    market_multiplier = np.array([country_multiplier[country] for country in countries])
    ticket_noise = rng.lognormal(mean=0.0, sigma=0.12, size=N_SALES)

    dollars_sold = np.round(
        units_sold * base_prices * season_multiplier * market_multiplier * ticket_noise,
        2,
    )

    return pd.DataFrame(
        {
            "time_id": time_id,
            "item_id": item_id,
            "location_id": location_id,
            "dollars_sold": dollars_sold,
            "units_sold": units_sold,
        }
    )


def main() -> None:
    rng = np.random.default_rng(SEED)
    DATA_DIR.mkdir(exist_ok=True)

    tabla_time = dim_time()
    tabla_item = dim_item(rng)
    tabla_location = dim_location()
    tabla_sales = fact_sales(tabla_time, tabla_item, tabla_location, rng)

    tabla_time.to_csv(DATA_DIR / "dim_time.csv", index=False)
    tabla_item.drop(columns=["base_price"]).to_csv(DATA_DIR / "dim_item.csv", index=False)
    tabla_location.to_csv(DATA_DIR / "dim_location.csv", index=False)
    tabla_sales.to_csv(DATA_DIR / "fact_sales.csv", index=False)

    print("Esquema estrella generado y guardado en CSV con exito.")


if __name__ == "__main__":
    main()
