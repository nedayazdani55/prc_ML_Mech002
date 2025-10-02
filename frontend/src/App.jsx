import React, { useState } from "react";
import DisplacementChart from "./components/DisplacementChart";
import ForceChart from "./components/ForceChart";
import StressChart from "./components/StressChart";

const API_BASE = "http://localhost:8000";

export default function App() {
  const [load, setLoad] = useState(-1000);
  const [A, setA] = useState(0.0001);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const onPredict = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch(API_BASE + "/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ load: Number(load), A: Number(A), use_model: true }),
      });
      const data = await res.json();
      setResult(data.result); // فقط بخش result
    } catch (err) {
      setResult({ error: err.toString() });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Truss AI — Demo</h1>
      <div className="card">
        <label>Load (N, negative = downward)</label>
        <input type="number" value={load} onChange={e=>setLoad(e.target.value)} />
        <label>Area (m²)</label>
        <input type="number" step="1e-7" value={A} onChange={e=>setA(e.target.value)} />
        <button onClick={onPredict} disabled={loading}>
          {loading ? "Running..." : "Predict / Run FEA"}
        </button>
      </div>

      <div className="card">
        <h3>Raw JSON Result</h3>
        <pre>{result ? JSON.stringify(result, null, 2) : "No result yet"}</pre>
      </div>

      {/* نمودارها */}
      {result && (
        <div className="charts">
          <DisplacementChart data={result.u} />
          <ForceChart data={result.elem_forces} />
          <StressChart data={result.elem_stresses} maxStress={result.max_stress} />
          <p><strong>Max Displacement: {result.max_disp}</strong></p>
        </div>
      )}

      <footer>Backend must run on <code>http://localhost:8000</code></footer>
    </div>
  );
}










// import React, { useState } from "react";

// const API_BASE = "http://localhost:8000";

// export default function App(){
//   const [load, setLoad] = useState(-1000);
//   const [A, setA] = useState(0.0001);
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);

//   const onPredict = async () => {
//     setLoading(true);
//     setResult(null);
//     try{
//       const res = await fetch(API_BASE + "/predict", {
//         method: "POST",
//         headers: {"Content-Type":"application/json"},
//         body: JSON.stringify({ load: Number(load), A: Number(A), use_model: true })
//       });
//       const data = await res.json();
//       setResult(data);
//     }catch(err){
//       setResult({error: err.toString()});
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="container">
//       <h1>Truss AI — Demo</h1>
//       <div className="card">
//         <label>Load (N, negative = downward)</label>
//         <input type="number" value={load} onChange={e=>setLoad(e.target.value)} />
//         <label>Area (m²)</label>
//         <input type="number" step="1e-7" value={A} onChange={e=>setA(e.target.value)} />
//         <button onClick={onPredict} disabled={loading}>{loading ? "Running..." : "Predict / Run FEA"}</button>
//       </div>

//       <div className="card">
//         <h3>Result</h3>
//         <pre>{result ? JSON.stringify(result, null, 2) : "No result yet"}</pre>
//       </div>

//       <footer>Backend must run on <code>http://localhost:8000</code></footer>
//     </div>
//   );
// }
