# Predicción de Demanda Mensual — Distribuidora Láctea

Modelo de machine learning para predecir la demanda mensual futura y optimizar
la planificación de pedidos a proveedores.

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
        │       └── datos_mensuales.csv
        ├── notebooks/
        │   ├── 01_eda.ipynb
        │   ├── 02_feature_engineering.ipynb
        │   └── 03_modeling.ipynb
        ├── src/
        │   ├── preprocessing.py
        │   ├── 
        │   ├── 
        │   └── 
        ├── results/
        ├── README.md
        └── requirements.txt