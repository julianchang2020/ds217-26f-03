"""Assignment 03: summarize a telemetry ward's systolic readings.

Run from the assignment directory with the project environment active:

    python3 analysis.py
"""

import numpy as np


def load_readings(filename):
    """Return (patient_ids, monitors, hour_columns, readings) from the supplied CSV.

    readings is a 2D array of integers: one row per patient, one column per
    monitored hour, in the order the header lists them.
    """
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    header = lines[0].strip().split(",")
    rows = [line.strip().split(",") for line in lines[1:] if line.strip()]

    patient_ids = np.array([row[0] for row in rows])
    monitors = np.array([row[1] for row in rows])
    hour_columns = np.array(header[2:])
    readings = np.array([row[2:] for row in rows]).astype(int)
    return patient_ids, monitors, hour_columns, readings


def main():
    patient_ids, monitors, hour_columns, readings = load_readings("data/bp_readings.csv")
    print(f"Loaded {readings.shape[0]} patients x {readings.shape[1]} hours")

    # TODO: answer each question in the README's summary table with NumPy.
    # TODO: write one "key: value" line per answer to output/vitals_summary.txt.
    output_path = "output/vitals_summary.txt"

    with open(output_path, "w") as file:
        file.write(f"patients: {len(patient_ids)}\n")
        file.write(f"readings: {len(readings)*len(hour_columns)}\n")
        file.write(f"mean_sbp: {readings.mean()} mmHg\n")
        file.write(f"sd_sbp: {readings.std()} mmHg\n")
        file.write(f"min_sbp: {readings.min():.0f} mmHg\n")
        file.write(f"max_sbp: {readings.max():.0f} mmHg\n")
        file.write(f"stage2_patients: {len(patient_ids[(np.mean(readings, axis = 1)) >= 140])}\n")
        file.write(f"highest_patient: {patient_ids[np.argmax(np.mean(readings, axis = 1))]}\n")
        file.write(f"highest_patient_mean: {np.max(np.mean(readings, axis = 1))} mmHg\n")
        file.write(f"peak_hour_column: {hour_columns[np.argmax(np.mean(readings, axis = 0))]}\n")
        file.write(f"peak_hour_mean: {np.max(np.mean(readings, axis = 0))} mmHg\n")

        monitors_2 = np.array(monitors)
        readings_2 = np.array(np.mean(readings, axis = 1))
        arr = []
        x = sorted(set(monitors_2))
        for monitor in x:
            i = (monitors_2 == monitor)
            average = readings_2[i].mean()
            arr.append(average)
        highest_monitor = x[np.array(arr).argmax()]
        file.write(f"high_monitor: {highest_monitor}\n")

        in_highest = (monitors_2 == highest_monitor)
        others = ~in_highest
        others_average = readings_2[others].mean()
        highest = np.max(arr)
        file.write(f"monitor_offset: {highest - others_average} mmHg\n")
        file.write(f"stage2_other_monitors: {(readings_2[others] >= 140).sum()}")


if __name__ == "__main__":
    main()
