import tkinter as tk
import numpy as np
import matplotlib
import common_lib

from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from data import data
from signal_process import signal_process

##########################################

matplotlib.use('TkAgg')

##########################################

class SignalAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Analyzer")
        self.root.geometry("900x550")
        
        # Default data
        self.results              = None
        self.current_signal_index = 0
        self.filtered_count       = 0

        # Initialize GUI
        self.create_menu()
        self.create_tabs()
        self.create_signal_selector()

        return

    ##########################################
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load File", command=self.load_signal)
        menubar.add_cascade(label="File", menu=file_menu)
        
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Analyze Signal", command=self.analyze_signal)
        tools_menu.add_command(label="Identify Spikes", command=self.detect_spikes)
        tools_menu.add_command(label="Identify Stalls", command=self.detect_stalls)
        tools_menu.add_command(label="Identify Oscillations", command=self.detect_oscillations)
        tools_menu.add_command(label="Filter Signal", command=self.filtered_data)
        tools_menu.add_command(label="Filter Signal, Keep Spikes", command=self.filtered_data_keep_spikes)
        tools_menu.add_command(label="Restore Signal", command=self.restore_data)
        tools_menu.add_command(label="Integrate Signal", command=self.integration)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        return

    ##########################################
        
    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)
        self.tab_time = ttk.Frame(tab_control)
        self.tab_fft = ttk.Frame(tab_control)
        self.tab_psd = ttk.Frame(tab_control)
        self.tab_stats = ttk.Frame(tab_control)
        
        tab_control.add(self.tab_time, text='Time Domain')
        tab_control.add(self.tab_fft, text='FFT')
        tab_control.add(self.tab_psd, text='PSD')
        tab_control.add(self.tab_stats, text='Statistics')
        tab_control.pack(expand=1, fill='both')
        
        # Time Domain tab
        self.fig_time = Figure(figsize=(8,4), dpi=100)
        self.ax_time = self.fig_time.add_subplot(111)
        self.canvas_time = FigureCanvasTkAgg(self.fig_time, master=self.tab_time)
        self.canvas_time.draw()
        self.canvas_time.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar_time = NavigationToolbar2Tk(self.canvas_time, self.tab_time)
        toolbar_time.update()
        toolbar_time.pack(side=tk.BOTTOM, fill=tk.X)
        
        # FFT
        self.fig_fft = Figure(figsize=(8,4), dpi=100)
        self.ax_fft = self.fig_fft.add_subplot(111)
        self.canvas_fft = FigureCanvasTkAgg(self.fig_fft, master=self.tab_fft)
        self.canvas_fft.draw()
        self.canvas_fft.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar_fft = NavigationToolbar2Tk(self.canvas_fft, self.tab_fft)
        toolbar_fft.update()
        toolbar_fft.pack(side=tk.BOTTOM, fill=tk.X)

        # PSD
        self.fig_psd = Figure(figsize=(8,4), dpi=100)
        self.ax_psd = self.fig_psd.add_subplot(111)
        self.canvas_psd = FigureCanvasTkAgg(self.fig_psd, master=self.tab_psd)
        self.canvas_psd.draw()
        self.canvas_psd.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar_psd = NavigationToolbar2Tk(self.canvas_psd, self.tab_psd)
        toolbar_psd.update()
        toolbar_psd.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Stats tab text
        self.stats_text = tk.Text(self.tab_stats, font=("Courier", 16), wrap='word')
        self.stats_text.pack(expand=1, fill='both', padx=10, pady=10)

        return

    ##########################################
        
    def create_signal_selector(self):
        
        frame = ttk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        label = ttk.Label(frame, text="Select Signal:")
        label.pack(side=tk.LEFT, padx=5)

        self.signal_combobox = ttk.Combobox(frame, state='readonly')
        self.signal_combobox.pack(side=tk.LEFT, padx=5)
        self.signal_combobox.bind("<<ComboboxSelected>>", self.on_signal_selected)

        return

    ##########################################
        
    def load_signal(self):
        
        filepath = filedialog.askopenfilename(
            title="Open Data File",
            filetypes=(("CSV / TXT files", "*.csv *.txt"), ("All files", "*.*")))

        self.filtered_count = 1
        
        if filepath:
            try:
                values         = common_lib.load_csv(filepath)
                self.results   = data(values)
                vectors        = self.results.vectors
                signal_names   = []
                
                for i in range(1, self.results.n_vectors):
                    signal_names.append(self.results.vectors[i].header)
                
                self.signal_combobox['values'] = signal_names
                self.signal_combobox.current(0)
                self.current_signal_index = 1
                messagebox.showinfo("Loaded", "Loaded {} signals, with time step {}".format(self.results.n_vectors - 1, self.results.time_step))

                i = self.current_signal_index
                self.plot_graph(self.ax_time, self.results.vectors[0].current, self.results.vectors[i].current, self.results.vectors[0].header, "Amplitude")
            except Exception as e:
                messagebox.showerror("Error", "Failed to load: {}".format(e))

        return

    ##########################################
                
    def on_signal_selected(self, event):
        
        self.current_signal_index = self.signal_combobox.current() + 1
        i                         = self.current_signal_index
        self.filtered_count       = 0

        # Update Time Domain plot
        self.plot_graph(self.ax_time, self.results.vectors[0].current, self.results.vectors[i].current,  self.results.vectors[0].header, "Amplitude")
        
        return

    ##########################################
        
    def analyze_signal(self):

        i = self.current_signal_index
        
        self.warn_load_signal()

        # Stats

        analysis = self.results.vectors[i].statistical().analysis()

        stats_msg = (
            "Statistical Results for {}\n\n".format(self.results.vectors[i].header)  +              
            "Samples: {}\n".format(self.results.vectors[i].n)                        +
            "Mean: {}\n".format(analysis["mean_value"])                              +
            "Variance: {}\n".format(analysis["variance"])                            +
            "Median: {}\n".format(analysis["median"])                                +
            "Standard Deviation: {}\n".format(analysis["std_dev"])                   +
            "RMS: {}\n".format(analysis["rms"])                                      +
            "Energy: {}\n".format(analysis["energy"])                                +
            "Range: {}\n".format(analysis["range"])                                  +
            "Min: {}    Max: {}".format(analysis["min"], analysis["max"])
            )
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert(tk.END, stats_msg)
        
        # Update Time Domain plot
        self.ax_time.axhline(analysis["mean_value"], color='g', linestyle='--', label='Mean')
        self.ax_time.legend()
        self.canvas_time.draw()

        # FFT & PSD
        sig_proc       = signal_process(self.results.vectors[i], self.results.time_step)
        psd_results    = sig_proc.psd()
        freq_results   = sig_proc.frequencies()
        fou_results    = sig_proc.amplitude()

        # Update FFT plot
        self.plot_graph_freq(self.ax_fft, freq_results, fou_results,  "Frequency 1 / time_step", "Amplitude")
        self.canvas_fft.draw()

        # Update PSD plot
        self.plot_graph_freq(self.ax_psd, psd_results[0], psd_results[1],  "Frequency 1 / time_step", "PSD (Power * time_step)")
        self.canvas_psd.draw()

        return

    ##########################################
        
    def detect_spikes(self):

        self.warn_load_signal()

        i = self.current_signal_index
        x_values = []
        y_values = []
        
        spikes = self.results.vectors[i].detect_spikes()

        for spike in spikes:
            x_values.append(spike[0])
            y_values.append(spike[1])

        if len(spikes) != 0:
            # Update Time Domain plot
            self.ax_time.plot(x_values, y_values, linestyle='None', marker='o', color='r', label='Spikes')
            self.ax_time.legend()
            self.canvas_time.draw()
        else:
            messagebox.showwarning("Spikes", "No spikes detected")

        return

    ##########################################
        
    def detect_stalls(self):

        self.warn_load_signal()

        i = self.current_signal_index
        x_values = []
        y_values = []
        
        stalls = self.results.vectors[i].detect_stalls()

        for j,stall in enumerate(stalls):
            x_values = [stall[0], stall[1] - 1]
            y_values = [self.results.vectors[i].current[stall[0]], self.results.vectors[i].current[stall[1] - 1]]

            # Update Time Domain plot
            self.ax_time.plot(x_values, y_values, marker='o', color='g', label='Stall {}'.format(j + 1))
            self.ax_time.legend()
            self.canvas_time.draw()
                
        if len(stalls) == 0:
            messagebox.showwarning("Stalls", "No stalls detected")

        return

    ##########################################
        
    def detect_oscillations(self):

        self.warn_load_signal()

        i = self.current_signal_index
        window_ratios = [0.05, 0.1]
        x_values      = []
        y_values      = []

        for ratio in window_ratios:
            oscis = self.results.vectors[i].detect_oscillations(ratio)
            if len(oscis) != 0:
                break
            
        if len(oscis) != 0:
            
            x_values = [oscis[0][0], oscis[-1][1]]
            y_values = [self.results.vectors[i].current[oscis[0][0]], self.results.vectors[i].current[oscis[-1][1]]]

            # Update Time Domain plot
            self.ax_time.plot(x_values, y_values, color='red', label='Oscillations')
            self.ax_time.legend()
            self.canvas_time.draw()
            
        else:
            messagebox.showwarning("Oscillations", "No oscillations detected")

        return
    
     ##########################################
        
    def restore_data(self):

        self.warn_load_signal()

        i = self.current_signal_index

        self.results.vectors[i].current = self.results.vectors[i].original_data

        # Update Time Domain plot
        self.plot_graph(self.ax_time, self.results.vectors[0].current, self.results.vectors[i].current, self.results.vectors[0].header, "Amplitude")

        return

    ##########################################
        
    def integration(self):

        self.warn_load_signal()

        i = self.current_signal_index

        sig_proc       = signal_process(self.results.vectors[i], self.results.time_step)

        self.results.vectors[i].current = sig_proc.integral()

        # Update Time Domain plot
        self.plot_graph(self.ax_time, self.results.vectors[0].current, self.results.vectors[i].current, self.results.vectors[0].header + " Integral", "Amplitude")

        return

    ##########################################
        
    def filtered_data(self):

        self.warn_load_signal()

        i = self.current_signal_index
        
        filtered = self.results.vectors[i].filtered_data(self.filtered_count)
        self.results.vectors[i].current = filtered

        self.filtered_count += 1

        # Update Time Domain plot
        self.plot_graph(self.ax_time, self.results.vectors[0].current, filtered, self.results.vectors[0].header, "Amplitude")

        return

    ##########################################
        
    def filtered_data_keep_spikes(self):

        self.warn_load_signal()

        i = self.current_signal_index

        spikes = self.results.vectors[i].detect_spikes()
        
        filtered = self.results.vectors[i].filtered_data(self.filtered_count)
        filtered = self.results.vectors[i].restore_spikes(spikes, filtered)
        
        self.results.vectors[i].current = filtered
        self.filtered_count += 1

        # Update Time Domain plot
        self.plot_graph(self.ax_time, self.results.vectors[0].current, filtered, self.results.vectors[0].header, "Amplitude")

        return

    ##########################################
        
    def plot_graph(self, graph, x_values, y_values, xlabel, ylabel):

        i = self.current_signal_index
        
        if data is None:
            return
        graph.cla()
        graph.plot(x_values, y_values, color='b')
        graph.set_title(self.results.vectors[i].header)
        graph.set_xlabel(xlabel)
        graph.set_ylabel(ylabel)
        graph.grid(True)
        self.canvas_time.draw()

        return

    ##########################################
        
    def plot_graph_freq(self, graph, x_values, y_values, xlabel, ylabel):

        i = self.current_signal_index

        if (x_values is None) or (y_values is None):
            return
        
        graph.cla()
        graph.semilogy(x_values, y_values, color='b')
        graph.set_title(self.results.vectors[i].header)
        graph.set_xlabel(xlabel)
        graph.set_ylabel(ylabel)
        graph.grid(True)
        self.canvas_time.draw()

        return

    ##########################################

    def show_about(self):
        
        messagebox.showinfo("About", "Signal Analyzer\nCreated by Gregory\nfor iCOMAT selection process")

        return

    ##########################################

    def warn_load_signal(self):
        
        if self.results is None:
            messagebox.showwarning("Load", "Please load a signal.")
            return

        return

    ##########################################
        
    def show_documentation(self):
        
        doc_text = (
            "1. Load CSV files with File → Load Signals.\n"
            "2. Select a signal from the dropdown.\n"
            "3. Use Tools → Analyze Signal to compute stats and FFT.\n"
            "4. View plots and statistics in the tabs.\n\n"
            "For more help, see the README.md."
        )
        messagebox.showinfo("Documentation", doc_text)

        return

    ##########################################
    
if __name__ == '__main__':
    
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')
    app = SignalAnalyzer(root)
    root.mainloop()
