









# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os, joblib, numpy as np
from truss_fea import solve_truss, build_demo_truss
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Truss-AI-CAE API")

# allow local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:3000","http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Element(BaseModel):
    n1: int
    n2: int
    A: float
    E: float

class FEAInput(BaseModel):
    nodes: List[List[float]]
    elements: List[Element]
    loads: List[float]
    fixed_dofs: List[int]

class PredictInput(BaseModel):
    load: float = -1000.0
    A: float = 1e-4
    E: float = 210e9
    use_model: bool = True  # try ML model if exists, else fallback to FEA

MODEL_PATH = "outputs/model.joblib"

@app.get("/")
def root():
    return {"status":"ok", "notes":"POST /run_fea or /predict"}

@app.post("/run_fea")
def run_fea(payload: FEAInput):
    try:
        nodes = payload.nodes
        elements = [el.dict() for el in payload.elements]
        res = solve_truss(nodes, elements, payload.loads, payload.fixed_dofs)
        return {"success": True, "result": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict")
def predict(payload: PredictInput):
    # Build demo truss from simple params
    nodes, elements, loads, fixed = build_demo_truss(load=payload.load, A=payload.A, E=payload.E)
    # if model exists and user asked to use it, try using it
    if payload.use_model and os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            # try to guess expected features
            n_features = getattr(model, "n_features_in_", None)
            # common simple case: features = [abs(load), A]
            X = np.array([[abs(payload.load), payload.A]])
            if n_features is None or n_features == X.shape[1]:
                ypred = model.predict(X)
                return {"success": True, "source": "ml_model", "prediction": float(ypred[0])}
            # fallback: if model expects different shape, do FEA fallback
        except Exception:
            # if model corrupt or mismatch, fallback silently to FEA
            pass
    # fallback: run actual FEA with the demo geometry
    try:
        res = solve_truss(nodes, elements, loads, fixed)
        return {"success": True, "source": "fea", "result": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"ok": True, "model_exists": os.path.exists(MODEL_PATH)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)













    # # api.py
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List
# import os, joblib, numpy as np, json, pandas as pd
# from truss_fea import solve_truss, build_demo_truss
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime

# app = FastAPI(title="Truss-AI-CAE API")

# # CORS for local frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173","http://localhost:3000","http://127.0.0.1:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Folder for saving CSV/JSON
# DATA_FOLDER = "data"
# os.makedirs(DATA_FOLDER, exist_ok=True)

# def save_result(result):
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
#     # Save JSON
#     json_path = os.path.join(DATA_FOLDER, f"result_{timestamp}.json")
#     with open(json_path, "w") as f:
#         json.dump(result, f, indent=2)
    
#     # Save CSV
#     df = pd.DataFrame({
#         "displacement": result.get("u", []),
#         "force": result.get("elem_forces", []),
#         "stress": result.get("elem_stresses", [])
#     })
#     df["max_stress"] = result.get("max_stress", 0)
#     df["max_disp"] = result.get("max_disp", 0)
#     csv_path = os.path.join(DATA_FOLDER, f"result_{timestamp}.csv")
#     df.to_csv(csv_path, index=False)

# # Pydantic models
# class Element(BaseModel):
#     n1: int
#     n2: int
#     A: float
#     E: float

# class FEAInput(BaseModel):
#     nodes: List[List[float]]
#     elements: List[Element]
#     loads: List[float]
#     fixed_dofs: List[int]

# class PredictInput(BaseModel):
#     load: float = -1000.0
#     A: float = 1e-4
#     E: float = 210e9
#     use_model: bool = True

# MODEL_PATH = "outputs/model.joblib"

# @app.get("/")
# def root():
#     return {"status":"ok", "notes":"POST /run_fea or /predict"}

# @app.post("/run_fea")
# def run_fea(payload: FEAInput):
#     try:
#         nodes = payload.nodes
#         elements = [el.dict() for el in payload.elements]
#         res = solve_truss(nodes, elements, payload.loads, payload.fixed_dofs)
#         save_result(res)
#         return {"success": True, "result": res}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.post("/predict")
# def predict(payload: PredictInput):
#     # Build demo truss
#     nodes, elements, loads, fixed = build_demo_truss(load=payload.load, A=payload.A, E=payload.E)
    
#     final_result = None
#     prediction = None

#     # Try ML model
#     if payload.use_model and os.path.exists(MODEL_PATH):
#         try:
#             model = joblib.load(MODEL_PATH)
#             X = np.array([[abs(payload.load), payload.A]])
#             prediction = float(model.predict(X)[0])
#         except Exception:
#             prediction = None

#     # Run FEA fallback (or always for consistent result)
#     try:
#         res = solve_truss(nodes, elements, loads, fixed)
#         save_result(res)
#         final_result = res
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     response = {"success": True, "source": "ml_model" if prediction else "fea", "result": final_result}
#     if prediction:
#         response["prediction"] = prediction
#     return response

# @app.get("/health")
# def health():
#     return {"ok": True, "model_exists": os.path.exists(MODEL_PATH)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)










# # api.py
# # from fastapi import FastAPI, HTTPException
# # from pydantic import BaseModel
# # from typing import List, Optional
# # import os, joblib, numpy as np, json, pandas as pd
# # from truss_fea import solve_truss, build_demo_truss
# # from fastapi.middleware.cors import CORSMiddleware
# # from datetime import datetime

# # app = FastAPI(title="Truss-AI-CAE API")

# # # allow local frontend
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["http://localhost:5173","http://localhost:3000","http://127.0.0.1:5173"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # DATA_FOLDER = "data"
# # os.makedirs(DATA_FOLDER, exist_ok=True)

# # def save_result(result):
# #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
# #     # Save JSON
# #     json_path = os.path.join(DATA_FOLDER, f"result_{timestamp}.json")
# #     with open(json_path, "w") as f:
# #         json.dump(result, f, indent=2)
    
# #     # Save CSV
# #     df = pd.DataFrame({
# #         "displacement": result.get("u", []),
# #         "force": result.get("elem_forces", []),
# #         "stress": result.get("elem_stresses", [])
# #     })
# #     df["max_stress"] = result.get("max_stress", 0)
# #     df["max_disp"] = result.get("max_disp", 0)
# #     csv_path = os.path.join(DATA_FOLDER, f"result_{timestamp}.csv")
# #     df.to_csv(csv_path, index=False)

# # class Element(BaseModel):
# #     n1: int
# #     n2: int
# #     A: float
# #     E: float

# # class FEAInput(BaseModel):
# #     nodes: List[List[float]]
# #     elements: List[Element]
# #     loads: List[float]
# #     fixed_dofs: List[int]

# # class PredictInput(BaseModel):
# #     load: float = -1000.0
# #     A: float = 1e-4
# #     E: float = 210e9
# #     use_model: bool = True  # try ML model if exists, else fallback to FEA

# # MODEL_PATH = "outputs/model.joblib"

# # @app.get("/")
# # def root():
# #     return {"status":"ok", "notes":"POST /run_fea or /predict"}

# # @app.post("/run_fea")
# # def run_fea(payload: FEAInput):
# #     try:
# #         nodes = payload.nodes
# #         elements = [el.dict() for el in payload.elements]
# #         res = solve_truss(nodes, elements, payload.loads, payload.fixed_dofs)
# #         return {"success": True, "result": res}
# #     except Exception as e:
# #         raise HTTPException(status_code=400, detail=str(e))

# # @app.post("/predict")
# # def predict(payload: PredictInput):
# #     # Build demo truss from simple params
# #     nodes, elements, loads, fixed = build_demo_truss(load=payload.load, A=payload.A, E=payload.E)
    
# #     # Try ML model if exists
# #     if payload.use_model and os.path.exists(MODEL_PATH):
# #         try:
# #             model = joblib.load(MODEL_PATH)
# #             n_features = getattr(model, "n_features_in_", None)
# #             X = np.array([[abs(payload.load), payload.A]])
# #             if n_features is None or n_features == X.shape[1]:
# #                 ypred = model.predict(X)
# #                 return {"success": True, "source": "ml_model", "prediction": float(ypred[0])}
# #         except Exception:
# #             pass  # fallback to FEA if model fails

# #     # FEA fallback
# #     try:
# #         res = solve_truss(nodes, elements, loads, fixed)
# #         save_result(res)
# #         return {"success": True, "source": "fea", "result": res}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.get("/health")
# # def health():
# #     return {"ok": True, "model_exists": os.path.exists(MODEL_PATH)}

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

