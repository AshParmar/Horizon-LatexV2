import { StatsCard } from "@/components/StatsCard";
import { GoogleSheetTile } from "@/components/GoogleSheetTile";
import { PipelineVisualization } from "@/components/PipelineVisualization";
import { StatusBadge, CandidateStatus } from "@/components/StatusBadge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Users, CheckCircle, XCircle, Clock, Mail, Upload } from "lucide-react";
import { useNavigate } from "react-router-dom";

const mockCandidates = [
  {
    id: "1",
    name: "Sarah Johnson",
    email: "sarah.j@email.com",
    score: 92,
    status: "selected" as CandidateStatus,
    source: "Gmail",
    avatar: "SJ",
  },
  {
    id: "2",
    name: "Michael Chen",
    email: "m.chen@email.com",
    score: 45,
    status: "auto-rejected" as CandidateStatus,
    source: "Upload",
    avatar: "MC",
  },
  {
    id: "3",
    name: "Emily Rodriguez",
    email: "emily.r@email.com",
    score: 78,
    status: "pending" as CandidateStatus,
    source: "LinkedIn",
    avatar: "ER",
  },
  {
    id: "4",
    name: "David Kim",
    email: "d.kim@email.com",
    score: 88,
    status: "needs-review" as CandidateStatus,
    source: "Gmail",
    avatar: "DK",
  },
];

const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">Recruitment Dashboard</h1>
        <p className="text-muted-foreground">Overview of your hiring pipeline</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Total Candidates"
          value={156}
          icon={Users}
          trend={{ value: "+12% this week", positive: true }}
        />
        <StatsCard
          title="Selected"
          value={34}
          icon={CheckCircle}
          description="21.8% selection rate"
        />
        <StatsCard
          title="Rejected"
          value={89}
          icon={XCircle}
          description="57.1% rejection rate"
        />
        <StatsCard
          title="Pending Review"
          value={33}
          icon={Clock}
          description="21.1% awaiting decision"
        />
      </div>

      {/* Auto-processed Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <StatsCard
          title="Auto-processed via Gmail"
          value={102}
          icon={Mail}
          description="65.4% of total"
        />
        <StatsCard
          title="Manual Uploads"
          value={54}
          icon={Upload}
          description="34.6% of total"
        />
      </div>

      {/* Google Sheets Integration */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Google Sheets Integration</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <GoogleSheetTile
            title="All Candidates Sheet"
            sheetUrl="https://docs.google.com/spreadsheets"
            lastSynced="2 mins ago"
            autoSync={true}
            recordCount={156}
          />
          <GoogleSheetTile
            title="Selected Candidates Sheet"
            sheetUrl="https://docs.google.com/spreadsheets"
            lastSynced="2 mins ago"
            autoSync={true}
            recordCount={34}
          />
        </div>
      </div>

      {/* Pipeline Visualization */}
      <PipelineVisualization />

      {/* Candidate Table */}
      <Card className="shadow-card">
        <div className="p-6 border-b border-border">
          <h2 className="text-xl font-semibold">Recent Candidates</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted/50">
              <tr>
                <th className="text-left p-4 text-sm font-medium text-muted-foreground">Candidate</th>
                <th className="text-left p-4 text-sm font-medium text-muted-foreground">Score</th>
                <th className="text-left p-4 text-sm font-medium text-muted-foreground">Status</th>
                <th className="text-left p-4 text-sm font-medium text-muted-foreground">Source</th>
                <th className="text-left p-4 text-sm font-medium text-muted-foreground">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {mockCandidates.map((candidate) => (
                <tr key={candidate.id} className="hover:bg-muted/50 transition-colors">
                  <td className="p-4">
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                        <span className="text-sm font-medium text-primary">{candidate.avatar}</span>
                      </div>
                      <div>
                        <p className="font-medium text-foreground">{candidate.name}</p>
                        <p className="text-sm text-muted-foreground">{candidate.email}</p>
                      </div>
                    </div>
                  </td>
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden max-w-[100px]">
                        <div 
                          className="h-full bg-primary rounded-full"
                          style={{ width: `${candidate.score}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium">{candidate.score}</span>
                    </div>
                  </td>
                  <td className="p-4">
                    <StatusBadge status={candidate.status} />
                  </td>
                  <td className="p-4">
                    <span className="text-sm text-muted-foreground">{candidate.source}</span>
                  </td>
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => navigate(`/candidate/${candidate.id}`)}
                      >
                        View Profile
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="sm"
                        onClick={() => window.open("https://docs.google.com/spreadsheets", "_blank")}
                      >
                        Open Sheet
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;
