import sif_parser
import numpy as np
import matplotlib.pyplot as plt

# Sip decoder (need to pip install sip_parser).
def decoded_matrix(file_path):
    raw_data, info = sif_parser.np_open(file_path)
    image_matrix = np.squeeze(raw_data)
    return image_matrix

if __name__ == "__main__":
    plt.figure(figsize=(8,6))
    img = decoded_matrix("/Users/sapunsunar/Documents/CODES/Lab_Data/absorption line 1 march 13.sif")
    plt.imshow(img, cmap="inferno", origin='lower')
    plt.tight_layout()
    plt.show()