# Fabry-Perot Quantum Interference (The Sub-Pixel Extractor)

**Directory:** `/Fabry_Perot_Analysis`

This module is a highly parallelized, classical targeting engine designed to extract absolute Full Width at Half Maximum (FWHM) values from degraded 2D Fabry-Pérot interferometer captures. It bypasses human visual error by deploying an autonomous grid search to isolate the true optical axis.

## Core Mathematical Architecture

* **Autonomous Multi-Core Grid Search:** Shatters the Python Global Interpreter Lock (GIL) via `concurrent.futures`, deploying parallel sub-pixel sweeps across multiple CPU cores to mathematically hunt for the deepest absorption void.

* **Fractional Photon Splitting (Sub-Pixel Binning):** Annihilates spatial aliasing and quantization error by splitting integer pixel intensities across fractional decimal radii.

* **Simultaneous Slanted Baseline Subtraction:** Upgrades the standard Levenberg-Marquardt optimizer (`scipy.optimize.curve_fit`) to fit a customized Slanted Lorentzian model. It simultaneously calculates the slope of the thermal plasma continuum and the depth of the quantum shadow, mathematically flattening asymmetrical hardware distortion.

* **Boolean Pincer Masking:** Isolates precise angular slices of the interference rings (Sector Alpha & Bravo) to bypass elliptical astigmatism caused by misaligned interferometer plates.

* **JSON State Retention:** `center.py` acts as a tactical visual HUD, saving bounded box parameters and sector shields into a local cache to allow rapid, headless re-execution of the optimizer.

---

## Dependencies & Installation

This suite relies on multiprocessing for the Fabry-Pérot engine and is entirely vectorized for rapid computational execution.



```bash
pip install numpy torch matplotlib scipy sip_parser
```

---

## Execution Guide
### Terminal Execution
The Fabry-Pérot suite is designed for high-performance terminal execution.

1) Open your terminal and navigate to the directory:
cd Fabry_Perot_Analysis

2) Execute the main pipeline:
```Bash
   python3 main.py
   ```
* The engine will automatically call center.py to trigger the Visual HUD.

* Define your bounding box and sector shields.

*  Close the window to pass the telemetry back to the terminal.

* The multi-core sub-pixel sweep will ignite. Output will display the top 3 extracted FWHM profiles mathematically constrained to the slanted continuum.