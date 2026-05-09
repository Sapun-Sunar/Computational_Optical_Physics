import sif_parser
import numpy as np

def decoded_matrix(file_path):
    raw_data, info = sif_parser.np_open(file_path)
    image_matrix = np.squeeze(raw_data)
    return image_matrix