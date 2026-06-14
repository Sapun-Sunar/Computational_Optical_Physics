# Advanced Optical & Plasma Spectroscopy Analysis Suite

This repository contains a high-performance, classical data processing pipeline designed for advanced optical physics and spectroscopy. It features two primary analytical engines: 
1. **Quantum Interference Analysis (Fabry-Perot Sub-Pixel Extractor)**
2. **Multi-Spectral Emission Analysis (LIBS)**

The objective of this suite is to transform raw experimental sensor data—ranging from severely degraded, astigmatic 2D interference matrices to noisy multi-file 1D spectra—into mathematically pristine, baseline-corrected, and physically quantifiable measurements.

---

## 📁 Repository Structure

```text
Optical-Spectroscopy-Suite/
├── README.md
├── Fabry_Perot_Analysis/
│   ├── main.py                 # Multi-Core Grid Search & Optimizer
│   ├── center.py               # Targeting HUD & JSON Memory Cache
│   ├── sip_decoder.py          # Proprietary .sif sensor decoder
│   ├── calibration_cache.json  # Autonomous parameter retention
│   └── Lab_Data/
└── LIBS_Spectral_Analysis/
    ├── main.ipynb
    ├── specline.csv            # NIST Reference Database
    └── Datas/

