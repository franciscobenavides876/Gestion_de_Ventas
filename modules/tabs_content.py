import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go  # ESTE ES EL IMPORT QUE FALTABA
from modules.database import save_venta, load_ventas, init_db
import time
import re

def render_ventas():
    st.title("💸 Registro de Ventas")
    df_actual = load_ventas()

    # --- RESTRICCIÓN PARA ADMIN: Ocultar Sidebar ---
    if st.session_state.auth_status != "admin":
        with st.sidebar:
            st.header("🛒 Nueva Transacción")
            with st.form("registro_venta", clear_on_submit=True):
                prod = st.text_input("📦 Nombre del Producto", placeholder="Ej: Café")
                rut_input = st.text_input("🆔 RUT del Cliente", placeholder="12345678-K")
                c_uni = st.number_input("💵 Costo de Compra ($)", min_value=0.0, step=100.0, value=None)
                p_uni = st.number_input("💰 Precio de Venta ($)", min_value=0.0, step=100.0, value=None)
                
                btn_reg = st.form_submit_button("🚀 Registrar Venta", use_container_width=True)
                
                if btn_reg:
                    rut_limpio = re.sub(r'[^0-9kK]', '', rut_input)
                    if not prod or not p_uni or not rut_input:
                        st.error("❌ Completa los campos obligatorios.")
                    elif not re.match(r"^[0-9]+[kK]?$", rut_limpio) or len(rut_limpio) < 7:
                        st.error("⚠️ RUT Inválido.")
                    else:
                        nueva_venta = {
                            "ID": int(datetime.now().timestamp()), 
                            "RUT": rut_input.upper(), 
                            "Producto": prod,
                            "Venta Total": float(p_uni),
                            "Costo Total": float(c_uni) if c_uni else 0.0,
                            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "Estado": "Completada"
                        }
                        save_venta(nueva_venta)
                        st.toast(f"¡Venta registrada!", icon="✅")
                        time.sleep(1)
                        st.rerun()

            st.markdown("---")
            st.header("🧮 Calculadora de Vuelto")
            monto_pago = st.number_input("Cliente paga con:", min_value=0.0, step=500.0, value=None, key="pago_cliente")
            
            # Intentamos obtener p_uni del formulario si existe
            if 'p_uni' in locals() and p_uni:
                st.info(f"Monto a cobrar: ${p_uni:,.0f}")
                if monto_pago:
                    vuelto = monto_pago - p_uni
                    if vuelto >= 0: st.success(f"Devolver: ${vuelto:,.0f}")
                    else: st.warning(f"Faltan: ${abs(vuelto):,.0f}")
    
    # --- VISIBLE PARA TODOS ---
    st.markdown("### 📋 Historial en la Nube")
    if not df_actual.empty:
        st.dataframe(df_actual.sort_values(by="ID", ascending=False), use_container_width=True)
    else:
        st.info("Aún no hay registros en la base de datos.")

def render_dashboard():
    st.title("📊 Análisis de Resultados")
    df_ventas = load_ventas()
    df_completadas = df_ventas[df_ventas["Estado"] == "Completada"] if not df_ventas.empty else pd.DataFrame()
    
    if not df_completadas.empty:
        t_ingresos = df_completadas["Venta Total"].sum()
        t_costos = df_completadas["Costo Total"].sum()
        balance = t_ingresos - t_costos
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos Reales", f"${t_ingresos:,.0f}")
        col2.metric("Costos Operativos", f"${t_costos:,.0f}")
        col3.metric("Utilidad Neta", f"${balance:,.0f}")

        c1, c2 = st.columns(2)
        with c1:
            # AQUÍ ES DONDE SE USABA 'go'
            fig = go.Figure(data=[
                go.Bar(name='Ingresos', x=['Totales'], y=[t_ingresos], marker_color='#2ecc71'),
                go.Bar(name='Costos', x=['Totales'], y=[t_costos], marker_color='#e74c3c')
            ])
            fig.update_layout(title='Balance General', barmode='group', template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            df_prod = df_completadas.groupby("Producto")["Venta Total"].sum().reset_index()
            fig_prod = px.pie(df_prod, values='Venta Total', names='Producto', title="Ventas por Producto")
            fig_prod.update_layout(template="plotly_dark")
            st.plotly_chart(fig_prod, use_container_width=True)
    else:
        st.info("No hay datos para el Dashboard.")

def render_devoluciones():
    st.title("🔄 Gestión de Anulaciones")
    df_ventas = load_ventas()
    
    if not df_ventas.empty:
        ventas_anulables = df_ventas[df_ventas["Estado"] == "Completada"]
        
        if not ventas_anulables.empty:
            opciones = ventas_anulables.apply(lambda x: f"ID: {x['ID']} | RUT: {x['RUT']} | {x['Producto']}", axis=1)
            seleccion = st.selectbox("Seleccione la Venta a anular:", opciones)
            
            id_anular = int(seleccion.split("|")[0].split(":")[1].strip())
            
            if st.button("❌ Confirmar Anulación", type="primary"):
                try:
                    db = init_db()
                    # Actualización transaccional en la nube de Firebase
                    docs = db.collection("ventas").where("ID", "==", id_anular).stream()
                    for doc in docs:
                        doc.reference.update({"Estado": "Anulada"})
                    
                    st.success(f"Venta #{id_anular} anulada exitosamente en la nube.")
                    
                    v_data = ventas_anulables[ventas_anulables["ID"] == id_anular].iloc[0]
                    st.code(f"--- BOLETA DE ANULACIÓN ---\nID: {v_data['ID']} | RUT: {v_data['RUT']}\nPRODUCTO: {v_data['Producto']}\nMONTO REINTEGRADO: ${v_data['Venta Total']:,.0f}\n---------------------------")
                    
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al conectar con la nube: {e}")
        else:
            st.info("No hay ventas activas para anular.")
    else:
        st.info("La base de datos está vacía.")

def render_implementos():
    st.title("📦 Implementos por Traer")
    if 'pendientes' not in st.session_state:
        st.session_state.pendientes = []
        
    c_in, c_li = st.columns([1, 2])
    with st.container():
        with c_in:
            item = st.text_input("¿Qué falta en la oficina/local?")
            if st.button("Añadir", use_container_width=True):
                if item:
                    st.session_state.pendientes.append(item)
                    st.rerun()
        with c_li:
            if st.session_state.pendientes:
                for p in st.session_state.pendientes:
                    st.write(f"✅ {p}")
            else:
                st.caption("Lista vacía.")