import { Card } from "@/components/ui/card";
import { Mail, FileText, Sparkles, Target, Database, UserCheck, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";

const stages = [
  { name: "Gmail", icon: Mail, status: "active" },
  { name: "Parsing", icon: FileText, status: "active" },
  { name: "Enrichment", icon: Sparkles, status: "active" },
  { name: "Scoring", icon: Target, status: "active" },
  { name: "Decision", icon: Sparkles, status: "processing" },
  { name: "Sheets Sync", icon: Database, status: "pending" },
  { name: "Human Review", icon: UserCheck, status: "pending" },
];

export const PipelineVisualization = () => {
  return (
    <Card className="p-6 shadow-card">
      <h3 className="text-lg font-semibold mb-6">Candidate Pipeline</h3>
      
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {stages.map((stage, index) => (
          <div key={stage.name} className="flex items-center gap-2">
            <div className="flex flex-col items-center gap-2 min-w-[120px]">
              <div className={cn(
                "h-16 w-16 rounded-xl flex items-center justify-center transition-all",
                stage.status === "active" && "bg-primary/10 text-primary",
                stage.status === "processing" && "bg-status-pending/10 text-status-pending animate-pulse",
                stage.status === "pending" && "bg-muted text-muted-foreground"
              )}>
                <stage.icon className="h-7 w-7" />
              </div>
              <div className="text-center">
                <p className={cn(
                  "text-xs font-medium",
                  stage.status === "active" && "text-primary",
                  stage.status === "processing" && "text-status-pending",
                  stage.status === "pending" && "text-muted-foreground"
                )}>
                  {stage.name}
                </p>
                <p className="text-[10px] text-muted-foreground mt-0.5">
                  {stage.status === "active" && "Complete"}
                  {stage.status === "processing" && "Processing..."}
                  {stage.status === "pending" && "Pending"}
                </p>
              </div>
            </div>
            
            {index < stages.length - 1 && (
              <ChevronRight className="h-5 w-5 text-muted-foreground flex-shrink-0 mt-[-24px]" />
            )}
          </div>
        ))}
      </div>
    </Card>
  );
};
