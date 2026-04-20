# Prototipo Funcional: Sistema Modular de Registro de Ventas
## Documentación Técnica y Análisis de Ingeniería

**Nombres:** Catalina Vergara, Francisco Benavides  
**Universidad:** Universidad Católica de Temuco (UCT)  
**Fecha de Entrega:** 19 de abril de 2026

---

## Índice
1. [Introducción](#introducción)
2. [Especificaciones Técnicas y Configuración](#1-especificaciones-técnicas-y-configuración)
3. [Guía de Funcionamiento y Forma de Uso](#2-guía-de-funcionamiento-y-forma-de-uso)
4. [Reflexión sobre el Proceso de Desarrollo](#3-reflexión-sobre-el-proceso-de-desarrollo)
5. [Conclusión](#conclusión)

---

## Introducción
El proyecto **"Sistema DUMA Pro"** surge de la necesidad de modernizar la gestión comercial en negocios locales, sustituyendo procesos manuales por una solución digital centralizada. Como ingenieros en formación, nuestro objetivo fue diseñar una plataforma que no solo capture transacciones, sino que transforme esos datos en **Inteligencia de Negocios**. Bajo una estética premium denominada *Onyx & Gold*, el sistema ofrece un entorno seguro, escalable y conectado en tiempo real a la nube a través de Google Firebase, permitiendo a los administradores tomar decisiones informadas basadas en utilidades reales y detección de pérdidas.

---

## 1. Especificaciones Técnicas y Configuración
El sistema se basa en un *stack* tecnológico moderno de Python, diseñado para ser ligero, eficiente y con persistencia de datos en la nube.

### 1.1 Librerías Requeridas y Dependencias
Para garantizar el funcionamiento de todos los módulos, es imperativo instalar las siguientes librerías:

* **Streamlit:** Framework principal para la interfaz web reactiva.
* **Firebase-Admin:** SDK oficial para la conexión con *Google Cloud Firestore*.
* **Bcrypt:** Librería de *hashing* criptográfico para protección de credenciales.
* **Pandas:** Gestión de datos y lógica contable.
* **Plotly:** Motor de gráficos dinámicos e interactivos.

### 1.2 Instrucciones de Instalación y Seguridad
1.  **Instalar dependencias:**
    ```bash
    pip install streamlit pandas plotly firebase-admin bcrypt
    ```
2.  **Configuración de la Llave de Seguridad:**
    Es fundamental que el archivo `firebase-key.json` se encuentre en la raíz del proyecto para permitir la conexión con la base de datos encriptada.
3.  **Ejecutar la aplicación:**
    ```bash
    python -m streamlit run app.py
    ```

### 1.3 Estructura Modular del Proyecto
* `app.py`: Controlador principal (navegación y roles).
* `modules/database.py`: Persistencia en Firebase y seguridad.
* `modules/styles.py`: Capa visual (CSS Custom).
* `modules/tabs_content.py`: Lógica de negocio y motores de búsqueda.

---

## 2. Guía de Funcionamiento y Forma de Uso

### 2.1 Sistema de Autenticación y Cambio de Roles
* **Acceso Administrador:** Gestión estratégica. 
    * **Usuario:** `admin` | **Contraseña:** `123456`
    * Permite ver Dashboard, Implementos y Devoluciones.
* **Acceso Empleado:** Operación diaria rápida.
    * Acceso directo a Ventas y Devoluciones.
* **Cerrar Sesión:** Botón disponible en la barra lateral para limpiar el estado de sesión.

### 2.2 Módulos Principales
* **Ventas:** Formulario validado con normalización de RUT mediante Regex y calculadora de vuelto integrada.
* **Dashboard (Admin):** Visualización de KPIs (Ingresos, Costos, Utilidad Neta) y detección visual de productos con margen negativo.
* **Implementos (Admin):** Registro de faltantes y lista dinámica de suministros para reposición.
* **Devoluciones:** Búsqueda por ID único en Firebase y actualización del estado de venta a "Anulada".

---

## 3. Reflexión sobre el Proceso de Desarrollo

### 3.1 Visión y Propósito
Buscamos trascender el prototipo académico para ofrecer una solución empresarial que equilibre la **eficiencia operativa** del empleado con la **visión estratégica** del administrador.

### 3.2 Desafíos Enfrentados
* **Persistencia de Datos:** Superamos la volatilidad de datos locales migrando a **Google Cloud Firestore (NoSQL)**.
* **Integridad de la Información:** Implementamos motores de validación estricta para evitar que datos mal ingresados corrompieran los análisis financieros.

### 3.3 Intervención de IA y Aporte Humano
* **Apoyo de la IA:** Facilitó el diseño visual con CSS, la implementación técnica de `bcrypt` y la resolución de errores de conexión.
* **Autoría Propia (La Estructura):** Nosotros diseñamos la arquitectura modular, la lógica de cálculo de márgenes, la jerarquía de roles y las reglas de validación de negocio. La IA fue la herramienta; nosotros los arquitectos.

### 3.4 Aspectos Técnicos Complejos
Mantenemos una actitud de aprendizaje sobre la **latencia asíncrona** de Google Cloud y la **matemática interna de encriptación** de Bcrypt, los cuales aplicamos funcionalmente aunque su teoría profunda sigue siendo objeto de estudio.

---

## Conclusión
El **"Sistema DUMA Pro"** integra programación, bases de datos y diseño UX para profesionalizar la gestión de negocios. Logramos hitos clave en seguridad (encriptación), decisiones basadas en datos (Dashboard de utilidades) y escalabilidad (nube), consolidando nuestra base en el desarrollo de software moderno.
