import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('../../data/data.csv')

def filter(data):
    """Apply a simple moving average filter to the data."""
    window_size = 5
    return data.rolling(window=window_size).mean()

def plot_data_from_csv(data):
    # Extract time and sensor data
    time = data['timestamp_ms']

    # Create subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 16))

    # Plot accelerometer data
    ax1.plot(time, data['accel_x_g'], label='Accel X', color='r')
    ax1.plot(time, data['accel_y_g'], label='Accel Y', color='g')
    ax1.plot(time, data['accel_z_g'], label='Accel Z', color='b')
    ax1.set_title('Accelerometer Data')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Acceleration (g)')
    ax1.legend()
    ax1.grid()

    # Plot gyroscope data
    ax2.plot(time, data['gyro_x_dps'], label='Gyro X', color='r')
    ax2.plot(time, data['gyro_y_dps'], label='Gyro Y', color='g')
    ax2.plot(time, data['gyro_z_dps'], label='Gyro Z', color='b')
    ax2.set_title('Gyroscope Data')
    ax2.set_xlabel('Time (ms)')
    ax2.set_ylabel('Angular Velocity (°/s)')
    ax2.legend()
    ax2.grid()

    # Plot temperature data
    ax3.plot(time, data['temperature_c'], label='Temperature', color='m')
    ax3.set_title('Temperature Data')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Temperature (°C)')
    ax3.legend()
    ax3.grid()

    # Adjust layout to increase spacing between subplots/figures
    fig.subplots_adjust(hspace=0.5)
    fig.tight_layout(pad=2.5)

    # save plots to file
    fig.savefig('../../docs/results/raw/plots_raw.png')

data = filter(data)
plot_data_from_csv(data)