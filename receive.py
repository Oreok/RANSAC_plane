# Niclas Ortner, Moritz Kobriger, Jakob Koller
import argparse
import serial
import sys
import os
import math
from plotter3d import DataPlotter


def calculate_pitch_roll(x_value, y_value, z_value):
    pitch = math.atan2(y_value, math.sqrt(x_value**2 + z_value**2))
    pitch_deg = math.degrees(pitch)
    print("Pitch: " + str(pitch_deg))

    roll = math.atan2(x_value, math.sqrt(y_value**2 + z_value**2))
    roll_deg = math.degrees(roll)
    print("Roll: " + str(roll_deg))

    return pitch_deg, roll_deg


def correct_distance(roll_deg, pitch_deg, distance):
    pitch_rad = math.radians(pitch_deg)
    roll_rad = math.radians(roll_deg)

    corrected_distance = distance * math.cos(pitch_rad) * math.cos(roll_rad)
    return corrected_distance


def main(port, baud, amount, output=None):
    print("Using these settings:", port, baud, amount, output)
    print("Connecting...")

    plotter = DataPlotter()

    with serial.Serial(port, baud, timeout=1) as ser:
        for _ in range(amount):
            reading = ser.readline()
            decoded_output = reading.decode("utf-8")
            print(decoded_output)
            # Process the received data as needed
            data_values = decoded_output.split(',')
            if len(data_values) == 4:
                x_value = float(data_values[0])
                y_value = float(data_values[1])
                z_value = float(data_values[2])
                distance = float(data_values[3])

                imu_pitch, imu_roll = calculate_pitch_roll(x_value, y_value, z_value)

                corrected_distance = correct_distance(imu_roll, imu_pitch, distance)

                plotter.add_data_point(imu_pitch, imu_roll, corrected_distance)

    print("Data received")

    if output:
        with open(output, 'w') as file:
            for x, y, z in zip(plotter.pitch, plotter.roll, plotter.distance):
                file.write(f"{x},{y},{z}\n")
        print("Data saved to", output)

    # Plot the data
    plotter.plot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="My receiver")
    parser.add_argument("port", type=str, help="define port e.g. /dev/cu.usb-serial110")
    parser.add_argument("baud", type=int, help="define baudratee e.g. 19200")
    parser.add_argument("amount", type=int, help="define amout of datapoints e.g. 1000")
    parser.add_argument("output", type=str, help="define a file where the output should be safed")

    args = parser.parse_args()
    try:
        main(args.port, args.baud, args.amount, args.output)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
