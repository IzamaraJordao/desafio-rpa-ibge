interface ExecutarRpaResponse {
  sucesso: boolean;
  mensagem: string;
  saida?: string;
  erro?: string;
}

export async function executarRpa(): Promise<ExecutarRpaResponse> {
  const response = await fetch(
    "http://localhost:3333/executar-rpa",
    {
      method: "POST",
    }
  );

  const resultado: ExecutarRpaResponse =
    await response.json();

  if (!response.ok) {
    throw new Error(
      resultado.erro ||
        resultado.mensagem ||
        "Erro ao executar automação."
    );
  }

  return resultado;
}