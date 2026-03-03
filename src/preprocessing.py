"""
preprocesamiento.py

Agrega los datos de ventas a nivel mensual por producto-presentación,
para predecir la demanda mensual.

Uso:
    python src/preprocesamiento.py
"""

from pathlib import Path

import pandas as pd

# Rutas relativas a la raíz del repositorio
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "raw" / "dataset_ventas_lacteos_2024.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "datos_mensuales.csv"


def preprocess_monthly(input_path: Path, output_path: Path) -> None:
    print(f"Leyendo datos desde: {input_path}")
    df = pd.read_csv(input_path)

    # Fecha a datetime
    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True)

    # Año, mes y fecha primer día de mes
    df["anio"] = df["Fecha"].dt.year
    df["mes"] = df["Fecha"].dt.month
    df["Fecha_mes"] = df["Fecha"].dt.to_period("M").dt.to_timestamp()

    # Agregamos por producto-presentación y mes
    print("Agregando por producto, presentación, año, mes...")
    agg = (
    df.groupby(["Categoría", "Producto", "Presentación", "anio", "mes", "Fecha_mes"])
    .agg(
        cantidad_total_mes=("Cantidad comprada", "sum"),
        num_pedidos=("ID Orden", "nunique"),
        num_clientes=("Nombre del supermercado", "nunique"),
    )
    .reset_index()
)

    # Ordenar por tiempo
    agg = agg.sort_values(["Fecha_mes", "Categoría", "Producto", "Presentación"])

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Guardando datos mensuales en: {output_path}")
    agg.to_csv(output_path, index=False)
    print("Preprocesamiento mensual completado.")


if __name__ == "__main__":
    preprocess_monthly(INPUT_PATH, OUTPUT_PATH)