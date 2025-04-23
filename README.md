# pyOVNA

`pyOVNA` is a lightweight Python toolkit for processing and analyzing data from Optical Vector Network Analyzer (OVNA) measurements.

It supports:

- Loading and parsing custom `.OVNA4` binary files
- Signal processing (filtering, smoothing, etc.)
- Spectral fitting and propagation loss extraction
- Jupyter-based analysis with real-world examples

---

<!-- ## 📦 Installation

Clone the repo and install locally:

```bash
git clone https://github.com/gcharalampous/pyOVNA.git
cd pyOVNA
pip install .
```

Or with editable mode (useful for development):

```bash
pip install -e .
```

--- -->

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
│   └── propagation_loss.ipynb
├── LICENSE
├── pyOVNA
│   ├── filters.py
│   ├── fitting.py
│   ├── __init__.py
│   ├── io.py
│   └── processing.py
├── pyproject.toml
├── README.md
└── tests
```

---

## 🚀 Usage Example

Inside a notebook:

```python
from pyOVNA.io import load_ovna
from pyOVNA.processing import calculate_loss

data = load_ovna('examples/data/R1C2S1_spiral_W1p0_L3000_R50.OVNA4')
loss = calculate_loss(data)
```

See `examples/propagation_loss.ipynb` for a complete walkthrough.

---

## 🧠 Contributing

Pull requests are welcome. Please document any new functionality and include appropriate tests.

---

## 📃 License

MIT License
