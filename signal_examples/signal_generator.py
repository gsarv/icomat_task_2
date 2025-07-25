import numpy as np
import csv

def generate_signal(num_points=600, seed=0):
    np.random.seed(seed)
    time = np.arange(num_points)
    
    # Base signals
    signal_1 = 3.0 + 0.8 * np.sin(0.02 * time)  # baseline 1
    signal_2 = 234 + 4.5 * np.cos(0.01 * time)  # baseline 2
    
    # Add small noise
    noise_1 = np.random.normal(0, 0.03, num_points)
    noise_2 = np.random.normal(0, 1.5, num_points)
    
    # Define stall region
    stall_start, stall_end = 150, 280
    signal_1[stall_start:stall_end] = 2.0
    signal_2[stall_start:stall_end] = 100
    noise_1[stall_start:stall_end] = 0
    noise_2[stall_start:stall_end] = 0
    
    # Oscillation region with larger amplitude
    osc_start, osc_end = 350, 420
    osc_time = np.arange(osc_end - osc_start)
    signal_1[osc_start:osc_end] += 0.8 * np.sin(0.3 * osc_time)
    signal_2[osc_start:osc_end] += 3 * np.cos(0.3 * osc_time)
    
    # Spikes at fixed points (excluding stall and oscillation)
    spikes_indices = [50, 130, 500]
    signal_1[spikes_indices] += [1.5, -1.2, 2.0]
    signal_2[spikes_indices] += [15, -10, 20]
    
    # Combine signals + noise (except stall region)
    signal_1 += noise_1
    signal_2 += noise_2
    
    # Prepare rows for CSV (list of lists)
    rows = []
    for t, c, v in zip(time, signal_1, signal_2):
        rows.append([t, c, v])
    
    return rows

# Write CSV without pandas
header = ['time', 'Signal_1', 'Signal_2']

data_rows = generate_signal(seed=5)
filename = f'test_signals_2.csv'
    
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data_rows)


    
print(f"Saved {filename}")
