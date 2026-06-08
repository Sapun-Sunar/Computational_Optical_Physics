# Advanced Optical & Plasma Spectroscopy Analysis Suite

This repository contains a high-performance, Python-based data processing pipeline designed for advanced optical physics and spectroscopy. It features two primary analytical engines: 
1. **Quantum Interference Analysis (Fabry-Pérot)**
2. **Multi-Spectral Emission Analysis (LIBS)**

The objective of this suite is to transform raw experimental sensor data—ranging from 2D interference matrices to noisy multi-file 1D spectra—into mathematically pristine, baseline-corrected, and physically quantifiable measurements.


=========================================================================


## 📁 Repository Structure

Optical-Spectroscopy-Suite

    README.md
    Fabry_Perot_Analysis/
        Fabry_Perot_Extraction.ipynb
        sip_decoder.py
  	    center.py
        Lab_Data
    LIBS_Spectral_Analysis/
        main.ipynb
        specline.csv (NIST Reference Database)
        Datas/
            data1.csv
            data2.csv
            data3.csv


=======================================================================

🔬 Engine 1: Fabry-Perot Quantum Interference.
Directory: /Fabry_Perot_Analysis

This module extracts the Free Spectral Range (FSR) and physical absorption data from 2D Fabry-Pérot interferometer captures. It converts rigid, flawed digital pixels into a mathematically continuous quantum profile.

Core Mathematical Features:

1) Inverse Mapping (Ray Casting): Calculates exact Cartesian-to-Polar geometry for every pixel simultaneously to eliminate spatial sampling gaps.

2) Polar Wedge Masking: Isolates specific angular slices of the interference rings to bypass asymmetrical sensor noise.

3) Sub-Pixel Interpolation (Fractional Binning): Annihilates spatial aliasing (quantization error) by splitting photon intensity across fractional decimal radii.

4) Azimuthal Integration: Collapses the 2D matrix into a 1D intensity wave.

5) Inverted Peak Hunting: Utilizes Savitzky-Golay filtering and inverted topographical algorithms to lock onto dark atomic absorption lines rather than emission peaks.

=======================================================================

Engine 2: Laser-Induced Breakdown Spectroscopy (LIBS)
Directory: /LIBS_Spectral_Analysis

This pipeline processes raw emission spectra obtained from LIBS. It isolates sharp atomic emission lines superimposed on a large, slowly-varying plasma continuum, matching the isolated peaks to known atomic elements.

Workflow & Methodology:

1) Data Ingestion & Interpolation: Loads multiple raw spectra (wavelength vs. intensity) and maps them onto a unified master wavelength axis using NumPy vectorization.

2) Signal-to-Noise Enhancement: Stacks and averages all interpolated spectra to suppress random detector shot noise.

3) High-Frequency Smoothing: Applies a Savitzky–Golay filter (51-point window, 3rd-order polynomial) to iron out thermal noise without distorting peak geometries.

4) Plasma Continuum Removal (Baseline Correction): Deploys a broad median filter to estimate the underlying thermal plasma continuum, subtracting it to isolate true atomic emission peaks.

5) Elemental Identification: Cross-references detected peaks against a customizable NIST-style emission line database (specline.csv) within a strictly defined nanometer tolerance (Default: 0.3nm).


=======================================================================


##  Dependencies & Installation

  This suite is entirely vectorized for rapid computational execution and relies on the Jupyter environment for interactive data visualization. Ensure the following scientific libraries are installed:

```bash
pip install numpy pandas matplotlib scipy jupyter
```

=======================================================================



## Execution Guide
Because these analytical engines are built as Jupyter Notebooks (.ipynb), they are designed for interactive, cell-by-cell execution rather than background terminal processing. You can copy paste the cells in a .py file and run python3 ____.py if you prefer it.

  Step 1: Launch the Environment
  Open your terminal, navigate to the main Optical-Spectroscopy-Suite repository folder, and start the Jupyter server:

  Bash
  jupyter notebook



  Step 2: Run the Fabry-Pérot Analysis

  In the Jupyter browser, navigate into the Fabry_Perot_Analysis/ folder.

  Open the cadmium_absorption.ipynb notebook.

  Ensure your .sip file is in the same folder.

  Run the cells sequentially (Shift + Enter) to process the matrix and render the FSR graphs.



  Step 3: Run the LIBS Analysis

  In the Jupyter browser, navigate into the LIBS_Spectral_Analysis/ folder.

  Open the main.ipynb notebook.

  Ensure all your .csv spectral files are placed inside the Datas/ subfolder.

  Run the cells sequentially (Shift + Enter) to process the baseline corrections and output the elemental identification.





Developed for academic research, plasma diagnostics, and advanced physics applications.
