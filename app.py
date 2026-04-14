import streamlit as st
from modules.database import init_db 
from modules.styles import apply_styles
from modules.tabs_content import (
    render_ventas, 
    render_dashboard, 
    render_implementos, 
    render_devoluciones
)

# 1. Configuración de la interfaz (Mantenemos tu estilo Onyx & Gold)
st.set_page_config(page_title="Gestión Empresarial Pro", page_icon="🏢", layout="wide")

# 2. Inicializar conexión a la nube y estilos premium
# init_db() ahora busca el archivo firebase-key.json para conectar con Firestore
init_db() 
apply_styles()

# 3. Navegación principal mediante pestañas
tab1, tab2, tab3, tab4 = st.tabs(["💰 Ventas", "📈 Dashboard", "📦 Implementos", "🔄 Devoluciones"])

with tab1:
    # Este módulo ahora incluye el campo para registrar el RUT del cliente
    render_ventas()

with tab2:
    # El dashboard ahora procesará los datos descargados de Firebase
    render_dashboard()

with tab3:
    render_implementos()

with tab4:
    render_devoluciones()