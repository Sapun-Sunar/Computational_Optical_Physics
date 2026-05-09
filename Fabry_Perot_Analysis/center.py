from scipy.ndimage import center_of_mass

def calculate_box_center(image_matrix, x_min, x_max, y_min, y_max):
    if (x_max-x_min) == (y_max-y_min):
        # 1. Slice the matrix like a scalpel
        a,b = (x_max - x_min)/3, (y_max - y_min)/3
        x_max, x_min, y_max, y_min = int(x_max - a), int(x_min + a), int(y_max - b), int(y_min + b)
        isolated_box = image_matrix[y_min:y_max, x_min:x_max]
    
        # 2. Calculate the center of mass (the "center of light")
        local_y, local_x = center_of_mass(isolated_box)

        # 3. Coordinate Translation
        global_x = local_x + x_min
        global_y = local_y + y_min
    
        # Return Y first, then X (standard matrix notation)
        return global_y, global_x
    
    else:
        raise ValueError("The defined box is not square. Please ensure (x_max-x_min) equals (y_max-y_min).")    