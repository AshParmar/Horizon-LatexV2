import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { Database, RefreshCw, CheckCircle2, Clock, ExternalLink } from "lucide-react";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

const SheetsSync = () => {
  const [autoSync, setAutoSync] = useState(true);
  const { toast } = useToast();

  const handleManualSync = () => {
    toast({
      title: "Syncing...",
      description: "Syncing data with Google Sheets",
    });
    setTimeout(() => {
      toast({
        title: "Sync Complete",
        description: "All data has been synced successfully",
      });
    }, 2000);
  };

  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">Sheets Sync</h1>
        <p className="text-muted-foreground">Manage Google Sheets synchronization</p>
      </div>

      {/* Sync Settings */}
      <Card className="p-6 shadow-card">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-lg font-semibold mb-1">Auto-Sync Settings</h2>
            <p className="text-sm text-muted-foreground">
              Automatically sync data every 5 minutes
            </p>
          </div>
          <Switch checked={autoSync} onCheckedChange={setAutoSync} />
        </div>

        <div className="flex items-center gap-3">
          <Button onClick={handleManualSync} className="gap-2">
            <RefreshCw className="h-4 w-4" />
            Manual Sync Now
          </Button>
          <Badge variant="outline" className="gap-1">
            <CheckCircle2 className="h-3 w-3 text-status-selected" />
            Connected
          </Badge>
        </div>
      </Card>

      {/* Sheets Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* All Candidates Sheet */}
        <Card className="p-6 shadow-card">
          <div className="flex items-start gap-4 mb-4">
            <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
              <Database className="h-6 w-6 text-primary" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-lg mb-1">All Candidates Sheet</h3>
              <p className="text-sm text-muted-foreground">
                Master sheet containing all candidate data
              </p>
            </div>
          </div>

          <div className="space-y-3 mb-4">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Total Records</span>
              <span className="font-medium">156</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Last Synced</span>
              <span className="font-medium">2 minutes ago</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Sync Status</span>
              <Badge variant="outline" className="gap-1">
                <CheckCircle2 className="h-3 w-3 text-status-selected" />
                Synced
              </Badge>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Auto-Update</span>
              <Badge variant="outline" className={autoSync ? "text-status-selected" : "text-muted-foreground"}>
                {autoSync ? "ON" : "OFF"}
              </Badge>
            </div>
          </div>

          <div className="flex gap-2">
            <Button 
              variant="outline" 
              className="flex-1 gap-2"
              onClick={() => window.open("https://docs.google.com/spreadsheets", "_blank")}
            >
              Open Sheet
              <ExternalLink className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon">
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
        </Card>

        {/* Selected Candidates Sheet */}
        <Card className="p-6 shadow-card">
          <div className="flex items-start gap-4 mb-4">
            <div className="h-12 w-12 rounded-lg bg-status-selected/10 flex items-center justify-center flex-shrink-0">
              <CheckCircle2 className="h-6 w-6 text-status-selected" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-lg mb-1">Selected Candidates Sheet</h3>
              <p className="text-sm text-muted-foreground">
                Filtered sheet with selected candidates only
              </p>
            </div>
          </div>

          <div className="space-y-3 mb-4">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Total Records</span>
              <span className="font-medium">34</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Last Synced</span>
              <span className="font-medium">2 minutes ago</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Sync Status</span>
              <Badge variant="outline" className="gap-1">
                <CheckCircle2 className="h-3 w-3 text-status-selected" />
                Synced
              </Badge>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Auto-Update</span>
              <Badge variant="outline" className={autoSync ? "text-status-selected" : "text-muted-foreground"}>
                {autoSync ? "ON" : "OFF"}
              </Badge>
            </div>
          </div>

          <div className="flex gap-2">
            <Button 
              variant="outline" 
              className="flex-1 gap-2"
              onClick={() => window.open("https://docs.google.com/spreadsheets", "_blank")}
            >
              Open Sheet
              <ExternalLink className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon">
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
        </Card>
      </div>

      {/* Sync History */}
      <Card className="p-6 shadow-card">
        <h2 className="text-lg font-semibold mb-4">Recent Sync Activity</h2>
        <div className="space-y-3">
          {[
            { time: "2 mins ago", action: "Auto-sync completed", records: 156, status: "success" },
            { time: "7 mins ago", action: "Manual sync triggered", records: 155, status: "success" },
            { time: "12 mins ago", action: "Auto-sync completed", records: 154, status: "success" },
            { time: "17 mins ago", action: "Auto-sync completed", records: 152, status: "success" },
          ].map((log, index) => (
            <div key={index} className="flex items-center gap-4 p-3 rounded-lg bg-muted/30">
              <div className="h-8 w-8 rounded-full bg-status-selected/10 flex items-center justify-center flex-shrink-0">
                <CheckCircle2 className="h-4 w-4 text-status-selected" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium">{log.action}</p>
                <p className="text-xs text-muted-foreground">{log.records} records synced</p>
              </div>
              <span className="text-xs text-muted-foreground">{log.time}</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default SheetsSync;
