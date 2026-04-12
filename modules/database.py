import streamlit as st
import pandas as pd

def init_session():
    if 'ventas' not in st.session_state:
        st.session_state.ventas = pd.DataFrame(columns=["ID", "Fecha", "Producto", "Costo Total", "Venta Total", "Estado"])
    if 'pendientes' not in st.session_state:
        st.session_state.pendientes = []