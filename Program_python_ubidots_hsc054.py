import machine
import time
import network
import dht
import urequests

# Konfigurasi WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Abrisam Lubis", "PakeAja.")

while not wlan.isconnected():
    print("...", end="")
    time.sleep(1)

print("\nWLAN is connected")
Ubidot_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/hsc054"
Ubidot_Control_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/hsc054/lampu/lv"
Flask_URL = "http://192.168.0.43:5000/save"

sensor = dht.DHT11(machine.Pin(23))
lampu = machine.Pin(2, machine.Pin.OUT)  # Lampu di GPIO2

headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": "BBUS-EIQzpwmYBCuufrcDUrXk7U4cz5oLYO"
}

while True:
    try:
        # Membaca sensor suhu dan kelembaban
        sensor.measure()
        suhu = sensor.temperature()
        kelembaban = sensor.humidity()
        print(f"Suhu = {suhu} C, Kelembaban = {kelembaban} %")

        data = {"suhu": suhu, "kelembaban": kelembaban}

        # Kirim ke Ubidots
        try:
            response = urequests.post(Ubidot_URL, json=data, headers=headers)
            if response.status_code == 200:
                print("Data berhasil dikirim ke Ubidots")
            else:
                print(f"Gagal mengirim ke Ubidots: {response.status_code}")
            response.close()
        except Exception as e:
            print(f"Error mengirim ke Ubidots: {e}")

        # Kirim ke Flask
        try:
            response = urequests.post(Flask_URL, json=data, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                print("Data berhasil dikirim ke Flask")
            else:
                print(f"Gagal mengirim ke Flask: {response.status_code}")
            response.close()
        except Exception as e:
            print(f"Error mengirim ke Flask: {e}")

        # Ambil data kontrol lampu dari Ubidots
        try:
            response = urequests.get(Ubidot_Control_URL, headers=headers)
            if response.status_code == 200:
                lampu_status = response.json().get("value", 0)
                if lampu_status == 1:
                    lampu.value(1)  # Nyalakan lampu
                    print("Lampu ON")
                else:
                    lampu.value(0)  # Matikan lampu
                    print("Lampu OFF")
            else:
                print(f"Gagal mengambil data kontrol lampu: {response.status_code}")
            response.close()
        except Exception as e:
            print(f"Error mengambil data kontrol lampu dari Ubidots: {e}")

    except OSError as e:
        print(f"Error membaca sensor: {e}")

    time.sleep(1)  # Delay 2 detik untuk stabilitas

