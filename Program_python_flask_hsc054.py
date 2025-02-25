from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Koneksi ke MongoDB Atlas
MongoURL = "mongodb+srv://rizkiefendi1:ovxClCUWyCNtavFD@man1.u2bs3.mongodb.net/?retryWrites=true&w=majority&appName=MAN1"
db_name = "sensor_db"
collection_name = "sensor_data"

client = MongoClient(MongoURL)
db = client[db_name]  # Menggunakan db_name yang benar
collection = db[collection_name]

@app.route('/save', methods=["POST"])
def save_data():
    data = request.get_json()  
    suhu = data.get("suhu")
    kelembaban = data.get("kelembaban")
    timestamp = datetime.datetime.utcnow()  # Waktu saat data diterima (UTC)
    
    simpan = {
        "suhu": suhu,
        "kelembaban": kelembaban,
        "timestamp": timestamp
    }
    collection.insert_one(simpan)

    return jsonify({"Pesan": "success", "timestamp": timestamp.isoformat()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
