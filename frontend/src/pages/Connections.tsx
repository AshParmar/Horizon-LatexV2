import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle, Mail, Sheet, Calendar, Plug } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const Connections = () => {
  const [setupSteps, setSetupSteps] = useState({
    gmail: false,
    sheets: false,
    calendar: false,
  });
  
  const { toast } = useToast();

  const handleConnect = (service: 'gmail' | 'sheets' | 'calendar') => {
    setSetupSteps({ ...setupSteps, [service]: !setupSteps[service] });
    
    if (!setupSteps[service]) {
      toast({
        title: `${service.charAt(0).toUpperCase() + service.slice(1)} Connected`,
        description: `Successfully connected to ${service}`,
      });
    }
  };

  return (
    <div className="p-8 space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2 flex items-center gap-3">
          <Plug className="h-8 w-8 text-primary" />
          Connections
        </h1>
        <p className="text-muted-foreground">
          Connect your tools to unlock the full power of AI-driven recruitment
        </p>
      </div>

      {/* Connection Status Overview */}
      <Card className="p-6 bg-gradient-to-r from-primary/10 via-accent/10 to-primary/10 border-primary/20">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold mb-1">Integration Status</h3>
            <p className="text-sm text-muted-foreground">
              {Object.values(setupSteps).filter(Boolean).length} of 3 integrations connected
            </p>
          </div>
          <div className="flex items-center gap-2">
            <div className={`h-3 w-3 rounded-full ${
              Object.values(setupSteps).every(Boolean) 
                ? 'bg-green-500 animate-pulse' 
                : 'bg-yellow-500'
            }`} />
            <span className="text-sm font-medium">
              {Object.values(setupSteps).every(Boolean) ? 'All Connected' : 'Setup Incomplete'}
            </span>
          </div>
        </div>
      </Card>

      {/* Connection Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Gmail Connection */}
        <Card className="p-6 hover-scale shadow-card transition-smooth">
          <div className="flex flex-col h-full">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
              setupSteps.gmail ? 'bg-green-500/20' : 'bg-primary/20'
            }`}>
              {setupSteps.gmail ? (
                <CheckCircle className="h-6 w-6 text-green-500" />
              ) : (
                <Mail className="h-6 w-6 text-primary" />
              )}
            </div>
            
            <h3 className="text-lg font-semibold mb-2">Gmail Integration</h3>
            <p className="text-sm text-muted-foreground mb-4 flex-1">
              Automatically capture and process resumes from your Gmail inbox. AI will extract candidate information and add them to your pipeline.
            </p>
            
            <div className="space-y-3">
              {setupSteps.gmail && (
                <div className="p-3 bg-muted/50 rounded-lg text-xs space-y-1 animate-fade-in">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Status:</span>
                    <span className="text-green-500 font-medium">Active</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Last Sync:</span>
                    <span className="font-medium">2 mins ago</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Resumes Captured:</span>
                    <span className="font-medium">102</span>
                  </div>
                </div>
              )}
              
              <Button
                onClick={() => handleConnect('gmail')}
                variant={setupSteps.gmail ? "outline" : "default"}
                className="w-full"
              >
                {setupSteps.gmail ? "Disconnect" : "Connect Gmail"}
              </Button>
            </div>
          </div>
        </Card>

        {/* Google Sheets Connection */}
        <Card className="p-6 hover-scale shadow-card transition-smooth">
          <div className="flex flex-col h-full">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
              setupSteps.sheets ? 'bg-green-500/20' : 'bg-primary/20'
            }`}>
              {setupSteps.sheets ? (
                <CheckCircle className="h-6 w-6 text-green-500" />
              ) : (
                <Sheet className="h-6 w-6 text-primary" />
              )}
            </div>
            
            <h3 className="text-lg font-semibold mb-2">Google Sheets Sync</h3>
            <p className="text-sm text-muted-foreground mb-4 flex-1">
              Sync candidate data in real-time with Google Sheets. Maintain a live spreadsheet with all candidate information and status updates.
            </p>
            
            <div className="space-y-3">
              {setupSteps.sheets && (
                <div className="p-3 bg-muted/50 rounded-lg text-xs space-y-1 animate-fade-in">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Status:</span>
                    <span className="text-green-500 font-medium">Syncing</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Last Sync:</span>
                    <span className="font-medium">Just now</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Records Synced:</span>
                    <span className="font-medium">156</span>
                  </div>
                </div>
              )}
              
              <Button
                onClick={() => handleConnect('sheets')}
                variant={setupSteps.sheets ? "outline" : "default"}
                className="w-full"
              >
                {setupSteps.sheets ? "Disconnect" : "Connect Sheets"}
              </Button>
            </div>
          </div>
        </Card>

        {/* Google Calendar Connection */}
        <Card className="p-6 hover-scale shadow-card transition-smooth">
          <div className="flex flex-col h-full">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
              setupSteps.calendar ? 'bg-green-500/20' : 'bg-primary/20'
            }`}>
              {setupSteps.calendar ? (
                <CheckCircle className="h-6 w-6 text-green-500" />
              ) : (
                <Calendar className="h-6 w-6 text-primary" />
              )}
            </div>
            
            <h3 className="text-lg font-semibold mb-2">Calendar Integration</h3>
            <p className="text-sm text-muted-foreground mb-4 flex-1">
              Automatically schedule interviews and send calendar invites. AI will find optimal time slots and create Google Meet links.
            </p>
            
            <div className="space-y-3">
              {setupSteps.calendar && (
                <div className="p-3 bg-muted/50 rounded-lg text-xs space-y-1 animate-fade-in">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Status:</span>
                    <span className="text-green-500 font-medium">Connected</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Interviews Scheduled:</span>
                    <span className="font-medium">18</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Upcoming:</span>
                    <span className="font-medium">5 this week</span>
                  </div>
                </div>
              )}
              
              <Button
                onClick={() => handleConnect('calendar')}
                variant={setupSteps.calendar ? "outline" : "default"}
                className="w-full"
              >
                {setupSteps.calendar ? "Disconnect" : "Connect Calendar"}
              </Button>
            </div>
          </div>
        </Card>
      </div>

      {/* Help Section */}
      <Card className="p-6 bg-card">
        <h3 className="text-lg font-semibold mb-2">Need Help?</h3>
        <p className="text-sm text-muted-foreground mb-4">
          Learn more about setting up integrations and maximizing your recruitment automation.
        </p>
        <div className="flex gap-3">
          <Button variant="outline" size="sm">
            View Documentation
          </Button>
          <Button variant="outline" size="sm">
            Contact Support
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default Connections;
