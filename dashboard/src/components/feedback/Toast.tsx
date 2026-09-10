import { useEffect } from "react";

interface ToastProps {
  mensagem: string;
  tipo: "sucesso" | "erro";
  onFechar: () => void;
}

export function Toast({ mensagem, tipo, onFechar }: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(onFechar, 4000);
    return () => clearTimeout(timer);
  }, [onFechar]);

  return (
    <div className={`toast toast-${tipo}`} role="status">
      <span className="toast-icone">{tipo === "sucesso" ? "✓" : "!"}</span>
      <span>{mensagem}</span>
      <button
        className="toast-fechar"
        onClick={onFechar}
        aria-label="Fechar aviso"
      >
        ×
      </button>
    </div>
  );
}
