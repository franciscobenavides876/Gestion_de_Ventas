import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

def init_db():
    """Inicializa la conexión con Firestore usando tu nueva llave."""
    if not firebase_admin._apps:
        # Aquí es donde el código busca el archivo que acabas de descargar
        cred = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

def save_venta(datos):
    """Envía la venta con el RUT a la base de datos de Firebase."""
    db = init_db()
    db.collection("ventas").add(datos)

def load_ventas():
    """Trae todas las ventas guardadas en la nube."""
    db = init_db()
    ventas_ref = db.collection("ventas").stream()
    listado = [doc.to_dict() for doc in ventas_ref]
    return pd.DataFrame(listado) if listado else pd.DataFrame(columns=["ID", "RUT", "Producto", "Venta Total", "Estado"])