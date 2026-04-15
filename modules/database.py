import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import os
import bcrypt

# ==========================================
# 1. HASHING SEGURO
# ==========================================

def generar_hash(password_plana):
    return bcrypt.hashpw(
        password_plana.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')


def verificar_password_segura(password_ingresada, hash_almacenado):
    try:
        return bcrypt.checkpw(
            password_ingresada.encode('utf-8'),
            hash_almacenado.encode('utf-8')
        )
    except Exception as e:
        print("❌ Error bcrypt:", e)
        return False


# ==========================================
# 2. CONEXIÓN FIREBASE
# ==========================================

def init_db():
    if not firebase_admin._apps:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cert_path = os.path.join(base_dir, "firebase-key.json")

        if not os.path.exists(cert_path):
            cert_path = "firebase-key.json"

        cred = credentials.Certificate(cert_path)
        firebase_admin.initialize_app(cred)

    return firestore.client()


# ==========================================
# 3. LOGIN CORREGIDO
# ==========================================

def verificar_usuario(usuario_ingresado, password_ingresada):
    try:
        db = init_db()
        doc = db.collection("administrador").document("admin").get()

        if not doc.exists:
            print("❌ Documento no existe")
            return False

        datos = doc.to_dict()

        db_usuario = str(datos.get("usuario", "")).strip().lower()
        db_hash = str(datos.get("contraseña", "")).strip()

        user_input = str(usuario_ingresado).strip().lower()
        pass_input = str(password_ingresada).strip()

        print("DB usuario:", db_usuario)
        print("Input usuario:", user_input)

        if db_usuario != user_input:
            print("❌ Usuario no coincide")
            return False

        if verificar_password_segura(pass_input, db_hash):
            print("✅ Login correcto")
            return True
        else:
            print("❌ Password incorrecta")
            return False

    except Exception as e:
        print("❌ Error en login:", e)
        return False


# ==========================================
# 4. RESETEAR PASSWORD (USAR UNA VEZ)
# ==========================================

def resetear_password_admin(nueva_clave):
    try:
        db = init_db()
        hash_nuevo = generar_hash(nueva_clave)

        db.collection("administrador").document("admin").update({
            "contraseña": hash_nuevo,
            "usuario": "admin"  # lo normalizamos también
        })

        print("✅ Password hasheada y subida correctamente")
        print("🔐 Nuevo hash:", hash_nuevo)

    except Exception as e:
        print("❌ Error:", e)


# ==========================================
# 5. VENTAS (igual que tenías)
# ==========================================

def save_venta(datos):
    try:
        db = init_db()
        db.collection("ventas").add(datos)
        return True
    except Exception as e:
        print(e)
        return False


def load_ventas():
    try:
        db = init_db()
        ventas = db.collection("ventas").stream()
        lista = [doc.to_dict() for doc in ventas]
        return pd.DataFrame(lista) if lista else pd.DataFrame()
    except Exception as e:
        print(e)
        return pd.DataFrame()


# ==========================================
# 6. EJECUCIÓN
# ==========================================

if __name__ == "__main__":
    # ⚠️ EJECUTA ESTO UNA SOLA VEZ
    resetear_password_admin("123456")