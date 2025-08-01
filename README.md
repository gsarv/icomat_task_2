
Signal Analyzer is a Python desktop application for quick, interactive visualization and statistical analysis of signals stored in CSV files.

## Features

-  Load CSV files with **multiple signals** (each column = one signal, first column should be time)
-  Interactive GUI:
  - Time domain plot
  - Frequency domain (FFT, PSD) plot
  - Descriptive statistics view
-  Switch between signals via dropdown
-  FFT & PSD calculation using `scipy`
-  Matplotlib toolbar: pan, zoom, save plots
-  Tabbed interface + clean modern theme

##  Requirements

- Python 3.8+
- `numpy`
- `scipy`
- `matplotlib`
- `tkinter` is included with most Python installations.

## Menu

- **File → Load Signals** – open CSV and load all signals
- **Tools → Analyze Signal** – compute statistics & FFT, PSD for selected signal
- **Tools → Identify Spikes** – identifies spikes in the selected signal
- **Tools → Identify Oscillations** – identifies areas with oscillations in the selected signal (needs further development and testing)
- **Tools → Identify Stallss** – identifies areas with almost zero time derivative
- **Tools → Filter Signal** – remove the noise of the signal
- **Help → About** – show app info
- **Help → Domumentation** – brief instructions

## Tabs

| Tab              | What it shows                                                     |
| ---------------- | ----------------------------------------------------------------- |
| Time Domain      | Line plot of the raw selected signal                              |
| FFT              | Fast Fourier Transform                       |
| PSD              | Power Spectral Density (PSD) using real FFT                       |
| Statistics       | Text summary: mean, variance, median, RMS, energy, min/max, range |

## Signal Selector

A dropdown (combobox) to choose which signal (column) to analyze & plot.

##  How It Works

1. Load a CSV file (columns = separate signals).
2. Select the signal you want to analyze.
3. Plot updates immediately in Time Domain.
4. Click **Analyze Signal**:
   - Shows statistics in the Statistics tab.
   - Plots frequency domain (FFT, PSD).

##  Analysis Details

- **Descriptive stats**: mean, variance, standard deviation, median, RMS, energy, min/max, range
- **Frequency domain**: uses `scipy.fft.rfft` for real FFT
- **PSD**: calculated as magnitude squared of FFT divided by sample count and sampling rate

##  Code Overview of app_gyi.py

| Method                   | Purpose                                   |
| ------------------------ | ----------------------------------------- |
| `create_menu`            | Builds the top menu bar                   |
| `create_tabs`            | Sets up tabs & Matplotlib plots           |
| `create_signal_selector` | Adds combobox to choose signal            |
| `load_signals`           | Loads CSV, parses signals                 |
| `plot_time`              | Draws time domain plot                    |
| `analyze_signal`         | Computes stats & frequency plot           |
| `on_signal_selected`     | Updates plot when user picks a new signal |


##  Example

Run in a terminal the following command "python app_gui.py"

Then:

1. Go to **File → Load Signals** and choose your CSV.
2. Pick a signal in the dropdown.
3. Go to **Tools → Analyze Signal**.
4. View plots and stats in the tabs.

## This text file was generated by AI and modified accordingly.


