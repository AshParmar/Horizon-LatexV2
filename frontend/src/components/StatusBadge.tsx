import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export type CandidateStatus = 
  | "selected" 
  | "rejected" 
  | "pending" 
  | "needs-review"
  | "auto-selected"
  | "auto-rejected";

interface StatusBadgeProps {
  status: CandidateStatus;
  className?: string;
}

const statusConfig = {
  "selected": {
    label: "Selected (Human)",
    className: "bg-status-selected/10 text-status-selected border-status-selected/20",
  },
  "auto-selected": {
    label: "Auto-Selected (AI)",
    className: "bg-status-selected/10 text-status-selected border-status-selected/20",
  },
  "rejected": {
    label: "Rejected (Human)",
    className: "bg-status-rejected/10 text-status-rejected border-status-rejected/20",
  },
  "auto-rejected": {
    label: "Auto-Rejected (AI)",
    className: "bg-status-rejected/10 text-status-rejected border-status-rejected/20",
  },
  "pending": {
    label: "Pending — Waiting for HR",
    className: "bg-status-pending/10 text-status-pending border-status-pending/20",
  },
  "needs-review": {
    label: "Needs Manual Review",
    className: "bg-status-review/10 text-status-review border-status-review/20",
  },
};

export const StatusBadge = ({ status, className }: StatusBadgeProps) => {
  const config = statusConfig[status];
  
  return (
    <Badge 
      variant="outline" 
      className={cn("font-medium", config.className, className)}
    >
      {config.label}
    </Badge>
  );
};
