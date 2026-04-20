import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from modules.database import save_venta, load_ventas, init_db
import time
import re
from collections import Counter

def render_ventas():
    st.title("💸 Registro de Ventas")
    
    # 1. Cargar datos y asegurar orden por ID
    try:
        df_actual = load_ventas()
        if not df_actual.empty:
            # LIMPIEZA CRÍTICA: Asegurar que ID sea numérico y quitar posibles nulos
            df_actual["ID"] = pd.to_numeric(df_actual["ID"], errors='coerce').fillna(0).astype(int)
            # Ordenamos de mayor a menor para la vista
            df_actual = df_actual.sort_values(by="ID", ascending=False)
    except Exception as e:
        st.error(f"Error al cargar base de datos: {e}")
        df_actual = pd.DataFrame()

    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

    if st.session_state.auth_status != "admin":
        with st.sidebar:
            st.header("🛒 Nueva Transacción")
            
            # --- SECCIÓN 1: AÑADIR AL CARRITO ---
            with st.form("agregar_producto", clear_on_submit=True):
                prod = st.text_input("📦 Nombre del Producto", placeholder="Ej: Café")
                
                col_p, col_q = st.columns([2, 1])
                with col_p:
                    p_uni = st.number_input("💰 Precio ($)", min_value=0.0, step=100.0, value=0.0)
                with col_q:
                    cant_input = st.selectbox("Cant.", options=list(range(1, 11)))
                
                c_uni = st.number_input("💵 Costo Unitario ($)", min_value=0.0, step=100.0, value=0.0)
                
                if st.form_submit_button("➕ Añadir al Carrito", use_container_width=True):
                    if prod and p_uni > 0:
                        for _ in range(cant_input):
                            st.session_state.carrito.append({
                                "nombre": prod, 
                                "costo": float(c_uni), 
                                "precio": float(p_uni)
                            })
                        st.toast(f"Añadido: {prod} (x{cant_input})", icon="🛒")
                        st.rerun()
                    else:
                        st.error("⚠️ Nombre y Precio son obligatorios")

            # --- SECCIÓN 2: RESUMEN Y REGISTRO FINAL ---
            monto_total_carrito = sum(item['precio'] for item in st.session_state.carrito) if st.session_state.carrito else 0.0
            
            if st.session_state.carrito:
                st.divider()
                st.subheader("📋 Resumen")
                nombres_temp = [item['nombre'] for item in st.session_state.carrito]
                resumen_visual = Counter(nombres_temp)
                for nombre, cantidad in resumen_visual.items():
                    st.caption(f"• {nombre} (x{cantidad})")
                
                st.write(f"### Total: ${monto_total_carrito:,.0f}")

                if st.button("🗑️ Vaciar Carrito", use_container_width=True):
                    st.session_state.carrito = []
                    st.rerun()

                with st.form("registro_final"):
                    rut_input = st.text_input("🆔 RUT del Cliente", placeholder="12345678-K")
                    if st.form_submit_button("🚀 Finalizar y Registrar Venta", use_container_width=True):
                        rut_limpio = re.sub(r'[^0-9kK]', '', rut_input)
                        if not rut_input or len(rut_limpio) < 7:
                            st.error("⚠️ RUT Inválido.")
                        else:
                            try:
                                # --- LÓGICA DE ID REFORZADA ---
                                # Volvemos a leer para evitar que otro usuario haya tomado la ID
                                df_temp = load_ventas()
                                if not df_temp.empty:
                                    ids_existentes = pd.to_numeric(df_temp["ID"], errors='coerce').fillna(0).astype(int)
                                    nueva_id = int(ids_existentes.max() + 1)
                                else:
                                    nueva_id = 1
                                
                                # Agrupación para DB
                                nombres_f = [item['nombre'] for item in st.session_state.carrito]
                                resumen_db = ", ".join([f"{n} (x{c})" for n, c in Counter(nombres_f).items()])
                                
                                nueva_venta = {
                                    "ID": nueva_id, 
                                    "RUT": rut_input.upper(), 
                                    "Producto": resumen_db,
                                    "Venta Total": float(monto_total_carrito),
                                    "Costo Total": float(sum(item['costo'] for item in st.session_state.carrito)),
                                    "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                    "Estado": "Completada"
                                }
                                
                                save_venta(nueva_venta)
                                st.session_state.carrito = [] 
                                st.success(f"✅ Venta #{nueva_id} registrada")
                                time.sleep(1.2)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al guardar: {e}")

            # --- SECCIÓN 3: CALCULADORA ---
            st.divider()
            st.metric("A Cobrar", f"${monto_total_carrito:,.0f}")
            pago = st.number_input("Paga con ($):", min_value=0.0, step=500.0, key="pago_side")
            if st.button("⚖️ Calcular", use_container_width=True):
                if monto_total_carrito > 0 and pago >= monto_total_carrito:
                    st.success(f"Vuelto: ${pago - monto_total_carrito:,.0f}")
                else:
                    st.error("Monto insuficiente")

    # --- HISTORIAL ---
    st.markdown("### 📋 Historial en la Nube")
    if not df_actual.empty:
        st.dataframe(df_actual, use_container_width=True)
    else:
        st.info("Sin registros.")

