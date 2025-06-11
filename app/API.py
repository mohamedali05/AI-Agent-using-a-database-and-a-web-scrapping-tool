from flask import Flask, jsonify
import psycopg2
import os
import time

time.sleep(5)
app = Flask(__name__)

# Configuration depuis les variables d'environnement
host = os.getenv("DB_HOST", "localhost")
api_port = int(os.getenv("API_PORT", "5000"))

# Connect to your local PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",  
    user="postgres",
    password="3Gy5uwht4*",
    host=host,  
    port="5432"
)

# === 1. TABLE Product ===

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running."})

@app.route("/products", methods=["GET"])
def get_all_products():
    cur = conn.cursor()
    cur.execute("SELECT * FROM Product;")
    rows = cur.fetchall()
    cur.close()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "nom": row[1],
            "description": row[2],
            "ingredients": row[3],
            "prix": float(row[4])
        })
    return jsonify(result)

@app.route("/product/<string:name>", methods=["GET"])
def get_product_by_name(name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Product WHERE nom ILIKE %s;", (f"%{name}%",))
    rows = cur.fetchall()
    cur.close()

    if not rows:
        return jsonify({"error": "Product not found"}), 404

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "nom": row[1],
            "description": row[2],
            "ingredients": row[3],
            "prix": float(row[4])
        })
    return jsonify(result)

# === 2. TABLE Store ===

@app.route("/stores", methods=["GET"])
def get_all_stores():
    cur = conn.cursor()
    cur.execute("SELECT * FROM Store;")
    rows = cur.fetchall()
    cur.close()
    return jsonify([{"id": row[0], "nom": row[1], "adresse": row[2]} for row in rows])

@app.route("/store/<string:name>", methods=["GET"])
def get_store_by_name(name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Store WHERE nom ILIKE %s;", (f"%{name}%",))
    rows = cur.fetchall()
    cur.close()

    if not rows:
        return jsonify({"error": "Store not found"}), 404

    return jsonify([{"id": row[0], "nom": row[1], "adresse": row[2]} for row in rows])

# === 3. TABLE Store_Products ===

@app.route("/store-products", methods=["GET"])
def get_all_store_products():
    cur = conn.cursor()
    cur.execute("""
        SELECT s.nom AS store_name, p.nom AS product_name, sp.stock_unit
        FROM Store_Products sp
        JOIN Store s ON sp.id_store = s.id
        JOIN Product p ON sp.id_product = p.id;
    """)
    rows = cur.fetchall()
    cur.close()
    return jsonify([
        {"store": row[0], "product": row[1], "stock_unit": row[2]} for row in rows
    ])

@app.route("/store-products/<string:store_name>", methods=["GET"])
def get_store_products_by_store_name(store_name):
    cur = conn.cursor()
    cur.execute("""
        SELECT p.nom, sp.stock_unit
        FROM Store_Products sp
        JOIN Product p ON sp.id_product = p.id
        JOIN Store s ON sp.id_store = s.id
        WHERE s.nom ILIKE %s;
    """, (f"%{store_name}%",))
    rows = cur.fetchall()
    cur.close()

    if not rows:
        return jsonify({"error": "No products found for this store"}), 404

    return jsonify([{"product": row[0], "stock_unit": row[1]} for row in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=api_port, debug=True)