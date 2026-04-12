import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def render_ventas():
    st.title("💸 Registro de Ventas")
    with st.sidebar:
        st.header("🛒 Nueva Transacción")
        with st.form("registro_venta", clear_on_submit=True):
            prod = st.text_input("📦 Nombre del Producto", placeholder="Ej: Café")
            
            # value=None elimina el cero inicial; placeholder muestra la guía sutil
            c_uni = st.number_input("💵 Costo de Compra ($)", min_value=0.0, step=100.0, value=None, placeholder="0.00")
            p_uni = st.number_input("💰 Precio de Venta ($)", min_value=0.0, step=100.0, value=None, placeholder="0.00")
            
            btn_reg = st.form_submit_button("🚀 Registrar Venta", use_container_width=True)
            
            if btn_reg:
                # Validamos que p_uni no sea None y sea mayor a 0
                if prod and p_uni is not None and p_uni > 0:
                    nueva = {
                        "ID": len(st.session_state.ventas) + 1, 
                        "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Producto": prod, 
                        "Costo Total": c_uni if c_uni is not None else 0.0, 
                        "Venta Total": p_uni, 
                        "Estado": "Completada"
                    }
                    st.session_state.ventas = pd.concat([st.session_state.ventas, pd.DataFrame([nueva])], ignore_index=True)
                    st.toast(f"¡{prod} registrado!", icon="✅")
                else:
                    st.error("Faltan datos obligatorios.")

        st.markdown("---")
        st.header("🧮 Calculadora de Vuelto")
        
        # También aplicamos value=None aquí para limpieza visual
        monto_pago = st.number_input("Cliente paga con:", min_value=0.0, step=500.0, value=None, placeholder="0.00", key="pago_cliente")
        
        if p_uni is not None and p_uni > 0:
            st.info(f"Monto a cobrar: *${p_uni:,.0f}*")
            if monto_pago is not None and monto_pago > 0:
                vuelto = monto_pago - p_uni
                if vuelto >= 0: 
                    st.success(f"Devolver: *${vuelto:,.0f}*")
                else: 
                    st.warning(f"Faltan: ${abs(vuelto):,.0f}")
        else:
            st.caption("Ingresa un precio arriba para calcular el vuelto.")

    st.markdown("### 📋 Historial Reciente")
    st.dataframe(st.session_state.ventas.sort_values(by="ID", ascending=False), use_container_width=True)

def render_dashboard():
    st.title("📊 Análisis de Resultados")
    df_completadas = st.session_state.ventas[st.session_state.ventas["Estado"] == "Completada"]
    
    if not df_completadas.empty:
        # Métricas generales
        t_ingresos = df_completadas["Venta Total"].sum()
        t_costos = df_completadas["Costo Total"].sum()
        balance = t_ingresos - t_costos
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos Reales", f"${t_ingresos:,.0f}")
        col2.metric("Costos Operativos", f"${t_costos:,.0f}", delta_color="inverse")
        col3.metric("Utilidad Neta", f"${balance:,.0f}", delta=f"{balance:,.0f}")

        if balance < 0:
            st.error(f"⚠️ Alerta: El balance actual es negativo (${abs(balance):,.0f} en pérdida).")
        
        # Procesamiento de datos por producto
        df_prod = df_completadas.groupby("Producto")[["Costo Total", "Venta Total"]].sum().reset_index()
        df_prod["Ganancia"] = df_prod["Venta Total"] - df_prod["Costo Total"]

        # --- SECCIÓN 1: BALANCE Y GANANCIAS PURAS ---
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure(data=[
                go.Bar(name='Ingresos', x=['Totales'], y=[t_ingresos], marker_color='#2ecc71'),
                go.Bar(name='Costos', x=['Totales'], y=[t_costos], marker_color='#e74c3c')
            ])
            fig.update_layout(title='Balance de Caja (General)', barmode='group', template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # FILTRO: Solo productos con ganancias mayores a cero
            df_solo_ganancias = df_prod[df_prod["Ganancia"] > 0]
            if not df_solo_ganancias.empty:
                fig_prod = px.bar(df_solo_ganancias, x="Producto", y="Ganancia", 
                                 color_discrete_sequence=['#2ecc71'],
                                 title="Ganancias Netas por Producto")
                fig_prod.update_layout(template="plotly_dark")
                st.plotly_chart(fig_prod, use_container_width=True)
            else:
                st.info("No hay productos con ganancias positivas.")

        # --- SECCIÓN 2: DETALLE DE PÉRDIDAS EXCLUSIVO ---
        st.markdown("---")
        df_perdidas = df_prod[df_prod["Ganancia"] < 0].copy()

        if not df_perdidas.empty:
            st.subheader("🚩 Detalle de Pérdidas")
            df_perdidas["Monto Perdido"] = df_perdidas["Ganancia"].abs()
            
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                # Gráfico de barras que muestra el monto de pérdida
                fig_p = px.bar(df_perdidas, x="Producto", y="Monto Perdido",
                             title="Productos con Saldo Negativo",
                             color_discrete_sequence=['#e74c3c'])
                fig_p.update_layout(template="plotly_dark")
                st.plotly_chart(fig_p, use_container_width=True)
            
            with p_col2:
                st.write("📋 **Resumen de pérdidas detectadas:**")
                for _, row in df_perdidas.iterrows():
                    st.error(f"El producto **{row['Producto']}** generó una pérdida literal de **${row['Monto Perdido']:,.0f}**")
        else:
            st.success("✅ No se registran pérdidas en los productos actuales.")

    else:
        st.info("No hay ventas completadas para mostrar en el Dashboard.")

def render_implementos():
    st.title("📦 Implementos por Traer")
    c_in, c_li = st.columns([1, 2])
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

def render_devoluciones():
    st.title("🔄 Gestión de Anulaciones")
    ventas_anulables = st.session_state.ventas[st.session_state.ventas["Estado"] == "Completada"]
    if not ventas_anulables.empty:
        id_anular = st.selectbox("ID de la Venta a anular:", ventas_anulables["ID"])
        if st.button("❌ Confirmar Anulación y Boleta", type="primary"):
            st.session_state.ventas.loc[st.session_state.ventas["ID"] == id_anular, "Estado"] = "Anulada"
            st.success(f"Venta #{id_anular} anulada.")
            v_data = st.session_state.ventas[st.session_state.ventas["ID"] == id_anular].iloc[0]
            st.code(f"--- BOLETA DE ANULACIÓN ---\nID: {v_data['ID']} | FECHA: {v_data['Fecha']}\nPRODUCTO: {v_data['Producto']}\nMONTO REINTEGRADO: ${v_data['Venta Total']:,.0f}\n---------------------------")
    else:
        st.info("No hay ventas activas disponibles para anular.")