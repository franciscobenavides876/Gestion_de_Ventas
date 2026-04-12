import streamlit as st

def apply_styles():
    """Aplica el diseño premium Onyx & Gold a la aplicación."""
    st.markdown("""
        <style>
        /* 1. Fondo Principal de la App (Onyx) */
        .stApp {
            background-color: #111111;
            color: #FFFFF0; /* Texto principal Crema/Marfil */
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        /* 2. Estilo de los Títulos Principales (H1) */
        h1 {
            color: #D4AF37 !important; /* Dorado sutil para títulos */
            font-weight: 300 !important;
            letter-spacing: 1px;
        }

        /* 3. Tarjetas de Métricas (Dashboard) */
        .stMetric {
            background-color: #1E1E1E; /* Fondo Carbón */
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #333333; /* Borde sutil */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5); /* Sombra elegante */
        }
        
        /* Etiquetas y valores de métricas */
        [data-testid="stMetricLabel"] { color: #778899 !important; text-transform: uppercase; font-size: 13px; }
        [data-testid="stMetricValue"] { color: #FFFFF0 !important; font-weight: bold; }

        /* 4. Estilo de las Pestañas (Tabs) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 15px;
            background-color: #1A1A1A;
            padding: 10px;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            color: #778899;
            border-radius: 8px;
            border: none;
        }

        /* Pestaña seleccionada */
        .stTabs [aria-selected="true"] {
            background-color: #2D2D2D !important;
            color: #D4AF37 !important;
            font-weight: bold;
        }

        /* 5. Botones con borde dorado */
        .stButton>button {
            background-color: transparent;
            color: #D4AF37;
            border: 1px solid #D4AF37;
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #D4AF37;
            color: #111111;
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
        }

        /* 6. Inputs y Formularios */
        .stTextInput>div>div>input, .stNumberInput>div>div>input, [data-testid="stForm"] {
            background-color: #1E1E1E !important;
            color: #FFFFF0;
            border: 1px solid #333333 !important;
            border-radius: 8px;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0c0c0c;
            border-right: 1px solid #222;
        }
        </style>
        """, unsafe_allow_html=True)

def get_chart_palette():
    """Devuelve la paleta de colores sofisticada para los gráficos de Plotly."""
    return {
        'bg': '#1E1E1E',
        'text': '#FFFFF0',
        'grid': '#333333',
        'primary': '#D4AF37',   # Dorado para ganancias e ingresos
        'secondary': '#778899'  # Azul Acero para costos y pérdidas
    }