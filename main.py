"""Measure distance with a KY-050 / HC-SR04-style ultrasonic sensor.

Wiring:
  Sensor VCC  -> its rated supply (many HC-SR04-style modules use 5 V)
  Sensor GND  -> micro:bit GND; connect supply GND to this same ground
  Sensor TRIG -> micro:bit P0
  Sensor ECHO -> micro:bit P1 THROUGH a voltage divider or level shifter

Do not connect a 5 V ECHO output directly to a micro:bit GPIO pin. For a
5 V echo, a divider such as 1 kΩ from ECHO to P1 and 2 kΩ from P1 to GND
reduces the signal to about 3.3 V.
"""

from microbit import *

TRIG = pin0
ECHO = pin1


def measure_distance_cm():
    """Return distance in centimeters, or None when no echo is received."""
    TRIG.write_digital(0)
    sleep(2)
    TRIG.write_digital(1)
    # The 1 ms trigger pulse is longer than the sensor's usual 10 us minimum.
    sleep(1)
    TRIG.write_digital(0)

    # Measure the echo's HIGH pulse in microseconds; timeout avoids hanging.
    pulse_us = ECHO.get_pulse_us(1, timeout=30000)
    if pulse_us < 0:
        return None

    # HC-SR04-style sensors take about 58 us for sound to travel 1 cm and back.
    return pulse_us / 58.0


while True:
    distance = measure_distance_cm()

    if distance is None:
        display.show(Image.NO)
        print("No echo")
    else:
        print("{:.1f} cm".format(distance))
        if distance < 10:
            display.show(Image.SAD)
        else:
            display.show(Image.HAPPY)

    sleep(200)
