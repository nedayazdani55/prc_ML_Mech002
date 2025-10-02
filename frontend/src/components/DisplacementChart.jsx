import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";

export default function DisplacementChart({ data }) {
  const chartData = data?.map((u, i) => ({ name: `Node ${i+1}`, displacement: u })) || [];
  return (
    <div>
      <h4>Displacements</h4>
      {chartData.length > 0 ? (
        <LineChart width={600} height={400} data={chartData} margin={{ top: 20, right: 30, left: 30, bottom: 70 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-30} textAnchor="end" interval={0}/>
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="displacement" stroke="#82ca9d" />
        </LineChart>
      ) : <p>No displacement data</p>}
    </div>
  );
}
