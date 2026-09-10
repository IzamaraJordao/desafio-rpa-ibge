import logoLev from "../../assets/logoLev.jpg";
import { useState } from "react";
import { executarRpa } from "../../services/rpaService";
import { Toast } from "../feedback/Toast";

interface TopBarProps {
  onAtualizar: () => Promise<void>;
}

interface ToastState {
  mensagem: string;
  tipo: "sucesso" | "erro";
}

export function TopBar({ onAtualizar }: TopBarProps) {
  const [executandoRpa, setExecutandoRpa] = useState(false);

  const [mensagemRpa, setMensagemRpa] = useState("");
  const [toast, setToast] = useState<ToastState | null>(null);

  async function atualizarDados() {
    try {
      setExecutandoRpa(true);
      setMensagemRpa("Executando automação no SIDRA...");

      await executarRpa();

      setMensagemRpa("Automação concluída! Atualizando dashboard...");

      // Carrega novamente o CSV gerado
      await onAtualizar();

      setMensagemRpa("Dados carregados");
      setToast({
        tipo: "sucesso",
        mensagem: "Dados atualizados com sucesso!",
      });
    } catch (error) {
      console.error(error);

      const mensagemErro =
        error instanceof Error ? error.message : "Erro ao atualizar dados.";

      setMensagemRpa("Dados carregados");
      setToast({ tipo: "erro", mensagem: mensagemErro });
    } finally {
      setExecutandoRpa(false);
    }
  }
  return (
    <div className="topbar">
      <div className="brand">
        <div className="brand-mark">IBGE</div>

        <div className="brand-text">
          <strong>Painel Tabela 1209</strong>
          <span>Automação RPA · SIDRA</span>
        </div>
      </div>

      <div className="header-actions">
        <div className="status">
          <span
            className={
              executandoRpa ? "status-dot status-dot-loading" : "status-dot"
            }
          />
          {mensagemRpa || "Dados carregados"}
        </div>

        <button
          className="update-button"
          onClick={atualizarDados}
          disabled={executandoRpa}
        >
          {executandoRpa ? (
            <>
              <span className="spinner" />
              Executando automação...
            </>
          ) : (
            "Atualizar dados do IBGE"
          )}
        </button>
      </div>

      <img className="powered-by-logo" src={logoLev} alt="Lev" />

      {toast && (
        <Toast
          mensagem={toast.mensagem}
          tipo={toast.tipo}
          onFechar={() => setToast(null)}
        />
      )}
    </div>
  );
}
