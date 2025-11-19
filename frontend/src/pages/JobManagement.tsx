import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Plus, Briefcase, Users, Calendar, Edit, Trash2, CheckCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Job {
  id: string;
  title: string;
  department: string;
  status: "active" | "closed";
  candidates: number;
  created: string;
  description: string;
}

const mockJobs: Job[] = [
  {
    id: "1",
    title: "Senior Frontend Developer",
    department: "Engineering",
    status: "active",
    candidates: 24,
    created: "2024-01-15",
    description: "Looking for an experienced frontend developer...",
  },
  {
    id: "2",
    title: "Product Manager",
    department: "Product",
    status: "active",
    candidates: 12,
    created: "2024-01-20",
    description: "Seeking a strategic product manager...",
  },
  {
    id: "3",
    title: "Data Scientist",
    department: "Data",
    status: "closed",
    candidates: 8,
    created: "2024-01-10",
    description: "Looking for a data scientist with ML experience...",
  },
];

const JobManagement = () => {
  const [jobs] = useState<Job[]>(mockJobs);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const { toast } = useToast();

  const handleAddJob = () => {
    toast({
      title: "Job Added",
      description: "New job posting created successfully",
    });
    setIsDialogOpen(false);
  };

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Job Management</h1>
          <p className="text-muted-foreground">Manage your open positions and candidates</p>
        </div>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button className="gradient-primary shadow-soft">
              <Plus className="mr-2 h-4 w-4" />
              Add New Job
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>Create New Job Posting</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Job Title</label>
                <Input placeholder="e.g., Senior Software Engineer" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Department</label>
                <Input placeholder="e.g., Engineering" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Job Description</label>
                <Textarea placeholder="Describe the role, requirements, and responsibilities..." rows={6} />
              </div>
              <Button onClick={handleAddJob} className="w-full gradient-primary">
                Create Job
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-6 shadow-card">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
              <Briefcase className="h-6 w-6 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold">{jobs.filter(j => j.status === "active").length}</p>
              <p className="text-sm text-muted-foreground">Active Jobs</p>
            </div>
          </div>
        </Card>
        <Card className="p-6 shadow-card">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center">
              <Users className="h-6 w-6 text-accent" />
            </div>
            <div>
              <p className="text-2xl font-bold">{jobs.reduce((acc, j) => acc + j.candidates, 0)}</p>
              <p className="text-sm text-muted-foreground">Total Candidates</p>
            </div>
          </div>
        </Card>
        <Card className="p-6 shadow-card">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg bg-status-selected/10 flex items-center justify-center">
              <CheckCircle className="h-6 w-6 text-status-selected" />
            </div>
            <div>
              <p className="text-2xl font-bold">{jobs.filter(j => j.status === "closed").length}</p>
              <p className="text-sm text-muted-foreground">Filled Positions</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Jobs List */}
      <div className="space-y-4">
        {jobs.map((job) => (
          <Card key={job.id} className="shadow-card hover:shadow-card-hover transition-smooth">
            <div className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-semibold">{job.title}</h3>
                    <Badge
                      variant={job.status === "active" ? "default" : "secondary"}
                      className={job.status === "active" ? "bg-primary" : ""}
                    >
                      {job.status}
                    </Badge>
                  </div>
                  <p className="text-muted-foreground mb-4">{job.description}</p>
                  <div className="flex items-center gap-6 text-sm text-muted-foreground">
                    <div className="flex items-center gap-2">
                      <Briefcase className="h-4 w-4" />
                      <span>{job.department}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Users className="h-4 w-4" />
                      <span>{job.candidates} candidates</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4" />
                      <span>Posted {new Date(job.created).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="icon">
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon">
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default JobManagement;
