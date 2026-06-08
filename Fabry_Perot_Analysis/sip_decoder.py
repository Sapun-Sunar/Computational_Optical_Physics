import sif_parser
import numpy as np
import matplotlib.pyplot as plt

def decoded_matrix(file_path):
    raw_data, info = sif_parser.np_open(file_path)
    image_matrix = np.squeeze(raw_data)
    return image_matrix

if __name__ == "__main__":
    plt.figure(figsize=(8,6))
    img = decoded_matrix("/Users/sapunsunar/Documents/GIT_Projects/Spectrometer_Analysis/Fabry_Perot_Analysis/Lab_Data/cadmium aborption line sep 22.sif")
    plt.imshow(img, cmap="inferno", origin='lower')
    plt.tight_layout()
    plt.show()