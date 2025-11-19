import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { StatusBadge } from "@/components/StatusBadge";
import { 
  ArrowLeft, Mail, Phone, MapPin, Briefcase, GraduationCap, 
  Code, Github, Linkedin, Globe, CheckCircle, XCircle, AlertCircle 
} from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

const CandidateProfile = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { toast } = useToast();
  const [status, setStatus] = useState<"auto-selected" | "selected" | "rejected" | "needs-review">("auto-selected");

  const handleOverride = (newStatus: typeof status) => {
    setStatus(newStatus);
    toast({
      title: "Decision Updated",
      description: `Candidate status changed to ${newStatus.replace("-", " ")}. Changes synced to Google Sheets.`,
    });
  };

  return (
    <div className="p-8 space-y-6">
      <Button 
        variant="ghost" 
        onClick={() => navigate("/dashboard")}
        className="gap-2"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Dashboard
      </Button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Panel - Candidate Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Header */}
          <Card className="p-6 shadow-card">
            <div className="flex items-start gap-6">
              <div className="h-24 w-24 rounded-2xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                <span className="text-3xl font-bold text-primary">SJ</span>
              </div>
              <div className="flex-1">
                <h1 className="text-2xl font-bold mb-2">Sarah Johnson</h1>
                <div className="flex flex-wrap gap-4 text-sm text-muted-foreground mb-4">
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4" />
                    sarah.j@email.com
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone className="h-4 w-4" />
                    +1 (555) 123-4567
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="h-4 w-4" />
                    San Francisco, CA
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  <Button variant="outline" size="sm" className="gap-2">
                    <Linkedin className="h-4 w-4" />
                    LinkedIn
                  </Button>
                  <Button variant="outline" size="sm" className="gap-2">
                    <Github className="h-4 w-4" />
                    GitHub
                  </Button>
                  <Button variant="outline" size="sm" className="gap-2">
                    <Globe className="h-4 w-4" />
                    Portfolio
                  </Button>
                </div>
              </div>
            </div>
          </Card>

          {/* Skills */}
          <Card className="p-6 shadow-card">
            <div className="flex items-center gap-2 mb-4">
              <Code className="h-5 w-5 text-primary" />
              <h2 className="text-lg font-semibold">Skills</h2>
            </div>
            <div className="flex flex-wrap gap-2">
              {["React", "TypeScript", "Node.js", "Python", "AWS", "Docker", "GraphQL", "PostgreSQL"].map((skill) => (
                <Badge key={skill} variant="secondary" className="px-3 py-1">
                  {skill}
                </Badge>
              ))}
            </div>
          </Card>

          {/* Experience */}
          <Card className="p-6 shadow-card">
            <div className="flex items-center gap-2 mb-4">
              <Briefcase className="h-5 w-5 text-primary" />
              <h2 className="text-lg font-semibold">Experience</h2>
            </div>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold">Senior Software Engineer</h3>
                <p className="text-sm text-muted-foreground">TechCorp Inc. • 2021 - Present</p>
                <p className="text-sm mt-2">Led development of microservices architecture serving 1M+ users. Reduced API latency by 40% through optimization.</p>
              </div>
              <div>
                <h3 className="font-semibold">Full Stack Developer</h3>
                <p className="text-sm text-muted-foreground">StartupXYZ • 2019 - 2021</p>
                <p className="text-sm mt-2">Built customer-facing web applications using React and Node.js. Implemented CI/CD pipelines.</p>
              </div>
            </div>
          </Card>

          {/* Education */}
          <Card className="p-6 shadow-card">
            <div className="flex items-center gap-2 mb-4">
              <GraduationCap className="h-5 w-5 text-primary" />
              <h2 className="text-lg font-semibold">Education</h2>
            </div>
            <div>
              <h3 className="font-semibold">Master of Science in Computer Science</h3>
              <p className="text-sm text-muted-foreground">Stanford University • 2017 - 2019</p>
            </div>
          </Card>

          {/* Resume Preview */}
          <Card className="p-6 shadow-card">
            <h2 className="text-lg font-semibold mb-4">Resume</h2>
            <div className="border border-border rounded-lg bg-muted/30 h-96 flex items-center justify-center">
              <div className="text-center text-muted-foreground">
                <p className="mb-2">PDF Resume Preview</p>
                <Button variant="outline" size="sm">Download Resume</Button>
              </div>
            </div>
          </Card>
        </div>

        {/* Right Panel - AI Evaluation & Decision */}
        <div className="space-y-6">
          {/* AI Evaluation */}
          <Card className="p-6 shadow-card">
            <div className="flex items-center gap-2 mb-4">
              <div className="h-8 w-8 rounded-lg bg-primary/10 flex items-center justify-center">
                <span className="text-lg">✨</span>
              </div>
              <h2 className="text-lg font-semibold">AI Agent Evaluation</h2>
            </div>

            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">JD Matching</span>
                  <span className="text-sm font-bold text-primary">92%</span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-primary rounded-full" style={{ width: "92%" }} />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Hard Skills</span>
                  <span className="text-sm font-bold text-primary">88%</span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-primary rounded-full" style={{ width: "88%" }} />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Soft Skills</span>
                  <span className="text-sm font-bold text-primary">85%</span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-primary rounded-full" style={{ width: "85%" }} />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Keyword Match</span>
                  <span className="text-sm font-bold text-primary">94%</span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-primary rounded-full" style={{ width: "94%" }} />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Cultural Fit</span>
                  <span className="text-sm font-bold text-primary">79%</span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-primary rounded-full" style={{ width: "79%" }} />
                </div>
              </div>
            </div>
          </Card>

          {/* Current Status */}
          <Card className="p-6 shadow-card">
            <h2 className="text-lg font-semibold mb-4">Current Status</h2>
            <StatusBadge status={status} className="w-full justify-center text-sm py-2" />
          </Card>

          {/* Decision Box */}
          <Card className="p-6 shadow-card border-2 border-primary/20">
            <h2 className="text-lg font-semibold mb-2">Gemini Recommendation</h2>
            <p className="text-sm text-muted-foreground mb-4">
              Based on AI analysis, this candidate is recommended for selection with 92% confidence.
            </p>

            <div className="space-y-2">
              <Button 
                className="w-full gap-2" 
                size="lg"
                onClick={() => handleOverride("selected")}
              >
                <CheckCircle className="h-4 w-4" />
                Override → Select
              </Button>
              <Button 
                variant="destructive" 
                className="w-full gap-2"
                onClick={() => handleOverride("rejected")}
              >
                <XCircle className="h-4 w-4" />
                Override → Reject
              </Button>
              <Button 
                variant="outline" 
                className="w-full gap-2"
                onClick={() => handleOverride("needs-review")}
              >
                <AlertCircle className="h-4 w-4" />
                Mark as Needs Review
              </Button>
            </div>
          </Card>

          {/* Quick Actions */}
          <Card className="p-6 shadow-card">
            <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-2">
              <Button variant="outline" className="w-full" onClick={() => navigate("/scheduling")}>
                Schedule Interview
              </Button>
              <Button variant="outline" className="w-full">
                Send Email
              </Button>
              <Button variant="outline" className="w-full" onClick={() => window.open("https://docs.google.com/spreadsheets", "_blank")}>
                View in Sheet
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default CandidateProfile;
