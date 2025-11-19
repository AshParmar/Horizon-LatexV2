import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { TrendingUp, Users, Clock, Target, Award, Calendar } from "lucide-react";

const weeklyData = [
  { name: "Mon", applied: 24, shortlisted: 12, selected: 3 },
  { name: "Tue", applied: 32, shortlisted: 18, selected: 5 },
  { name: "Wed", applied: 28, shortlisted: 15, selected: 4 },
  { name: "Thu", applied: 35, shortlisted: 20, selected: 6 },
  { name: "Fri", applied: 30, shortlisted: 16, selected: 4 },
];

const sourceData = [
  { name: "Gmail", value: 102, color: "hsl(142, 71%, 45%)" },
  { name: "LinkedIn", value: 35, color: "hsl(217, 91%, 60%)" },
  { name: "Upload", value: 19, color: "hsl(262, 83%, 58%)" },
];

const skillsData = [
  { skill: "React", count: 45 },
  { skill: "Python", count: 38 },
  { skill: "Node.js", count: 32 },
  { skill: "TypeScript", count: 28 },
  { skill: "AWS", count: 25 },
];

const Reports = () => {
  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Reports & Insights</h1>
        <p className="text-muted-foreground">Analytics and metrics for your recruitment pipeline</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-6 shadow-card">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="h-5 w-5 text-primary" />
            <span className="text-xs text-status-selected">↑ 12%</span>
          </div>
          <p className="text-2xl font-bold">156</p>
          <p className="text-sm text-muted-foreground">Total Applications</p>
        </Card>
        <Card className="p-6 shadow-card">
          <div className="flex items-center justify-between mb-2">
            <Users className="h-5 w-5 text-accent" />
            <span className="text-xs text-status-selected">↑ 8%</span>
          </div>
          <p className="text-2xl font-bold">21.8%</p>
          <p className="text-sm text-muted-foreground">Selection Rate</p>
        </Card>
        <Card className="p-6 shadow-card">
          <div className="flex items-center justify-between mb-2">
            <Clock className="h-5 w-5 text-status-pending" />
            <span className="text-xs text-status-selected">↓ 15%</span>
          </div>
          <p className="text-2xl font-bold">4.2 days</p>
          <p className="text-sm text-muted-foreground">Avg. Time to Shortlist</p>
        </Card>
        <Card className="p-6 shadow-card">
          <div className="flex items-center justify-between mb-2">
            <Target className="h-5 w-5 text-status-review" />
            <span className="text-xs text-status-selected">↑ 20%</span>
          </div>
          <p className="text-2xl font-bold">85%</p>
          <p className="text-sm text-muted-foreground">AI Accuracy</p>
        </Card>
      </div>

      {/* Charts */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="grid w-full grid-cols-3 max-w-md">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="sources">Sources</TabsTrigger>
          <TabsTrigger value="skills">Skills</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <Card className="p-6 shadow-card">
            <h3 className="text-lg font-semibold mb-4">Weekly Hiring Funnel</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="applied"
                  stroke="hsl(142, 71%, 45%)"
                  strokeWidth={2}
                  name="Applied"
                />
                <Line
                  type="monotone"
                  dataKey="shortlisted"
                  stroke="hsl(262, 83%, 58%)"
                  strokeWidth={2}
                  name="Shortlisted"
                />
                <Line
                  type="monotone"
                  dataKey="selected"
                  stroke="hsl(217, 91%, 60%)"
                  strokeWidth={2}
                  name="Selected"
                />
              </LineChart>
            </ResponsiveContainer>
          </Card>

          <Card className="p-6 shadow-card">
            <h3 className="text-lg font-semibold mb-4">Conversion Metrics</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                />
                <Legend />
                <Bar dataKey="applied" fill="hsl(142, 71%, 45%)" name="Applied" />
                <Bar dataKey="shortlisted" fill="hsl(262, 83%, 58%)" name="Shortlisted" />
                <Bar dataKey="selected" fill="hsl(217, 91%, 60%)" name="Selected" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </TabsContent>

        <TabsContent value="sources" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <Card className="p-6 shadow-card">
              <h3 className="text-lg font-semibold mb-4">Candidate Sources</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={sourceData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {sourceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card>

            <Card className="p-6 shadow-card">
              <h3 className="text-lg font-semibold mb-4">Source Performance</h3>
              <div className="space-y-4">
                {sourceData.map((source) => (
                  <div key={source.name}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium">{source.name}</span>
                      <span className="text-sm text-muted-foreground">{source.value} candidates</span>
                    </div>
                    <div className="h-2 bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${(source.value / 156) * 100}%`,
                          backgroundColor: source.color,
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="skills" className="space-y-4">
          <Card className="p-6 shadow-card">
            <h3 className="text-lg font-semibold mb-4">Top Skills Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={skillsData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis type="number" stroke="hsl(var(--muted-foreground))" />
                <YAxis dataKey="skill" type="category" stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                />
                <Bar dataKey="count" fill="hsl(142, 71%, 45%)" />
              </BarChart>
            </ResponsiveContainer>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="p-6 shadow-card">
              <div className="flex items-center gap-3 mb-2">
                <Award className="h-5 w-5 text-primary" />
                <span className="font-semibold">Most Demanded</span>
              </div>
              <p className="text-2xl font-bold mb-1">React</p>
              <p className="text-sm text-muted-foreground">45 candidates</p>
            </Card>
            <Card className="p-6 shadow-card">
              <div className="flex items-center gap-3 mb-2">
                <TrendingUp className="h-5 w-5 text-accent" />
                <span className="font-semibold">Growing Trend</span>
              </div>
              <p className="text-2xl font-bold mb-1">TypeScript</p>
              <p className="text-sm text-muted-foreground">+25% this month</p>
            </Card>
            <Card className="p-6 shadow-card">
              <div className="flex items-center gap-3 mb-2">
                <Calendar className="h-5 w-5 text-status-review" />
                <span className="font-semibold">Rare Skills</span>
              </div>
              <p className="text-2xl font-bold mb-1">Rust</p>
              <p className="text-sm text-muted-foreground">Only 3 candidates</p>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Reports;
