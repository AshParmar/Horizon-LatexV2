import { LayoutDashboard, Users, Calendar, FileSpreadsheet, Briefcase, BarChart3, Settings as SettingsIcon, Sparkles, Plug } from "lucide-react";
import { NavLink } from "@/components/NavLink";
import { ThemeToggle } from "./ThemeToggle";

const navigation = [
  { name: "Dashboard", to: "/dashboard", icon: LayoutDashboard },
  { name: "Connections", to: "/connections", icon: Plug },
  { name: "Candidates", to: "/candidates", icon: Users },
  { name: "Jobs", to: "/jobs", icon: Briefcase },
  { name: "Scheduling", to: "/scheduling", icon: Calendar },
  { name: "Reports", to: "/reports", icon: BarChart3 },
  { name: "Sheets Sync", to: "/sheets-sync", icon: FileSpreadsheet },
  { name: "Settings", to: "/settings", icon: SettingsIcon },
];

export const Sidebar = () => {
  return (
    <aside className="w-64 bg-card border-r border-border h-screen sticky top-0 flex flex-col">
      <div className="p-6 border-b border-border flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            Horizon-LaTeX
          </h1>
          <p className="text-xs text-muted-foreground mt-1">Gemini Edition</p>
        </div>
        <ThemeToggle />
      </div>
      
      <nav className="flex-1 p-4 space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.to}
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium hover:bg-muted transition-smooth"
            activeClassName="bg-primary text-primary-foreground hover:bg-primary"
          >
            <item.icon className="h-4 w-4" />
            {item.name}
          </NavLink>
        ))}
      </nav>
      
      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
            <span className="text-sm font-medium text-primary">HR</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">HR Manager</p>
            <p className="text-xs text-muted-foreground truncate">hr@horizon.ai</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
