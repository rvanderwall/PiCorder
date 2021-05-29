from time import sleep
try:
    import board
    import adafruit_sht31d
    import adafruit_bmp280
except Exception as ex:
    print(ex)
    print("Cannot import required libraries")

# I2C Debugging
#  i2cdiscover 1

def get_SHT31():
    print("Get i2c board")
    i2c = board.I2C()
    print("Get sensor")
    sensor = adafruit_sht31d.SHT31D(i2c)
    for idx in range(5):
        h = sensor.relative_humidity
        c = sensor.temperature
        print(f"Temp:{c} and humidity:{h}")
        sleep(1)

def get_BMP280():
    print("Get i2c board")
    i2c = board.I2C()
    print("Get sensor")
    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    sensor.sea_level_pressure = 1013.25
    for idx in range(5):
        t = sensor.temperature
        p = sensor.pressure
        a = sensor.altitude
        print(f"Temp:{t}, pressure:{p}, altitude:{a}")
        sleep(1)
        
def get_all():
    print("Get i2c board")
    i2c = board.I2C()
    print("Get sensor")
    sht31 = adafruit_sht31d.SHT31D(i2c)
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    bmp280.sea_level_pressure = 1013.25
    for idx in range(5):
        t = bmp280.temperature
        p = bmp280.pressure
        a = bmp280.altitude
        c = sht31.temperature
        h = sht31.relative_humidity
        print(f"Temp:{c} and humidity:{h}")
        print(f"Temp:{t}, pressure:{p}, altitude:{a}")
        sleep(1)

sensors = [
    ("SHT31",get_SHT31),
    ("BMP280",get_BMP280),
    ("all",get_all),
    ("exit",exit)]

def run():
    while True:
        for idx in range(len(sensors)):
            print(f"{idx} - {sensors[idx][0]}")

        c = input("Enter choice: ")
        c = int(c)
        fnc = sensors[c][1]
        fnc()


if __name__ == "__main__":
    run()
