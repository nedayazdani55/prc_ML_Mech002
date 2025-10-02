# 📘 AutoFEA-ML

**AutoFEA-ML** is an educational and experimental project demonstrating how to combine **Artificial Intelligence (ML)** with **Finite Element Analysis (FEA)**.  
It includes a **Backend** built with **FastAPI** and a **Frontend** using **React + Vite**.  
Users can input load and cross-sectional area, then view FEA results such as **Displacements**, **Forces**, and **Stresses** both as raw JSON and as interactive charts.

---

## ⚙️ Installation & Run

### 1. Backend (FastAPI + Python)

```bash
# navigate to project root
cd AutoFEA-ML

# create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# install requirements
pip install -r requirements.txt

Run backend:
uvicorn api:app --reload

Default addresses:
Backend API → http://localhost:8000
Docs (Swagger UI) → http://localhost:8000/docs

2. Frontend (React + Vite)
cd frontend
npm install
Run frontend:
npm run dev

Default address:
Frontend UI → http://localhost:5173

📊 Features

🔧 FEA Solver: Calculates displacements, element forces, and stresses for a demo truss
🤖 ML Model: Supports optional ML prediction if model.joblib exists
📈 Visualization: Displays results in three separate charts (Displacement, Forces, Stresses)
💾 Data Logging: Stores test results in JSON and CSV under outputs/
🌐 API: REST endpoints served by FastAPI (/predict, /run_fea)

API Endpoints
GET / → API status
POST /predict → Predict or run FEA from simple inputs:

{
  "load": -1000,
  "A": 0.0001,
  "E": 210000000000,
  "use_model": true
}

POST /run_fea → Run FEA with full data (nodes, elements, loads, fixed DOFs)
GET /health → Health check (and whether ML model exists)

Example JSON Output:
{
  "success": true,
  "source": "fea",
  "result": {
    "u": [0.0, 0.0, -4.7e-05, -1.34e-04, -9.52e-05, -3.64e-04, 0.0, -1.34e-04],
    "elem_forces": [-1000.0, -1000.0, -1414.21, 0.0, 1414.21],
    "elem_stresses": [-1e7, -1e7, -1.41e7, 0.0, 1.41e7],
    "max_stress": 14142135.62,
    "max_disp": 0.0003646
  }
}

Requirements :
Python 3.10+
Node.js 18+
npm 9+
Modern browser (Chrome, Edge, Firefox)
