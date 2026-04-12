import streamlit as st
from modules.database import init_session
from modules.styles import apply_styles
from modules.tabs_content import (
    render_ventas, 
    render_dashboard, 
    render_implementos, 
    render_devoluciones
)

# 1. Configuración de página
st.set_page_config(page_title="Gestión Empresarial Pro", page_icon="🏢", layout="wide")

# 2. Inicializar datos y estilos
init_session()
apply_styles()

# 3. Navegación principal
tab1, tab2, tab3, tab4 = st.tabs(["💰 Ventas", "📈 Dashboard", "📦 Implementos", "🔄 Devoluciones"])

with tab1:
    render_ventas()

with tab2:
    render_dashboard()

with tab3:
    render_implementos()

with tab4:
    render_devoluciones()