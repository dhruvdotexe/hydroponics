import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import os
import glob
import datetime

# Initialize I2C and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1  # ±4.096V range

# Create analog input channels
tds_channel = AnalogIn(ads, ADS.P0)
ph_channel = AnalogIn(ads, ADS.P1)

# Temperature sensor setup
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Function to read DS18B20 temperature
def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# Function to calculate TDS
def calculate_tds(voltage):
    tds = (133.42 * voltage ** 3 - 255.86 * voltage ** 2 + 857.39 * voltage) * 0.5
    return tds

# Function to calculate pH
PH_OFFSET = 0.12  # Adjust based on calibration
def calculate_ph(voltage):
    ph = 3.5 * voltage + PH_OFFSET  # Adjust formula based on calibration
    return ph

# Main loop to read all sensors
while True:
    # Read TDS sensor
    tds_voltage = tds_channel.voltage
    tds_value = calculate_tds(tds_voltage)
    print("TDS Voltage: {:.2f}V, TDS: {:.2f} ppm".format(tds_voltage, tds_value))

    # Read pH sensor
    ph_voltage = ph_channel.voltage
    ph_value = calculate_ph(ph_voltage)
    print("pH Voltage: {:.2f}V, pH: {:.2f}".format(ph_voltage, ph_value))

    # Read temperature sensor
    temp_c = read_temp()
    print("Temperature: {:.2f}°C".format(temp_c))

    print("-" * 30)
    time.sleep(2)
