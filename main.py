from machine import Pin, I2C
from lib_bme680 import *
import time
import ntptime
import lib_send_data as send
import lib_oled as oled

# ============================================================
# CONFIGURAÇÕES WIFI
# ============================================================

WIFI_SSID = "Ap1208_2G"
WIFI_PASSWORD = "20081995"

# "BME680 RPi Pico - Pin assignment
i2c = I2C(id=1, scl=Pin(3), sda=Pin(2))

bme = BME680_I2C(i2c=i2c)

#curl -v -X POST http://192.168.18.34:8080/api/v1/n9y3WpZhhg6MpBLQGu8l/telemetry --header Content-Type:application/json --data "{temperature:25}"

URL = "http://192.168.18.34:8080/api/v1/n9y3WpZhhg6MpBLQGu8l/telemetry"

# Conecta ao Wi-Fi
wifi = send.conectar_wifi(WIFI_SSID, WIFI_PASSWORD)

print(wifi)

#ntptime.settime()

while True:
  try:
    temp = round(bme.temperature, 2)
    #temp = (bme.temperature) * (9/5) + 32
    #temp = str(round(temp, 2)) + 'F'
    
    hum = round(bme.humidity, 2)
    
    pres = round(bme.pressure, 2)
    
    gas = round(bme.gas/1000, 2)
    
    dado_envio = {
        "timestamp": time.time(),
        "hum": hum,
        "temp": temp,
        "pres": pres,
        "gas": gas
    }
    sucesso = send.enviar_dados(dado_envio, URL)
    oled.update_massages(temp, hum, pres, gas)
    print(f'Temperature:{temp}  C')
    print(f'Humidity:{hum} %')
    print(f'Pressure: {pres} hPa')
    print(f'Gas: {gas} KOhms')
    print('-------')
  except OSError as e:
    print('Failed to read sensor.')
 
  time.sleep(120)



