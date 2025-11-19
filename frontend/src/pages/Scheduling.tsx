import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Calendar as CalendarIcon, Clock, Video } from "lucide-react";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

const Scheduling = () => {
  const [date, setDate] = useState<Date | undefined>(new Date());
  const { toast } = useToast();

  const timeSlots = [
    "09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM", 
    "02:00 PM", "03:00 PM", "04:00 PM"
  ];

  const handleSchedule = (time: string) => {
    toast({
      title: "Interview Scheduled",
      description: `Google Meet created and invitation sent for ${date?.toLocaleDateString()} at ${time}`,
    });
  };

  return (
    <div className="p-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">Interview Scheduling</h1>
        <p className="text-muted-foreground">Schedule interviews and send calendar invites</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendar */}
        <Card className="p-6 shadow-card lg:col-span-2">
          <div className="flex items-center gap-2 mb-6">
            <CalendarIcon className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-semibold">Select Date</h2>
          </div>
          <Calendar
            mode="single"
            selected={date}
            onSelect={setDate}
            className="rounded-md border"
          />
        </Card>

        {/* Candidate Info */}
        <Card className="p-6 shadow-card">
          <h2 className="text-lg font-semibold mb-4">Candidate</h2>
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center">
                <span className="font-medium text-primary">SJ</span>
              </div>
              <div>
                <p className="font-medium">Sarah Johnson</p>
                <p className="text-sm text-muted-foreground">sarah.j@email.com</p>
              </div>
            </div>
            <div className="pt-4 border-t border-border">
              <p className="text-sm text-muted-foreground mb-2">Interview Type</p>
              <p className="font-medium">Technical Interview - Round 1</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground mb-2">Duration</p>
              <p className="font-medium">60 minutes</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Time Slots */}
      <Card className="p-6 shadow-card">
        <div className="flex items-center gap-2 mb-6">
          <Clock className="h-5 w-5 text-primary" />
          <h2 className="text-lg font-semibold">Available Time Slots</h2>
          <span className="ml-auto text-sm text-muted-foreground">
            {date?.toLocaleDateString()}
          </span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
          {timeSlots.map((time, index) => (
            <Button
              key={time}
              variant={index === 2 ? "default" : "outline"}
              className="flex flex-col h-auto py-4"
              onClick={() => handleSchedule(time)}
            >
              <Clock className="h-4 w-4 mb-1" />
              <span className="text-sm">{time}</span>
              {index === 2 && (
                <span className="text-xs mt-1 opacity-80">✨ AI Recommended</span>
              )}
            </Button>
          ))}
        </div>
      </Card>

      {/* Actions */}
      <Card className="p-6 shadow-card">
        <h2 className="text-lg font-semibold mb-4">Actions</h2>
        <div className="flex flex-wrap gap-3">
          <Button size="lg" className="gap-2">
            <Video className="h-4 w-4" />
            Create Google Meet + Send Mail
          </Button>
          <Button variant="outline" size="lg">
            Send Custom Invitation
          </Button>
          <Button variant="outline" size="lg">
            Add to Calendar Only
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default Scheduling;
