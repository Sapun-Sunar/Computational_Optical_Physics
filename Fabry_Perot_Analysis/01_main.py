# Importing necessary library and tools.
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
from scipy.optimize import curve_fit
import time
import concurrent.futures
import itertools


# 1. INGESTION
from center import test_matrix, execute_visual_calibration

def slanted_lorentzian(x, slope, intercept, amplitude, center, gamma):
    """The continuous physics of spectral absorption upon a slanted plasma continuum."""
    # The linear mountain (m*x + b)
    baseline = slope * x + intercept
    # The quantum shadow
    absorption = (amplitude / np.pi) * (gamma / ((x - center)**2 + gamma**2))
    return baseline - absorption


def worker_trajectory(args):
    """
    The isolated CPU worker. It receives a specific coordinate, 
    executes the math, and returns the result or None if it fails.
    """
    dx, dy, x_base, y_base, s1_min, s1_max, s2_min, s2_max, radius_max = args
    current_x = x_base + dx
    current_y = y_base + dy
    y_indices, x_indices = np.indices(test_matrix.shape)
    

    # KINEMATICS
    raw_angles = np.degrees(np.arctan2(y_indices - current_y, x_indices - current_x))
    angle_seg = np.mod(raw_angles, 360)
    radii = np.sqrt((x_indices - current_x)**2 + (y_indices - current_y)**2)

    mask_alpha = (angle_seg >= s1_min) & (angle_seg <= s1_max)
    mask_bravo = (angle_seg >= s2_min) & (angle_seg <= s2_max)
    master_mask = (mask_alpha | mask_bravo) & (radii <= radius_max)

    valid_radii = radii[master_mask]
    valid_intensities = test_matrix[master_mask]

    if len(valid_radii) == 0:
        return None


    # FRACTIONAL SPLITTING
    fractional_part = valid_radii % 1.0
    weight_upper = fractional_part
    weight_lower = 1.0 - fractional_part

    bin_lower = np.floor(valid_radii).astype(int)
    bin_upper = bin_lower + 1
    max_bin = np.max(bin_upper) + 1

    radial_intensity = np.bincount(bin_lower, weights=valid_intensities * weight_lower, minlength=max_bin) + \
                       np.bincount(bin_upper, weights=valid_intensities * weight_upper, minlength=max_bin)
    pixel_count = np.bincount(bin_lower, weights=weight_lower, minlength=max_bin) + \
                  np.bincount(bin_upper, weights=weight_upper, minlength=max_bin)

    pixel_count[pixel_count == 0] = 1 
    spectrum_1d = radial_intensity / pixel_count


   # SMOOTHING AND DETECTION OF PEAKS
    smoothed_spectrum = savgol_filter(spectrum_1d, window_length=10, polyorder=3)
    search_start = len(smoothed_spectrum) // 2
    safe_end = len(smoothed_spectrum) - 10 
    search_area = -smoothed_spectrum[search_start:safe_end]

    # We must capture the 'properties' dictionary returned by find_peaks
    detected_valleys, properties = find_peaks(search_area, prominence=5, distance=25)
    

    if len(detected_valleys) > 0:
        valley_idx = detected_valleys[0] + search_start
        true_local_depth = properties['prominences'][0]
        
        return {
            'depth': true_local_depth,
            'x': current_x,
            'y': current_y,
            'valley_idx': valley_idx,
            'spectrum': spectrum_1d,
            'smoothed': smoothed_spectrum
        }
    return None



