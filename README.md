# Desarrollo-de-Aplicaciones-Empresariales
### ↗️ Gestión de Ventas

Prototipo Funcional: Sistema Modular de Registro de Ventas
Estado del Proyecto: Prototipo Funcional (Avance del 60%)

Autores: Catalina Vergara & Francisco Benavides

Institución: Universidad Católica de Temuco (UCT)

Fecha de Entrega: 12 de abril de 2026

## 📌 Resumen Ejecutivo
Este sistema es una aplicación de gestión comercial diseñada para transformar el registro de transacciones en inteligencia de negocios. A través de una interfaz de alto contraste denominada "Onyx & Gold", el software permite no solo capturar ventas, sino analizar la rentabilidad en tiempo real, detectar pérdidas operativas y gestionar la logística de insumos.

Actualmente, el proyecto cuenta con un núcleo estable que integra procesamiento contable, persistencia de datos en sesión y visualización analítica avanzada mediante gráficos interactivos.

## 🛠️ Arquitectura y Tecnologías
El software se ha construido bajo un paradigma de desarrollo modular, facilitando la escalabilidad y el mantenimiento del código para futuras iteraciones académicas o comerciales.

Stack Tecnológico:
Lenguaje: Python 3.x

Framework de Interfaz: Streamlit (Para la creación de la web app).

Procesamiento de Datos: Pandas (Gestión de DataFrames y lógica contable).

Visualización: Plotly (Gráficos dinámicos en modo oscuro).

Estilizado: CSS inyectado para una experiencia de usuario (UX) de alta gama.

## 🧱 Estructura del Proyecto:
app.py: Controlador principal que gestiona el flujo de navegación y la integración de módulos.

modules/database.py: Módulo encargado de la persistencia de datos (actualmente en session_state).

modules/styles.py: Definición de la capa visual premium mediante selectores CSS.

modules/tabs_content.py: Implementación de la lógica de negocio, cálculos de márgenes y motores de búsqueda.

## 🚀 Instalación y Ejecución
Para iniciar la aplicación en un entorno local, siga estas instrucciones:

1. **Instalar dependencias necesarias:**
   ```bash
   pip install streamlit pandas plotly
   ```

2. **Ejecutar la aplicación:**
   Desde la raíz del proyecto, ejecute:
   ```bash
   python -m streamlit run app.py
   ```

---

## 📊 Funcionalidades del Prototipo

### 1. Gestión de Ventas y Flujo de Caja
El núcleo operativo presenta un diseño de "panel dividido". Incluye un formulario intuitivo para el registro de productos, una **calculadora de vuelto** integrada y un historial dinámico que permite la trazabilidad total de la jornada.

### 2. Dashboard Analítico de Resultados (KPIs)
El sistema actúa como una herramienta de inteligencia de negocios. Mediante tarjetas visuales de alto contraste, se visualizan:
* **Ingresos Brutos:** Total de ventas percibido.
* **Costos Operativos:** Inversión en productos vendidos.
* **Utilidad Neta:** El margen de beneficio real después de costos.

### 3. Detección Temprana de Pérdidas
El software incluye un algoritmo preventivo que segrega automáticamente productos que no generen beneficios. Si un ítem registra un saldo negativo, el sistema lo despliega en un panel de alerta roja para facilitar la toma de decisiones administrativas.

### 4. Control de Anulaciones y Logística de Insumos
* **Anulaciones:** Permite revertir transacciones generando automáticamente un comprobante de reintegro.
* **Implementos:** Lista de verificación interactiva para asegurar que el local cuente siempre con los recursos necesarios (aseo, papelería, etc.).

---

## 📈 Trabajo Pendiente y Mejoras Futuras
A pesar del avance funcional, se han proyectado las siguientes áreas para la entrega final:
* **Persistencia en la Nube:** Migración de almacenamiento local a una solución de base de datos remota para acceso multiusuario.
* **Seguridad:** Implementación de un sistema de autenticación con roles (Administrador vs. Vendedor).
* **Exportación de Reportes:** Generación automática de balances y boletas en formato PDF.
* **Módulo de Clientes:** Registro y trazabilidad de compras asociadas al RUT del cliente.

---
