import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { formatarNumero } from "../../utils/formatNumero";
import type { Population } from "../../types/Population";

interface PopulationChartProps {
  dados: Population[];
}

export function PopulationChart({ dados }: PopulationChartProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <h2>
            População 60+ por UF
          </h2>

          <p>
            Comparação entre as faixas etárias
          </p>
        </div>
      </div>

      <div className="chart">
        <ResponsiveContainer
          width="100%"
          height={420}
        >
          <BarChart data={dados}>
            <CartesianGrid
              strokeDasharray="3 3"
            />

            <XAxis
              dataKey="uf"
              angle={-45}
              textAnchor="end"
              height={120}
              interval={0}
            />

            <YAxis />

            <Tooltip
              formatter={(value) =>
                formatarNumero(
                  Number(value)
                )
              }
            />

            <Legend />

            <Bar
              dataKey="faixa60a69"
              name="60 a 69 anos"
              fill="#753bbd"
            />

            <Bar
              dataKey="faixa70Mais"
              name="70 anos ou mais"
              fill="#ff6900"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
