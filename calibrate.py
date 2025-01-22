import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)

# Set the input channel to A1
channel = AnalogIn(ads, ADS1115.P1)

# Reference values (adjust if necessary)
adc_max_value = 32767  # 16-bit ADC max value
vcc = 5.0  # Reference voltage for the sensor

print("Starting pH Sensor Calibration...")

while True:
    # Read the raw ADC value
    raw_value = channel.value

    # Calculate the voltage using the same formula as in the Arduino code
    voltage = raw_value * (vcc / adc_max_value)

    # Print the raw ADC value and voltage
    print(f"Raw ADC Value: {raw_value}, Voltage: {voltage:.2f} V")

    time.sleep(0.5)