if __name__ == "__main__":
    print("\n--- INITIALIZATION ---")
    y_base, x_base, s1_min, s1_max, s2_min, s2_max, radius_max = execute_visual_calibration(test_matrix)


    # 2. PARALLEL SUB-PIXEL SWEEP
    step_size = 0.1
    search_radius = 4.0
    x_offsets = np.arange(-search_radius, search_radius + step_size, step_size)
    y_offsets = np.arange(-search_radius, search_radius + step_size, step_size)
    

    # Create the complete list of tasks
    tasks = [(dx, dy, x_base, y_base, s1_min, s1_max, s2_min, s2_max, radius_max) 
             for dx, dy in itertools.product(x_offsets, y_offsets)]
    
    total_iterations = len(tasks)
    print(f"\nEngaging Parallel Sub-Pixel Sweep...")
    print(f"Total Trajectories to Calculate: {total_iterations}")
    
    results_database = []
    start_time = time.time()
    

    # Ignite all CPU Cores
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Map the worker function to the tasks
        results = executor.map(worker_trajectory, tasks)
        
        # Filter out the failed trajectories (None values)
        for result in results:
            if result is not None:
                results_database.append(result)

    exec_time = time.time() - start_time
    print(f"\nSweep Complete. Time elapsed: {exec_time:.2f} seconds.")
    print(f"Total viable optical axes found: {len(results_database)}")



    # 3. TACTICAL ARBITRATION (TOP 3)
    if len(results_database) == 0:
        print("CRITICAL FAILURE: No absorption dips detected in any configuration.")
        exit()

    results_database.sort(key=lambda item: item['depth'], reverse=True)
    top_3 = results_database[:3]

    print("\nExecuting Sub-Pixel FWHM Extraction On Top 3 Candidates...")
    
    fig, axes = plt.subplots(1, 3, figsize=(24, 8))
    fig.suptitle("Apex Configuration: Top 3 Sub-Pixel Depth Maximizations", fontsize=20)


    for rank, (ax, data) in enumerate(zip(axes, top_3)):
        x_axis = np.arange(len(data['spectrum']))
        valley_idx = data['valley_idx']
        
        ax.plot(x_axis, data['spectrum'], color='gray', alpha=0.5, linewidth=1, label='Raw Data')
        ax.plot(x_axis, data['smoothed'], color='cyan', linewidth=1.5, label='Savitzky-Golay')
        ax.plot(valley_idx, data['smoothed'][valley_idx], "rx", markersize=10, markeredgewidth=2)
        

       # THE SLANTED CONTINUUM MODEL)
        window = 8 # Expanded sight so the math can "see" the slopes
        
        x_local = x_axis[valley_idx - window : valley_idx + window]
        y_local = data['spectrum'][valley_idx - window : valley_idx + window]
        

        # 1. Calculate the literal slope of the plasma mountain
        dx = x_local[-1] - x_local[0]
        dy = y_local[-1] - y_local[0]
        slope_guess = dy / dx if dx != 0 else 0
        intercept_guess = y_local[0] - slope_guess * x_local[0]
        

        # 2. Calculate what the baseline altitude should be at the exact center of the valley
        baseline_center_altitude = slope_guess * valley_idx + intercept_guess
        amplitude_guess = (baseline_center_altitude - np.min(y_local)) * np.pi
        
        # Initial Guesses: [Slope, Intercept, Amplitude, Center, Gamma]
        p0 = [slope_guess, intercept_guess, amplitude_guess, valley_idx, 2.0]
        
        # THE CAGE
        # Allow the slope/intercept to be anything, but clamp the center and the FWHM
        min_bounds = [-np.inf, -np.inf, 0, valley_idx - 2, 0.1]
        max_bounds = [np.inf, np.inf, np.inf, valley_idx + 2, 6.0] # Max FWHM of 12
        
        best_fwhm = None
        

        try:
            # Inject the slanted physics into the Levenberg-Marquardt engine
            popt, _ = curve_fit(slanted_lorentzian, x_local, y_local, p0=p0, bounds=(min_bounds, max_bounds), maxfev=2000)
            best_fwhm = 2 * abs(popt[4]) # Gamma is now the 5th parameter (index 4)
            
            x_continuous = np.linspace(min(x_local), max(x_local), 100)
            y_continuous = slanted_lorentzian(x_continuous, *popt)
            

            # VISUALIZATION
            # 1. Plot the Slanted Plasma Baseline (Red Dotted Line)
            baseline_line = popt[0] * x_continuous + popt[1]
            ax.plot(x_continuous, baseline_line, color='red', linestyle=':', linewidth=2, label='Plasma Continuum')
            
            # 2. Plot the Magenta Physics
            ax.plot(x_continuous, y_continuous, color='#FF00FF', linewidth=2.5, label='Slanted Lorentzian Fit')
            
            # 3. Plot the True Half-Maximum Width (Slanted to match the mountain)
            half_max_altitude = baseline_line - ((popt[2] / (np.pi * popt[4])) / 2)
            ax.plot(x_continuous, half_max_altitude, color='lime', linestyle='--', linewidth=2)
            
        except RuntimeError:
            pass


        if best_fwhm:
            title_color = 'lime' if rank == 0 else 'green'
            ax.set_title(f"Rank {rank+1} | X:{data['x']:.1f} Y:{data['y']:.1f}\nDepth: {data['depth']:.1f} | FWHM: {best_fwhm:.4f}", 
                         fontsize=14, color=title_color)
        else:
            ax.set_title(f"Rank {rank+1} | X:{data['x']:.1f} Y:{data['y']:.1f}\nOPTIMIZER FAILED", fontsize=14, color='red')
            
        ax.set_xlim(15, radius_max)
        ax.set_ylim(550, 850)
        ax.set_xlabel("Radius (Pixels)")
        ax.set_ylabel("Intensity")
        ax.grid(True, alpha=0.2)
        ax.legend(loc='lower right')


    plt.tight_layout(rect=[0, 0.03, 1, 0.92])
    plt.show()                