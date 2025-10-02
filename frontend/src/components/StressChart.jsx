import React from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, LabelList } from "recharts";

export default function StressChart({ data, maxStress }) {
  const chartData = data?.map((s, i) => ({ name: `Elem ${i+1}`, stress: s })) || [];
  return (
    <div>
      <h4>Element Stresses</h4>
      {chartData.length > 0 ? (
        <BarChart width={600} height={400} data={chartData} margin={{ top: 20, right: 30, left: 30, bottom: 70 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-30} textAnchor="end" interval={0}/>
          <YAxis tickFormatter={(val) => (val / 1e6).toFixed(1) + " MPa"}/>
          <Tooltip formatter={(val) => (val / 1e6).toFixed(2) + " MPa"} />
          <Bar dataKey="stress" fill="#ff7300">
            <LabelList dataKey="stress" position="top" formatter={(val) => (val / 1e6).toFixed(1)}/>
          </Bar>
        </BarChart>
      ) : <p>No stress data</p>}
      {maxStress && <p><strong>Max Stress: {maxStress}</strong></p>}
    </div>
  );
}
