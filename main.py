import network
import urequests
from machine import Pin, PWM
from time import sleep
from config import CONFIG

led = Pin(10, Pin.OUT)

def blink(times=1):
    for i in range(times):
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)

def pulse(times=1):
    pulzar = PWM(led, 5000)
    for i in range(times):
        for duty in range(0, 1024):
            pulzar.duty(duty)
            sleep(0.001)
        for duty in range(1, 1024):
            pulzar.duty(1024 - duty)
            sleep(0.001)
    pulzar.deinit()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(txpower=8.5)
if not wlan.isconnected():
    print('Connecting to wifi')
    wlan.connect(CONFIG['SSID'], CONFIG['KEY'])
    while not wlan.isconnected():
        sleep(2)
        print('still connecting...')
        led.on()
        sleep(0.2)
        led.off()
    print('WIFI connected')
    blink(5)
else:
    print('Wifi already connected! Nice.')
    blink(3)
while True:
    print('Fetching Zapier storage')
    resp = urequests.get(CONFIG['STORE_URL'] + '?key=mentioned', headers={'X-Secret': CONFIG['STORE_KEY']})
    data = resp.json()
    resp.close()
    print(data)
    if data['mentioned'] == '1':
        resp = urequests.get(CONFIG['ZAPIER_RESET_URL'])
        resp.close()
        pulse(6)
    sleep(5)
