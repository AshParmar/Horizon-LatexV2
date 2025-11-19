import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ExternalLink, CheckCircle2, Clock } from "lucide-react";

interface GoogleSheetTileProps {
  title: string;
  sheetUrl: string;
  lastSynced: string;
  autoSync: boolean;
  recordCount: number;
}

export const GoogleSheetTile = ({ 
  title, 
  sheetUrl, 
  lastSynced, 
  autoSync, 
  recordCount 
}: GoogleSheetTileProps) => {
  return (
    <Card className="p-6 shadow-card hover:shadow-card-hover transition-shadow">
      <div className="flex items-start gap-4">
        <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
          <svg className="h-6 w-6 text-primary" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
          </svg>
        </div>
        
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-foreground mb-1">{title}</h3>
          <p className="text-sm text-muted-foreground mb-3">{recordCount} records</p>
          
          <div className="flex items-center gap-4 text-xs text-muted-foreground mb-3">
            <div className="flex items-center gap-1">
              {autoSync ? (
                <CheckCircle2 className="h-3.5 w-3.5 text-status-selected" />
              ) : (
                <Clock className="h-3.5 w-3.5 text-status-pending" />
              )}
              <span>{autoSync ? "Auto-sync ON" : "Manual sync"}</span>
            </div>
            <div>Last synced: {lastSynced}</div>
          </div>
          
          <Button 
            size="sm" 
            variant="outline"
            className="gap-2"
            onClick={() => window.open(sheetUrl, '_blank')}
          >
            Open Sheet
            <ExternalLink className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>
    </Card>
  );
};
