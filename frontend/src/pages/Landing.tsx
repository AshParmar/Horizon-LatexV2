import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useNavigate } from "react-router-dom";
import {
  Brain,
  Workflow,
  Mail,
  Sheet,
  Linkedin,
  Target,
  Calendar,
  BarChart3,
  UserCheck,
  ArrowRight,
  CheckCircle,
  Sparkles,
  Zap,
  Shield,
} from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "Gemini Candidate Scoring",
    description: "AI-powered evaluation with precision matching",
  },
  {
    icon: Workflow,
    title: "Multi-Agent Pipeline",
    description: "Automated workflow from screening to scheduling",
  },
  {
    icon: Mail,
    title: "Automated Gmail Capture",
    description: "Instantly process resumes from email",
  },
  {
    icon: Sheet,
    title: "Google Sheets Sync",
    description: "Real-time synchronization with your sheets",
  },
  {
    icon: Linkedin,
    title: "LinkedIn Enrichment",
    description: "Auto-fetch candidate profiles and insights",
  },
  {
    icon: Target,
    title: "AI JD Matching",
    description: "Smart job description alignment",
  },
  {
    icon: Calendar,
    title: "One-click Scheduling",
    description: "Automated interview calendar management",
  },
  {
    icon: BarChart3,
    title: "Analytics Dashboard",
    description: "Deep insights into your hiring pipeline",
  },
  {
    icon: UserCheck,
    title: "Human-in-the-Loop",
    description: "Full control with AI recommendations",
  },
];

const testimonials = [
  {
    quote: "Horizon-LaTeX helped us process 10x more candidates without increasing our team size.",
    author: "Sarah Johnson",
    role: "Head of Talent, TechCorp",
    avatar: "SJ",
  },
  {
    quote: "The AI scoring is remarkably accurate. We've reduced time-to-hire by 60%.",
    author: "Michael Chen",
    role: "HR Director, Innovation Labs",
    avatar: "MC",
  },
  {
    quote: "Finally, a recruitment tool that keeps humans in control while leveraging AI power.",
    author: "Emily Rodriguez",
    role: "Talent Manager, StartupHub",
    avatar: "ER",
  },
];

