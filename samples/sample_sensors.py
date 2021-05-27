try:
    import board
    import adafruit_sht31d
    import Adafruit_GPIO.SPI as SPI
    import Adafruit_SSD1306 as SSD
except:
    print("Cannot import required libraries")


def get_SHT31():
    i2c = board.I2C()
    sensor = adafruit_sht31d.SHT31D(i2c)
    for idx in range(5):
        h = sensor.relative_humidity
        c = sensor.temperature
        print(f"Temp:{c} and humidity:{h}")


sensors = [
    ("SHT31",get_SHT31),
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