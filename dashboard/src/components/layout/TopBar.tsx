import logoLev from "../../assets/logoLev.jpg";
import { useState } from "react";
import { executarRpa } from "../../services/rpaService";
import { toast } from "react-toastify";

interface TopBarProps {
  onAtualizar: () => Promise<void>;
}

export function TopBar({ onAtualizar }: TopBarProps) {
  const [executandoRpa, setExecutandoRpa] = useState(false);

  const [mensagemRpa, setMensagemRpa] = useState("");

  async function atualizarDados() {
    try {
      setExecutandoRpa(true);
      setMensagemRpa("Executando automação no SIDRA...");

      await executarRpa();

      setMensagemRpa("Automação concluída! Atualizando dashboard...");

      await onAtualizar();

      setMensagemRpa("Dados carregados");
      toast.success("Dados atualizados com sucesso!");
    } catch (error) {
      console.error(error);

      const mensagemErro =
        error instanceof Error ? error.message : "Erro ao atualizar dados.";

      setMensagemRpa("Dados carregados");
      toast.error(mensagemErro);
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

    </div>
  );
}
