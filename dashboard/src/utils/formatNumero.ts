export function formatarNumero(valor: number): string {
  return new Intl.NumberFormat("pt-BR").format(valor);
}
