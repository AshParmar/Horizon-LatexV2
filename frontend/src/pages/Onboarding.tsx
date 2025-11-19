import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";
import { CheckCircle, Mail, Sheet, Calendar, FileText, Upload, ArrowRight, ArrowLeft } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";

const steps = [
  { id: 1, title: "Connect Gmail", icon: Mail },
  { id: 2, title: "Connect Sheets", icon: Sheet },
  { id: 3, title: "Connect Calendar", icon: Calendar },
  { id: 4, title: "Add Job Description", icon: FileText },
];

const Onboarding = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [gmailConnected, setGmailConnected] = useState(false);
  const [sheetsConnected, setSheetsConnected] = useState(false);
  const [calendarConnected, setCalendarConnected] = useState(false);
  const [autoSync, setAutoSync] = useState(true);
  const [autoSchedule, setAutoSchedule] = useState(true);
  const [jobDescription, setJobDescription] = useState("");
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleNext = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1);
    } else {
      // Complete onboarding
      toast({
        title: "Setup Complete!",
        description: "Welcome to Horizon-LaTeX. Redirecting to dashboard...",
      });
      setTimeout(() => navigate("/dashboard"), 1500);
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return gmailConnected;
      case 2:
        return sheetsConnected;
      case 3:
        return calendarConnected;
      case 4:
        return jobDescription.trim().length > 0;
      default:
        return false;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-subtle flex items-center justify-center p-6">
      <Card className="w-full max-w-4xl shadow-card-hover">
        <div className="p-8">
          {/* Progress Indicator */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              {steps.map((step, index) => (
                <div key={step.id} className="flex items-center flex-1">
                  <div className="flex flex-col items-center flex-1">
                    <div
                      className={`w-10 h-10 rounded-full flex items-center justify-center transition-smooth ${
                        currentStep > step.id
                          ? "bg-primary text-primary-foreground"
                          : currentStep === step.id
                          ? "bg-primary text-primary-foreground animate-pulse-glow"
                          : "bg-muted text-muted-foreground"
                      }`}
                    >
                      {currentStep > step.id ? (
                        <CheckCircle className="h-5 w-5" />
                      ) : (
                        <step.icon className="h-5 w-5" />
                      )}
                    </div>
                    <span className="text-xs mt-2 font-medium">{step.title}</span>
                  </div>
                  {index < steps.length - 1 && (
                    <div className={`h-1 flex-1 mx-2 rounded ${
                      currentStep > step.id ? "bg-primary" : "bg-muted"
                    }`} />
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Step Content */}
          <div className="min-h-[400px]">
            {currentStep === 1 && (
              <div className="space-y-6 animate-fade-in-up">
                <div className="text-center mb-8">
                  <Mail className="h-16 w-16 text-primary mx-auto mb-4" />
                  <h2 className="text-3xl font-bold mb-2">Connect Gmail</h2>
                  <p className="text-muted-foreground">
                    Allow Horizon-LaTeX to fetch resumes from your email automatically
                  </p>
                </div>

                <Card className={`p-6 border-2 transition-smooth ${
                  gmailConnected ? "border-primary bg-primary/5" : "border-border"
                }`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Mail className="h-5 w-5 text-primary" />
                      <div>
                        <p className="font-medium">Gmail Integration</p>
                        <p className="text-sm text-muted-foreground">
                          Status: {gmailConnected ? "Connected" : "Not Connected"}
                        </p>
                      </div>
                    </div>
                    <Button
                      onClick={() => setGmailConnected(!gmailConnected)}
                      variant={gmailConnected ? "outline" : "default"}
                      className={gmailConnected ? "" : "gradient-primary"}
                    >
                      {gmailConnected ? "Disconnect" : "Connect Gmail"}
                    </Button>
                  </div>
                </Card>

                <div className="bg-muted/50 p-4 rounded-lg">
                  <p className="text-sm text-muted-foreground">
                    <strong>Note:</strong> We'll only access emails with resume attachments.
                    Your privacy is our priority.
                  </p>
                </div>
              </div>
            )}

            {currentStep === 2 && (
              <div className="space-y-6 animate-fade-in-up">
                <div className="text-center mb-8">
                  <Sheet className="h-16 w-16 text-primary mx-auto mb-4" />
                  <h2 className="text-3xl font-bold mb-2">Connect Google Sheets</h2>
                  <p className="text-muted-foreground">
                    Sync candidates to your Google Sheets automatically
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card className="p-6 border-2 border-border hover:border-primary transition-smooth">
                    <Sheet className="h-8 w-8 text-primary mb-3" />
                    <h3 className="font-semibold mb-2">All Candidates Sheet</h3>
                    <p className="text-sm text-muted-foreground mb-4">
                      Complete candidate database
                    </p>
                    <div className="space-y-2 text-xs text-muted-foreground">
                      <p>• Last synced: Never</p>
                      <p>• Records: 0</p>
                    </div>
                  </Card>

                  <Card className="p-6 border-2 border-border hover:border-primary transition-smooth">
                    <Sheet className="h-8 w-8 text-status-selected mb-3" />
                    <h3 className="font-semibold mb-2">Selected Candidates</h3>
                    <p className="text-sm text-muted-foreground mb-4">
                      Shortlisted candidates only
                    </p>
                    <div className="space-y-2 text-xs text-muted-foreground">
                      <p>• Last synced: Never</p>
                      <p>• Records: 0</p>
                    </div>
                  </Card>
                </div>

                <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Label htmlFor="auto-sync">Auto-sync every 5 minutes</Label>
                  </div>
                  <Switch id="auto-sync" checked={autoSync} onCheckedChange={setAutoSync} />
                </div>

                <Button
                  onClick={() => setSheetsConnected(true)}
                  className="w-full gradient-primary"
                  disabled={sheetsConnected}
                >
                  {sheetsConnected ? "Sheets Connected ✓" : "Connect Google Sheets"}
                </Button>
              </div>
            )}

            {currentStep === 3 && (
              <div className="space-y-6 animate-fade-in-up">
                <div className="text-center mb-8">
                  <Calendar className="h-16 w-16 text-primary mx-auto mb-4" />
                  <h2 className="text-3xl font-bold mb-2">Connect Google Calendar</h2>
                  <p className="text-muted-foreground">
                    Enable automatic interview scheduling
                  </p>
                </div>

                <Card className={`p-6 border-2 transition-smooth ${
                  calendarConnected ? "border-primary bg-primary/5" : "border-border"
                }`}>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <Calendar className="h-5 w-5 text-primary" />
                        <div>
                          <p className="font-medium">Calendar Integration</p>
                          <p className="text-sm text-muted-foreground">
                            Status: {calendarConnected ? "Connected" : "Not Connected"}
                          </p>
                        </div>
                      </div>
                      <Button
                        onClick={() => setCalendarConnected(!calendarConnected)}
                        variant={calendarConnected ? "outline" : "default"}
                        className={calendarConnected ? "" : "gradient-primary"}
                      >
                        {calendarConnected ? "Disconnect" : "Connect Calendar"}
                      </Button>
                    </div>

                    {calendarConnected && (
                      <div className="pt-4 border-t border-border">
                        <div className="flex items-center justify-between">
                          <div>
                            <Label htmlFor="auto-schedule">Auto-schedule interviews</Label>
                            <p className="text-xs text-muted-foreground mt-1">
                              Automatically find and book available slots
                            </p>
                          </div>
                          <Switch
                            id="auto-schedule"
                            checked={autoSchedule}
                            onCheckedChange={setAutoSchedule}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                </Card>

                <div className="bg-muted/50 p-4 rounded-lg">
                  <p className="text-sm font-medium mb-2">Available Features:</p>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Google Meet integration</li>
                    <li>• Automatic email invites</li>
                    <li>• Smart slot recommendations</li>
                  </ul>
                </div>
              </div>
            )}

            {currentStep === 4 && (
              <div className="space-y-6 animate-fade-in-up">
                <div className="text-center mb-8">
                  <FileText className="h-16 w-16 text-primary mx-auto mb-4" />
                  <h2 className="text-3xl font-bold mb-2">Add Job Description</h2>
                  <p className="text-muted-foreground">
                    Upload or paste your job description for AI matching
                  </p>
                </div>

                <div className="space-y-4">
                  <div className="flex gap-4">
                    <Button variant="outline" className="flex-1">
                      <Upload className="mr-2 h-4 w-4" />
                      Upload JD PDF
                    </Button>
                    <Button variant="outline" className="flex-1" disabled>
                      <FileText className="mr-2 h-4 w-4" />
                      Paste Text
                    </Button>
                  </div>

                  <Textarea
                    placeholder="Paste your job description here..."
                    className="min-h-[200px]"
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                  />

                  {jobDescription && (
                    <Card className="p-4 bg-primary/5 border-primary/20">
                      <p className="text-sm font-medium mb-1">AI Summary</p>
                      <p className="text-sm text-muted-foreground">
                        {jobDescription.length > 100
                          ? `${jobDescription.slice(0, 100)}...`
                          : jobDescription}
                      </p>
                    </Card>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Navigation Buttons */}
          <div className="flex items-center justify-between mt-8 pt-6 border-t border-border">
            <Button
              variant="outline"
              onClick={handleBack}
              disabled={currentStep === 1}
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>

            <Button
              onClick={handleNext}
              disabled={!canProceed()}
              className="gradient-primary"
            >
              {currentStep === 4 ? "Complete Setup" : "Next"}
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Onboarding;
