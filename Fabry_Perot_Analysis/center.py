# Importing Necessary Libraries and Tools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import os
from sip_decoder import decoded_matrix

# The Matrix Data We Are Gonna Work On
test_matrix = decoded_matrix("/Users/sapunsunar/Documents/GIT_Projects/Computational_Optical_Physics/Fabry_Perot_Analysis/Lab_Data/FHWM 8.6456 absorption line 2 march 13.sif")
CACHE_FILE = "calibration_cache.json"


# PHASE 1: DEFINING THE CENTER
# The boundary of the first ring is guessed, tolerance of 4 pixels along both x and y are valid.
def calculate_box_center(x_min, x_max, y_min, y_max):
    # Retaining a 1-pixel tolerance for input
    if abs((x_max - x_min) - (y_max - y_min)) > 1: 
        raise ValueError(f"The defined box is not square. Width: {x_max-x_min}, Height: {y_max-y_min}")

    center_x = (x_min + x_max) / 2.0
    center_y = (y_min + y_max) / 2.0
    return center_y, center_x

# Getting previous parameters if any and storing new parameters
def get_parameter(param_name, prompt_text, cast_type, cache, master_override):
    """Handles the logic of retrieving either a cached parameter or a fresh user input."""
    cached_val = cache.get(param_name)
    
    if master_override and cached_val is not None:
        return cast_type(cached_val)
        
    if cached_val is not None:
        choice = input(f"Use previous {param_name} [{cached_val}]? (y/n): ").strip().lower()
        if choice == 'y':
            return cast_type(cached_val)
            
    while True:
        try:
            val = input(prompt_text)
            return cast_type(val)
        except ValueError:
            print(f"ERROR: {param_name} must be a valid {cast_type.__name__}. Try again.")


def execute_visual_calibration(image_matrix):
    vmin_val = np.percentile(image_matrix, 5)
    vmax_val = np.percentile(image_matrix, 99.5)

    # Load Memory Cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)

    while True:
        print("\n PHASE 1: RAW MATRIX SCAN")
        print("WARNING: Close the image window to proceed to the configuration terminal.")
        plt.figure(figsize=(8,6))
        plt.imshow(test_matrix, cmap="inferno", origin='lower')
        plt.colorbar()
        plt.tight_layout()
        plt.show()



        # PHASE 2: PARAMETER ACQUISITION 
        use_all = False
        if cache:
            master = input("\nMemory cache detected. Use ALL previous parameters? (y/n): ").strip().lower()
            if master == 'y':
                use_all = True

        try:
            print("\n Bounding Box Coordinates ")
            x_min = get_parameter('x_min', "Enter Bounding Box x_min: ", int, cache, use_all)
            x_max = get_parameter('x_max', "Enter Bounding Box x_max: ", int, cache, use_all)
            y_min = get_parameter('y_min', "Enter Bounding Box y_min: ", int, cache, use_all)
            y_max = get_parameter('y_max', "Enter Bounding Box y_max: ", int, cache, use_all)
            
            print("\n Sector Shields (Degrees) ")
            s1_min = get_parameter('s1_min', "Sector Alpha MIN angle: ", float, cache, use_all)
            s1_max = get_parameter('s1_max', "Sector Alpha MAX angle: ", float, cache, use_all)
            s2_min = get_parameter('s2_min', "Sector Bravo MIN angle: ", float, cache, use_all)
            s2_max = get_parameter('s2_max', "Sector Bravo MAX angle: ", float, cache, use_all)
            
            print("\n Sweep Boundaries ")
            radius_max = get_parameter('radius_max', "Maximum Search Radius: ", float, cache, use_all)
            
        except ValueError:
            print("ERROR: Invalid numerical input. Restarting calibration...")
            continue

        try:
            center_y, center_x = calculate_box_center(x_min, x_max, y_min, y_max)
        except ValueError as e:
            print(f"\nGEOMETRY ERROR: {e}")
            continue
        

        # PHASE 3: TERMINAL HUD VERIFICATION 
        print("\n Review the boundaries selected.")
        print("CLOSE the image window to confirm or reject in the terminal.")
        plt.figure(figsize=(8, 6))
        plt.imshow(image_matrix, origin='lower', cmap='inferno', vmin=vmin_val, vmax=vmax_val)
        
        # 1. Paint the Bounding Box
        width = x_max - x_min
        height = y_max - y_min
        rect = patches.Rectangle((x_min, y_min), width, height, 
                                 linewidth=1.5, edgecolor='cyan', facecolor='none', linestyle='--')
        plt.gca().add_patch(rect)
        
        # 2. Paint the Optical Axis
        plt.plot(center_x, center_y, 'w+', markersize=20, markeredgewidth=2, label='Optical Axis')
        
        # 3. Paint the Radial Parts
        wedge_alpha = patches.Wedge((center_x, center_y), radius_max, s1_min, s1_max, 
                                    fill=False, edgecolor='lime', linestyle='-', linewidth=2, label='Sector Alpha')
        plt.gca().add_patch(wedge_alpha)
        
        wedge_bravo = patches.Wedge((center_x, center_y), radius_max, s2_min, s2_max, 
                                    fill=False, edgecolor='magenta', linestyle='-', linewidth=2, label='Sector Bravo')
        plt.gca().add_patch(wedge_bravo)

        plt.text(x_min, y_min - 10, f"Center: ({center_x:.1f}, {center_y:.1f})", 
                 color='cyan', fontsize=12, fontweight='bold')
        
        plt.title("Phase 3: Axis Lock & Sector Shielding")
        plt.xlabel("X-Axis (Pixels)")
        plt.ylabel("Y-Axis (Pixels)")
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.show()



        # PHASE 4: THE ARBITRATION & MEMORY SAVE 
        choice = input(f"\nTarget acquired. Store these coordinates (y/n): ")
        if choice.lower() == 'y':
            print("Writing configuration to memory cache...")
            new_cache = {
                'x_min': x_min, 'x_max': x_max, 'y_min': y_min, 'y_max': y_max,
                's1_min': s1_min, 's1_max': s1_max, 's2_min': s2_min, 's2_max': s2_max,
                'radius_max': radius_max
            }
            with open(CACHE_FILE, 'w') as f:
                json.dump(new_cache, f, indent=4)

            print("Locking parameters into main pipeline...")

            # Return the exact payload of variables expected by main.py
            return center_y, center_x, s1_min, s1_max, s2_min, s2_max, radius_max
        else:
            print("Parameters rejected. Rebooting visual scan...")


if __name__ == "__main__":
    execute_visual_calibration(test_matrix)