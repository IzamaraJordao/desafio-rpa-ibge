import { usePopulacao } from "./hooks/usePopulacao";

import { TopBar } from "./components/layout/TopBar";
import { Footer } from "./components/layout/Footer";
import { Hero } from "./components/dashboard/Hero";
import { SummaryCards } from "./components/dashboard/SummaryCards";
import { PopulationChart } from "./components/dashboard/PopulationChart";
import { RankingTable } from "./components/dashboard/RankingTable";
import { LoadingState } from "./components/feedback/LoadingState";
import { ErrorState } from "./components/feedback/ErrorState";

import "./styles.css";

export default function App() {
  const {
    carregando,
    erro,
    busca,
    setBusca,
    ranking,
    dadosFiltrados,
    totalBrasil,
    maior,
    menor,
    recarregar,
  } = usePopulacao();

  if (carregando) {
    return <LoadingState />;
  }

  if (erro) {
    return <ErrorState mensagem={erro} />;
  }

  return (
    <main className="container">
      <TopBar onAtualizar={recarregar} />

      <Hero />

      <SummaryCards
        totalBrasil={totalBrasil}
        maior={maior}
        menor={menor}
        totalUnidades={ranking.length}
      />

      <PopulationChart dados={ranking} />

      <RankingTable
        ranking={ranking}
        dadosFiltrados={dadosFiltrados}
        busca={busca}
        onBuscaChange={setBusca}
      />

      <Footer totalUnidades={ranking.length} />
    </main>
  );
}
