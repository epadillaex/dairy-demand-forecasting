# Predicción de Demanda Mensual — Distribuidora Láctea

Proyecto de aprendizaje y práctica en machine learning aplicado a series temporales. El objetivo técnico es predecir la demanda mensual futura para optimizar la planificación de pedidos a proveedores.

## 📌 Objetivo del proyecto

**Predecir la demanda mensual futura** de una empresa distribuidora de productos lácteos con el fin de optimizar la planificación de pedidos a proveedor.

El modelo estima el número de unidades que se venderán por producto y formato comercial (por ejemplo: Yogur natural – pack 4×125 g), que es el nivel de detalle real al que la empresa realiza sus compras y gestiona su inventario.

Dado que se trata de productos perecederos, la previsión de demanda no solo busca evitar faltantes, sino también minimizar mermas por caducidad, equilibrando correctamente el stock disponible con la rotación esperada.

Este problema es especialmente relevante en un entorno donde:

- Parte de los proveedores se encuentran en otras regiones o países.
- Una mala planificación puede provocar:
    - Roturas de stock, con impacto directo en ventas y satisfacción del cliente.
    - Exceso de inventario, que en productos lácteos se traduce en pérdidas económicas por caducidad.

## 🗂️ Estructura del repositorio

        ├── data/
        │   ├── raw/
        │   │   └── dataset_ventas_lacteor_2024.csv
        │   └── processed/
        │       ├── datos_features.csv
        │       └── datos_mensuales.csv
        ├── notebooks/
        │   ├── 01_eda.ipynb
        │   ├── 02_feature_engineering.ipynb
        │   └── 03_modeling.ipynb
        ├── src/
        │   └── preprocessing.py
        ├── results/
        │   ├── figures/
        │   │   ├── acf/
        │   │   ├── pacf/
        │   │   ├── series_temporales/
        │   │   ├── test/
        │   │   └── train/
        │   ├── modelo/
        │   │    └── catboost_mode.cbm
        │   └── predicciones/
        │        └── predicciones.csv
        ├── README.md
        └── requirements.txt
---

## 📦 Datos

**Dataset original:** `dataset_ventas_lacteos_2024.csv`

Fuente: [Dataset Ventas Lácteos 2024 — Kaggle](https://www.kaggle.com/datasets/hectorconde/dataset-ventas-lacteos-2024)

Contiene registros de ventas diarias durante el año 2024 con las siguientes columnas relevantes:

| Campo | Descripción |
|---|---|
| `Fecha` | Fecha de la orden |
| `ID Orden` | Identificador único de pedido |
| `Categoría` | Categoría del producto (ej. Cremas, Leche…) |
| `Producto` | Nombre del producto |
| `Presentación` | Formato comercial (ej. Tarrina 200g, Spray 250ml…) |
| `Cantidad comprada` | Unidades vendidas |
| `Nombre del supermercado` | Cliente destino |

**Dataset procesado:** `datos_mensuales.csv`

Ventas agregadas mensualmente por combinación `Categoría + Producto + Presentación`, con las columnas `cantidad_total_mes`, `num_pedidos` y `num_clientes` (588 filas × 9 columnas).

---

## ⚙️ Pipeline

### 1. Preprocesamiento — `src/preprocessing.py`

Agrega los datos de ventas a nivel mensual por cada combinación producto-presentación:

```bash
python src/preprocessing.py
```

Genera `data/processed/datos_mensuales.csv`.

### 2. Feature Engineering — `notebooks/02_feature_engineering.ipynb`

Construye las variables de entrada para el modelo a partir de los datos mensuales:

| Feature | Descripción |
|---|---|
| `lag_1` | Ventas del mes anterior |
| `lag_2` | Ventas de hace 2 meses |
| `lag_3` | Ventas de hace 3 meses |
| `media_movil_3` | Media móvil de los últimos 3 meses |
| `mes` | Número de mes (1–12), como feature ordinal |
| `mes_seno` | Codificación cíclica del mes (seno) |
| `mes_coseno` | Codificación cíclica del mes (coseno) |
| `num_pedidos` | Número de pedidos ese mes |
| `num_clientes` | Número de clientes distintos ese mes |

Dado que solo se dispone de 12 meses de histórico por serie, se ha aplicado un criterio conservador: los lags introducen 3 filas `NaN` por serie, resultando en un dataset final de **441 filas × 15 columnas** (9 meses efectivos por cada una de las 49 combinaciones producto-presentación).

> **Nota sobre codificación cíclica:** La representación en seno/coseno del mes permite al modelo entender que diciembre (12) y enero (1) son meses contiguos, y no extremos opuestos de la escala numérica.

### 3. Modelado — `notebooks/03_modeling.ipynb`

Se entrena un modelo **CatBoost Regressor** optimizando RMSE. Los datos se dividen en tres conjuntos: entrenamiento, validación y test.


> **Nota:** La elección de CatBoost responde al propósito de práctica del proyecto. Para un dataset de este tamaño (441 filas, 9 meses por serie), modelos más sencillos como ARIMA, pensado específicamente para series temporales, o una regresión lineal probablemente serían más apropiados, con menor riesgo de sobreajuste y más fáciles de interpretar.

---

## 📊 Resultados

| Conjunto | MAE | RMSE | R² |
|---|---|---|---|
| **Validación** | 1.550,80 | 1.926,15 | 0,9144 |
| **Test** | 1.984,32 | 2.610,50 | 0,8540 |

El modelo explica más del **85% de la varianza** en el conjunto de test, con un error medio absoluto de ~1.984 unidades. El R² de 0,91 en validación confirma un buen ajuste, mientras que la ligera caída en test es esperable dado el reducido histórico disponible (12 meses por serie).

---

## 🚀 Reproducir el proyecto

1. Clona el repositorio:
   ```bash
   git clone https://github.com/epadillaex/dairy-demand-forecasting.git
   cd dairy-demand-forecasting
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta el preprocesamiento:
   ```bash
   python src/preprocessing.py
   ```

4. Abre los notebooks en orden:
   - `notebooks/01_eda.ipynb`
   - `notebooks/02_feature_engineering.ipynb`
   - `notebooks/03_modeling.ipynb`

---

## 🛠️ Tecnologías utilizadas

- Python 3.11
- pandas · numpy
- CatBoost
- Jupyter Notebooks

---