import argparse
import sys
import os
from plotter3d import DataPlotter


def main(path):
    print("Using these settings:", path)

    plotter = DataPlotter()

    with open(path, "r") as reader:
        for line in reader.readlines():

            data_values = line.split(",")
            if len(data_values) == 3:
                imu_pitch = float(data_values[0])
                imu_roll = float(data_values[1])
                distance = float(data_values[2])

            plotter.add_data_point(imu_pitch, imu_roll, distance)

    print("Data received")
    plotter.plot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="My receiver")
    parser.add_argument("path", type=str, help="define path to file")

    args = parser.parse_args()
    try:
        main(args.path)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
