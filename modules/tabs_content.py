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
    
    # Cargar datos de la DB
    df_actual = load_ventas()

    # Inicializar el carrito en la sesión si no existe
    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

    if st.session_state.auth_status != "admin":
        with st.sidebar:
            st.header("🛒 Nueva Transacción")
            
            # --- SECCIÓN 1: FORMULARIO PARA AÑADIR PRODUCTOS AL CARRITO ---
            with st.form("agregar_producto", clear_on_submit=True):
                prod = st.text_input("📦 Nombre del Producto", placeholder="Ej: Café")
                c_uni = st.number_input("💵 Costo de Compra ($)", min_value=0.0, step=100.0, value=0.0)
                p_uni = st.number_input("💰 Precio de Venta ($)", min_value=0.0, step=100.0, value=0.0)
                
                btn_add = st.form_submit_button("➕ Agregar al Carrito", use_container_width=True)
                
                if btn_add:
                    if prod and p_uni > 0:
                        # Añadimos el producto a la lista temporal
                        item = {"nombre": prod, "costo": float(c_uni), "precio": float(p_uni)}
                        st.session_state.carrito.append(item)
                        st.toast(f"{prod} añadido", icon="🛒")
                        st.rerun() # Recargar para actualizar montos en calculadora
                    else:
                        st.error("Nombre y Precio son obligatorios")

            # --- SECCIÓN 2: RESUMEN DEL CARRITO Y REGISTRO FINAL ---
            monto_total_carrito = sum(item['precio'] for item in st.session_state.carrito) if st.session_state.carrito else 0.0
            
            if st.session_state.carrito:
                st.divider()
                st.subheader("📋 Resumen del Carrito")
                
                # Listar productos agregados
                for i, item in enumerate(st.session_state.carrito):
                    st.caption(f"{i+1}. {item['nombre']} — ${item['precio']:,.0f}")
                
                st.write(f"### Total: ${monto_total_carrito:,.0f}")

                if st.button("🗑️ Vaciar Carrito", use_container_width=True):
                    st.session_state.carrito = []
                    st.rerun()

                # Formulario para el RUT y Guardar en DB
                with st.form("registro_final"):
                    rut_input = st.text_input("🆔 RUT del Cliente", placeholder="12345678-K")
                    btn_reg = st.form_submit_button("🚀 Finalizar y Registrar Venta", use_container_width=True)

                    if btn_reg:
                        rut_limpio = re.sub(r'[^0-9kK]', '', rut_input)
                        if not rut_input or len(rut_limpio) < 7:
                            st.error("⚠️ RUT Inválido.")
                        else:
                            # --- LÓGICA DE AGRUPACIÓN (x4) ---
                            nombres = [item['nombre'] for item in st.session_state.carrito]
                            conteo = Counter(nombres)
                            # Crea el string agrupado: "Café (x3), Agua (x1)"
                            resumen_productos = ", ".join([f"{nom} (x{cant})" for nom, cant in conteo.items()])
                            
                            total_costo = sum(item['costo'] for item in st.session_state.carrito)

                            nueva_venta = {
                                "ID": int(datetime.now().timestamp()), 
                                "RUT": rut_input.upper(), 
                                "Producto": resumen_productos,
                                "Venta Total": monto_total_carrito,
                                "Costo Total": total_costo,
                                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                "Estado": "Completada"
                            }
                            
                            save_venta(nueva_venta)
                            st.session_state.carrito = [] # Limpiar carrito tras éxito
                            st.success("¡Venta registrada!")
                            time.sleep(1.2)
                            st.rerun()

            # --- SECCIÓN 3: CALCULADORA DE VUELTO ---
            st.markdown("---")
            st.header("🧮 Calculadora de Vuelto")
            
            # Muestra siempre el total del carrito actual
            st.metric("Monto a Cobrar", f"${monto_total_carrito:,.0f}")
            
            with st.container(border=True):
                pago_cliente = st.number_input("Cliente paga con ($):", min_value=0.0, step=500.0, value=0.0, key="calc_pago")
                btn_calc = st.button("⚖️ Calcular Vuelto", use_container_width=True)
                
                if btn_calc:
                    if monto_total_carrito == 0:
                        st.warning("El carrito está vacío.")
                    elif pago_cliente >= monto_total_carrito:
                        vuelto = pago_cliente - monto_total_carrito
                        st.success(f"**Vuelto a devolver: ${vuelto:,.0f}**")
                    else:
                        st.error(f"**Faltan: ${abs(pago_cliente - monto_total_carrito):,.0f}**")

    # --- HISTORIAL EN EL CUERPO PRINCIPAL ---
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
                    docs = db.collection("ventas").where("ID", "==", id_anular).stream()
                    for doc in docs:
                        doc.reference.update({"Estado": "Anulada"})
                    
                    st.success(f"Venta #{id_anular} anulada exitosamente.")
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("No hay ventas activas.")

def render_implementos():
    st.title("📦 Implementos por Traer")
    if 'pendientes' not in st.session_state:
        st.session_state.pendientes = []
        
    c_in, c_li = st.columns([1, 2])
    with c_in:
        item = st.text_input("¿Qué falta en la oficina/local?")
        if st.button("Añadir"):
            if item:
                st.session_state.pendientes.append(item)
                st.rerun()
    with c_li:
        if st.session_state.pendientes:
            for p in st.session_state.pendientes:
                st.write(f"✅ {p}")
            else:
                st.caption("Lista vacía.")