const Landing = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-subtle">
      {/* Header */}
      <header className="fixed top-0 w-full z-50 glass-strong border-b border-border">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold">Horizon-LaTeX</span>
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <Button variant="ghost" onClick={() => navigate("/login")}>
              Sign In
            </Button>
            <Button onClick={() => navigate("/login")} className="gradient-primary">
              Get Started
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="container mx-auto text-center max-w-5xl">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary mb-6 animate-fade-in-up">
            <Zap className="h-4 w-4" />
            <span className="text-sm font-medium">Powered by Gemini & Agentic AI</span>
          </div>
          
          <h1 className="text-6xl md:text-7xl font-bold mb-6 animate-fade-in-up" style={{ animationDelay: "0.1s" }}>
            AI-Powered Recruitment with{" "}
            <span 
              className="inline-block gradient-primary" 
              style={{
                WebkitBackgroundClip: 'text',
                backgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                color: 'transparent'
              }}
            >
              Gemini
            </span>
          </h1>
          
          <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
            Automate resume screening, candidate evaluation, and scheduling—while keeping humans in control.
          </p>

          <div className="flex items-center justify-center gap-4 animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
            <Button size="lg" onClick={() => navigate("/login")} className="gradient-primary shadow-lg hover-lift">
              Get Started
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="shadow-soft">
              View Demo
            </Button>
          </div>

          {/* Hero Illustration Placeholder */}
          <div className="mt-16 relative">
            <Card className="shadow-card-hover glass overflow-hidden animate-float">
              <div className="p-12 flex items-center justify-center gap-8 flex-wrap">
                <div className="flex flex-col items-center gap-2">
                  <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center">
                    <Brain className="h-8 w-8 text-primary" />
                  </div>
                  <span className="text-sm font-medium">AI Agents</span>
                </div>
                <ArrowRight className="h-6 w-6 text-muted-foreground" />
                <div className="flex flex-col items-center gap-2">
                  <div className="w-16 h-16 rounded-full bg-accent/20 flex items-center justify-center">
                    <Sheet className="h-8 w-8 text-accent" />
                  </div>
                  <span className="text-sm font-medium">Sheets Sync</span>
                </div>
                <ArrowRight className="h-6 w-6 text-muted-foreground" />
                <div className="flex flex-col items-center gap-2">
                  <div className="w-16 h-16 rounded-full bg-status-selected/20 flex items-center justify-center">
                    <BarChart3 className="h-8 w-8 text-status-selected" />
                  </div>
                  <span className="text-sm font-medium">Analytics</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 bg-card">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Everything You Need to Scale Hiring</h2>
            <p className="text-muted-foreground text-lg">Powerful features built for modern recruitment teams</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <Card
                key={index}
                className="p-6 shadow-card hover:shadow-card-hover transition-smooth hover-lift"
              >
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <feature.icon className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Animated Pipeline Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Intelligent Multi-Agent Pipeline</h2>
            <p className="text-muted-foreground text-lg">
              Watch your hiring workflow transform with AI-powered automation
            </p>
          </div>

          <Card className="shadow-card p-8">
            <div className="flex items-center justify-between gap-4 overflow-x-auto">
              {[
                { icon: Mail, label: "Gmail", color: "text-blue-500" },
                { icon: Workflow, label: "Parsing", color: "text-purple-500" },
                { icon: Brain, label: "Scoring", color: "text-primary" },
                { icon: Target, label: "Decision", color: "text-accent" },
                { icon: Sheet, label: "Sync", color: "text-green-500" },
                { icon: UserCheck, label: "Review", color: "text-orange-500" },
              ].map((step, index) => (
                <div key={index} className="flex items-center gap-4">
                  <div className="flex flex-col items-center gap-2 min-w-[100px]">
                    <div className={`w-14 h-14 rounded-full bg-card border-2 border-border flex items-center justify-center shadow-soft ${step.color}`}>
                      <step.icon className="h-7 w-7" />
                    </div>
                    <span className="text-sm font-medium text-center">{step.label}</span>
                  </div>
                  {index < 5 && <ArrowRight className="h-5 w-5 text-muted-foreground flex-shrink-0" />}
                </div>
              ))}
            </div>
          </Card>
        </div>
      </section>

      {/* About Section */}
      <section className="py-20 px-6 bg-card">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-4xl font-bold mb-6">Built for Modern Recruiters</h2>
          <p className="text-lg text-muted-foreground mb-8">
            Horizon-LaTeX helps recruiters handle 10× more candidates with AI-backed precision,
            while ensuring transparency, oversight, and fairness in every decision.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            <div className="flex flex-col items-center gap-3">
              <div className="w-16 h-16 rounded-full gradient-primary flex items-center justify-center">
                <Shield className="h-8 w-8 text-white" />
              </div>
              <h3 className="font-semibold">Transparent</h3>
              <p className="text-sm text-muted-foreground">Full visibility into AI decisions</p>
            </div>
            <div className="flex flex-col items-center gap-3">
              <div className="w-16 h-16 rounded-full gradient-accent flex items-center justify-center">
                <Zap className="h-8 w-8 text-white" />
              </div>
              <h3 className="font-semibold">Efficient</h3>
              <p className="text-sm text-muted-foreground">10x productivity gains</p>
            </div>
            <div className="flex flex-col items-center gap-3">
              <div className="w-16 h-16 rounded-full bg-status-selected flex items-center justify-center">
                <CheckCircle className="h-8 w-8 text-white" />
              </div>
              <h3 className="font-semibold">Reliable</h3>
              <p className="text-sm text-muted-foreground">Human oversight at every step</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Loved by Hiring Teams</h2>
            <p className="text-muted-foreground text-lg">See what our customers have to say</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="p-6 shadow-card hover:shadow-card-hover transition-smooth">
                <p className="text-muted-foreground mb-4 italic">"{testimonial.quote}"</p>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
                    <span className="text-sm font-medium text-primary">{testimonial.avatar}</span>
                  </div>
                  <div>
                    <p className="font-semibold text-sm">{testimonial.author}</p>
                    <p className="text-xs text-muted-foreground">{testimonial.role}</p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-border bg-card">
        <div className="container mx-auto max-w-7xl">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="h-5 w-5 text-primary" />
                <span className="font-bold">Horizon-LaTeX</span>
              </div>
              <p className="text-sm text-muted-foreground">
                AI-powered recruitment automation for modern teams.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Demo</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">About</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Careers</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-3">Legal</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Privacy</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Terms</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Security</a></li>
              </ul>
            </div>
          </div>
          <div className="pt-8 border-t border-border flex items-center justify-between">
            <p className="text-sm text-muted-foreground">
              © 2024 Horizon-LaTeX. All rights reserved.
            </p>
            <ThemeToggle />
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
