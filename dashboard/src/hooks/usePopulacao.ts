import { useCallback, useEffect, useMemo, useState } from "react";

import { carregarPopulacao } from "../services/csvService";
import type { Population } from "../types/Population";

interface UsePopulacaoResult {
  carregando: boolean;
  erro: string;
  busca: string;
  setBusca: (valor: string) => void;
  ranking: Population[];
  dadosFiltrados: Population[];
  totalBrasil: number;
  maior?: Population;
  menor?: Population;
  recarregar: () => Promise<void>;
}

export function usePopulacao(): UsePopulacaoResult {
  const [dados, setDados] = useState<Population[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");
  const [busca, setBusca] = useState("");

  useEffect(() => {
    let ativo = true;

    carregarPopulacao()
      .then((resultado) => {
        if (ativo) setDados(resultado);
      })
      .catch((error: unknown) => {
        if (ativo) {
          setErro(error instanceof Error ? error.message : "Erro ao carregar dados.");
        }
      })
      .finally(() => {
        if (ativo) setCarregando(false);
      });

    return () => {
      ativo = false;
    };
  }, []);

  // Recarrega os dados sem derrubar o dashboard para a tela de loading em tela cheia
  const recarregar = useCallback(async () => {
    const resultado = await carregarPopulacao();
    setDados(resultado);
  }, []);

  const ranking = useMemo(() => {
    return [...dados].sort(
      (a, b) => b.total60Mais - a.total60Mais
    );
  }, [dados]);

  const dadosFiltrados = useMemo(() => {
    return ranking.filter((item) =>
      item.uf.toLowerCase().includes(
        busca.toLowerCase()
      )
    );
  }, [ranking, busca]);

  const totalBrasil = useMemo(() => {
    return dados.reduce(
      (total, item) => total + item.total60Mais,
      0
    );
  }, [dados]);

  return {
    carregando,
    erro,
    busca,
    setBusca,
    ranking,
    dadosFiltrados,
    totalBrasil,
    maior: ranking[0],
    menor: ranking[ranking.length - 1],
    recarregar,
  };
}
