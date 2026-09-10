interface FooterProps {
  totalUnidades: number;
}

export function Footer({ totalUnidades }: FooterProps) {
  return (
    <footer className="footer">
      <span>
        Dados extraídos da Tabela 1209 (SIDRA/IBGE) via automação RPA.
      </span>

      <span>
        {totalUnidades} unidades federativas processadas
      </span>
    </footer>
  );
}
