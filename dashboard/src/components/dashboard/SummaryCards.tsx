import { formatarNumero } from "../../utils/formatNumero";
import type { Population } from "../../types/Population";
import { StatCard } from "./StatCard";

interface SummaryCardsProps {
  totalBrasil: number;
  maior?: Population;
  menor?: Population;
  totalUnidades: number;
}

export function SummaryCards({
  totalBrasil,
  maior,
  menor,
  totalUnidades,
}: SummaryCardsProps) {
  return (
    <section className="cards">
      <StatCard
        variant="primary"
        label="População 60+"
        value={formatarNumero(totalBrasil)}
        helper="Soma das 27 UFs"
      />

      <StatCard
        variant="success"
        label="Maior população"
        value={maior?.uf ?? "-"}
        helper={formatarNumero(maior?.total60Mais ?? 0)}
      />

      <StatCard
        variant="danger"
        label="Menor população"
        value={menor?.uf ?? "-"}
        helper={formatarNumero(menor?.total60Mais ?? 0)}
      />

      <StatCard
        variant="neutral"
        label="Unidades Federativas"
        value={String(totalUnidades)}
        helper="Estados + DF"
      />
    </section>
  );
}
