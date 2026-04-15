import streamlit as st
from modules.database import init_db, verificar_usuario
from modules.styles import apply_styles
from modules.tabs_content import (
    render_ventas, render_dashboard, 
    render_implementos, render_devoluciones
)

st.set_page_config(page_title="Sistema DUMA Pro", page_icon="🏢", layout="wide")
apply_styles()
init_db()

if "auth_status" not in st.session_state:
    st.session_state.auth_status = None

def login():
    st.title("🏢 Gestión Empresarial")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Inicio de Sesión")
        with st.expander("🔐 Administrador", expanded=True):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.button("Ingresar como Admin", use_container_width=True):
                if verificar_usuario(u, p):
                    st.session_state.auth_status = "admin"
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
        st.markdown("---")
        if st.button("👤 Entrar como Empleado", use_container_width=True):
            st.session_state.auth_status = "empleado"
            st.rerun()

if st.session_state.auth_status is None:
    login()
else:
    with st.sidebar:
        st.write(f"Sesión: **{st.session_state.auth_status.upper()}**")
        if st.button("Cerrar Sesión"):
            st.session_state.auth_status = None
            st.rerun()

    # Renderizado condicional
    if st.session_state.auth_status == "admin":
        t1, t2, t3, t4 = st.tabs(["💰 Ventas", "📈 Dashboard", "📦 Implementos", "🔄 Devoluciones"])
        with t1: render_ventas()
        with t2: render_dashboard()
        with t3: render_implementos()
        with t4: render_devoluciones()
    else:
        t1, t4 = st.tabs(["💰 Ventas", "🔄 Devoluciones"])
        with t1: render_ventas()
        with t4: render_devoluciones()