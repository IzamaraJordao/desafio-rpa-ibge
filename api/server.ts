import cors from "cors";
import express from "express";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const app = express();

app.use(cors());
app.use(express.json());

const PORT = 3333;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const raizProjeto = path.resolve(
  __dirname,
  ".."
);

const pythonPath = path.resolve(
  raizProjeto,
  ".venv",
  "Scripts",
  "python.exe"
);

const scriptPath = path.resolve(
  raizProjeto,
  "desafio_ibge_1209.py"
);

app.get("/health", (_req, res) => {
  return res.json({
    status: "ok",
  });
});

app.post(
  "/executar-rpa",
  (_req, res) => {
    console.log(
      "Iniciando automação..."
    );

    console.log(
      "Python:",
      pythonPath
    );

    console.log(
      "Script:",
      scriptPath
    );

    const processo = spawn(
      pythonPath,
      [scriptPath],
      {
        cwd: raizProjeto,
      }
    );

    let saida = "";
    let erro = "";

    processo.stdout.on(
      "data",
      (data) => {
        const texto =
          data.toString();

        saida += texto;

        console.log(texto);
      }
    );

    processo.stderr.on(
      "data",
      (data) => {
        const texto =
          data.toString();

        erro += texto;

        console.error(texto);
      }
    );

    processo.on(
      "error",
      (error) => {
        console.error(
          "Erro ao iniciar processo:",
          error
        );

        if (!res.headersSent) {
          return res
            .status(500)
            .json({
              sucesso: false,
              mensagem:
                "Não foi possível iniciar a automação.",
              erro:
                error.message,
            });
        }
      }
    );

    processo.on(
      "close",
      (codigo) => {
        if (res.headersSent) return;
        console.log(
          "Processo finalizado:",
          codigo
        );

        if (codigo !== 0) {
          return res
            .status(500)
            .json({
              sucesso: false,
              mensagem:
                "Erro durante a execução da automação.",
              erro,
              saida,
            });
        }

        return res.json({
          sucesso: true,
          mensagem:
            "Automação concluída com sucesso.",
          saida,
        });
      }
    );
  }
);

app.listen(
  PORT,
  () => {
    console.log(
      `API rodando em http://localhost:${PORT}`
    );
  }
);