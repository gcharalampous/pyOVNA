# pyOVNA

`pyOVNA` is a lightweight Python toolkit for processing and analyzing data from Optical Vector Network Analyzer (OVNA) measurements.

It supports:

- Loading and parsing custom `.OVNA4` binary files
- Signal processing (filtering, smoothing, etc.)
- Spectral fitting and propagation loss extraction
- Jupyter-based analysis with real-world examples

---

## 📦 Installation

Clone the repo and install locally:

```bash
git clone https://github.com/gcharalampous/pyOVNA.git
cd pyOVNA
pip install .
```
---

## 🧪 Requirements

- Python 3.7+
- numpy
- scipy
- pandas
- matplotlib

(Handled automatically during install)

---

## 📂 Project Structure

```
pyOVNA/
├── examples
│   ├── data
│   ├── propagation_loss.ipynb
│   ├── resonator_transmission_analysis.ipynb
│   └── transmission.ipynb
├── LICENSE
├── pyOVNA
│   ├── filters.py
│   ├── fitting.py
│   ├── __init__.py
│   ├── io.py
│   ├── processing.py
├── pyproject.toml
└── README.md
```

---

## 🚀 Usage Example

Inside a notebook:

```python
from pyOVNA.io import load_ovna
from pyOVNA.processing import calculate_loss

data = read_ovna_file('examples/data/R1C2S1_spiral_W1p0_L3000_R50.OVNA4')
avg_loss = fit_spectrum_peaks(distance_points=distance_points, raw_spectrum=data, labels=labels)
```

See `examples/propagation_loss.ipynb` for a complete walkthrough.

---

## 🧠 Contributing

Pull requests are welcome. Please document any new functionality and include appropriate tests.

---

## 📃 License

MIT License
