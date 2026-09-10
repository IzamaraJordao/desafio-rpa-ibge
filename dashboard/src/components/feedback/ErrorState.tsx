interface ErrorStateProps {
  mensagem: string;
}

export function ErrorState({ mensagem }: ErrorStateProps) {
  return (
    <div className="loading error">
      {mensagem}
    </div>
  );
}
