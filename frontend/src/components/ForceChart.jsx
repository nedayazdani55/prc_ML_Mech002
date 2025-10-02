import React from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";

export default function ForceChart({ data }) {
  const chartData = data?.map((f, i) => ({ name: `Elem ${i+1}`, force: f })) || [];
  return (
    <div>
      <h4>Element Forces</h4>
      {chartData.length > 0 ? (
        <BarChart width={500} height={300} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="force" fill="#8884d8" />
        </BarChart>
      ) : <p>No force data</p>}
    </div>
  );
}
