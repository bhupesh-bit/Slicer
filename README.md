# Horizontal Slicer Pipeline

Three different topology classification strategies i have implemented and compared:

1. **Winding Rule (Signed Area)**
2. **Trimesh Enclosure Graph**(**will work most of the time ,requires networkx & rtree , work on collab/kaggle/python older version 3.12**)
3. **Parity (Even–Odd Region Classification)** -( good output for cluster.stl)

---

## Folder Structure

slicer_pipeline/
├── common.py
├── slicer_parity.py
├── slicer_winding.py
├── slicer_enclosure.py
├── run_slicer.py
├── README.md
---

## Python Version

> **Python 3.14.2+**  

## Dependencies / Requirements

The following Python packages are required:

- `numpy`
- `trimesh`
- `shapely`
- `matplotlib`
- `networkx` (required internally by trimesh for enclosure graph)()
-`rtree`

---

## Run

Edit `run_slicer.py`:
   - Choose method: `METHOD = "parity"` / `"winding"` / `"enclosure"`
   - Choose model: `MODEL_NAME = "cluster.stl"` or `"carburetor.stl"`


├── cluster.stl
└── carburetor.stl


---

## Output

For each layer:
Slicer_Output/
0.00/
outer.png
holes.png
0.50/
outer.png
holes.png


- `outer.png` → outer boundaries
- `holes.png` → inner holes


## Methods

### 1. Winding Rule
Classifies CCW loops as solid and CW as holes.  
**Limitation:** will work for cluster but not generating inner lopes in carburetor

### 2. Enclosure Graph
Uses Trimesh nesting graph to detect hierarchy.  
**Limitation:** working in both ,but in cluster polygon and inner hole sizes are bigger

### 3. Parity (Final)
Uses even–odd rule on region containment.  
**Robust and correct for real CAD models.**working perfect in cluster , but in carburetor starts from 4.5 and not working properly

---
