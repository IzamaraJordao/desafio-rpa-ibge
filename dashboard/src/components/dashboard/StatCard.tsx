export type CardVariant = "primary" | "success" | "danger" | "neutral";

interface StatCardProps {
  label: string;
  value: string;
  helper: string;
  variant: CardVariant;
}

export function StatCard({ label, value, helper, variant }: StatCardProps) {
  return (
    <div className={`card card--${variant}`}>
      <span>{label}</span>

      <strong>{value}</strong>

      <small>{helper}</small>
    </div>
  );
}
