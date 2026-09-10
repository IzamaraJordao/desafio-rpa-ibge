import { formatarNumero } from "../../utils/formatNumero";
import type { Population } from "../../types/Population";

interface RankingTableProps {
  ranking: Population[];
  dadosFiltrados: Population[];
  busca: string;
  onBuscaChange: (valor: string) => void;
}

export function RankingTable({
  ranking,
  dadosFiltrados,
  busca,
  onBuscaChange,
}: RankingTableProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <h2>
            Ranking por Unidade da Federação
          </h2>

          <p>
            Dados processados a partir do CSV
            gerado pelo SIDRA
          </p>
        </div>

        <input
          className="search"
          placeholder="Buscar UF..."
          value={busca}
          onChange={(event) =>
            onBuscaChange(event.target.value)
          }
        />
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Ranking</th>
              <th>UF</th>
              <th>60 a 69</th>
              <th>70+</th>
              <th>Total 60+</th>
            </tr>
          </thead>

          <tbody>
            {dadosFiltrados.map((item) => {
              const posicao =
                ranking.findIndex(
                  (registro) =>
                    registro.uf === item.uf
                ) + 1;

              return (
                <tr key={item.uf}>
                  <td>
                    <span
                      className={`rank-badge ${
                        posicao <= 3 ? `top-${posicao}` : ""
                      }`}
                    >
                      {posicao}º
                    </span>
                  </td>

                  <td>
                    <strong>
                      {item.uf}
                    </strong>
                  </td>

                  <td>
                    {formatarNumero(
                      item.faixa60a69
                    )}
                  </td>

                  <td>
                    {formatarNumero(
                      item.faixa70Mais
                    )}
                  </td>

                  <td>
                    <strong>
                      {formatarNumero(
                        item.total60Mais
                      )}
                    </strong>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