def render_dashboard():
    st.title("📊 Análisis de Resultados")
    df_ventas = load_ventas()
    df_completadas = df_ventas[df_ventas["Estado"] == "Completada"] if not df_ventas.empty else pd.DataFrame()
    
    if not df_completadas.empty:
        df_completadas["Venta Total"] = pd.to_numeric(df_completadas["Venta Total"])
        df_completadas["Costo Total"] = pd.to_numeric(df_completadas["Costo Total"])
        
        t_ingresos = df_completadas["Venta Total"].sum()
        t_costos = df_completadas["Costo Total"].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos", f"${t_ingresos:,.0f}")
        col2.metric("Costos", f"${t_costos:,.0f}")
        col3.metric("Utilidad", f"${(t_ingresos - t_costos):,.0f}")

        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure(data=[
                go.Bar(name='Ingresos', x=['Totales'], y=[t_ingresos], marker_color='#2ecc71'),
                go.Bar(name='Costos', x=['Totales'], y=[t_costos], marker_color='#e74c3c')
            ])
            fig.update_layout(title='Balance General', template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # LIMPIEZA PARA EL GRÁFICO DE PIZZA
            df_plot = df_completadas.copy()
            df_plot["Producto"] = df_plot["Producto"].str.split(", ")
            df_plot = df_plot.explode("Producto")
            df_plot["Producto"] = df_plot["Producto"].str.replace(r'\s*\(.*?\)', '', regex=True).str.strip()
            
            df_prod = df_plot.groupby("Producto")["Venta Total"].sum().reset_index()
            fig_prod = px.pie(df_prod, values='Venta Total', names='Producto', title="Ventas por Producto (Limpio)")
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
            opciones = ventas_anulables.apply(lambda x: f"ID: {x['ID']} | {x['Producto']}", axis=1)
            seleccion = st.selectbox("Venta a anular:", opciones)
            id_anular = int(seleccion.split("|")[0].split(":")[1].strip())
            
            if st.button("❌ Confirmar Anulación", type="primary"):
                try:
                    db = init_db()
                    docs = db.collection("ventas").where("ID", "==", id_anular).stream()
                    for doc in docs:
                        doc.reference.update({"Estado": "Anulada"})
                    st.success("Anulada correctamente.")
                    time.sleep(1.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

def render_implementos():
    st.title("📦 Implementos")
    if 'pendientes' not in st.session_state: st.session_state.pendientes = []
    item = st.text_input("¿Qué falta?")
    if st.button("Añadir"):
        if item:
            st.session_state.pendientes.append(item)
            st.rerun()
        for p in st.session_state.pendientes: 
            st.write(f"✅ {p}")
        else:
            st.caption("La lista está vacía.")