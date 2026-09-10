import Papa from "papaparse";

import type { Population } from "../types/Population";

export async function carregarPopulacao(): Promise<Population[]> {
  const response = await fetch(
    "/populacao_60mais_1209.csv"
  );

  if (!response.ok) {
    throw new Error(
      "Não foi possível carregar o arquivo CSV."
    );
  }

  const texto = await response.text();

  const resultado = Papa.parse<string[]>(
    texto,
    {
      delimiter: ";",
      skipEmptyLines: true,
    }
  );

  const linhas = resultado.data;

  const indiceCabecalho = linhas.findIndex(
    (linha) =>
      linha[0] === "Unidade da Federação" &&
      linha[1] === "60 a 69 anos" &&
      linha[2] === "70 anos ou mais"
  );

  if (indiceCabecalho === -1) {
    throw new Error(
      "Cabeçalho dos dados não encontrado no CSV."
    );
  }

  const dados: Population[] = [];

  for (
    let i = indiceCabecalho + 1;
    i < linhas.length;
    i++
  ) {
    const linha = linhas[i];

    if (!linha[0]) {
      continue;
    }

    if (
      linha[0].startsWith("Fonte:")
    ) {
      break;
    }

    const faixa60a69 = Number(
      linha[1]
    );

    const faixa70Mais = Number(
      linha[2]
    );

    if (
      Number.isNaN(faixa60a69) ||
      Number.isNaN(faixa70Mais)
    ) {
      continue;
    }

    dados.push({
      uf: linha[0],
      faixa60a69,
      faixa70Mais,
      total60Mais:
        faixa60a69 + faixa70Mais,
    });
  }

  return dados;
}