# Scheduled Tasks / Cron Jobs Guide

## 📅 Overview

This backend uses **APScheduler** for scheduled background tasks (cron jobs).

## 📁 Location

All cron jobs are defined in:
```
backend/tasks/scheduler.py
```

## 🚀 How It Works

1. **Task Scheduler** (`TaskScheduler` class) manages all scheduled jobs
2. **Automatically starts** when FastAPI app starts
3. **Automatically stops** when app shuts down
4. **Runs in background** without blocking API requests

## ⏰ Pre-configured Tasks

| Task | Schedule | Purpose |
|------|----------|---------|
| `daily_resume_enrichment` | Daily at 9 AM | Enrich pending resumes with LinkedIn/GitHub data |
| `check_pending_interviews` | Every hour | Send reminders for upcoming interviews |
| `weekly_analytics_report` | Monday at 8 AM | Generate and email weekly analytics |
| `sync_to_sheets` | Every 30 minutes | Sync candidate data to Google Sheets |

## ✏️ Adding a New Cron Job

### Step 1: Define the task function in `tasks/scheduler.py`

```python
async def my_custom_task(self):
    """
    Description of what this task does
    
    Schedule: Your schedule description
    """
    logger.info("Running my custom task...")
    try:
        # Your task logic here
        pass
    except Exception as e:
        logger.error(f"Error in my_custom_task: {e}")
```

### Step 2: Register the task in `register_tasks()` method

```python
def register_tasks(self):
    # ... existing tasks ...
    
    # Add your new task
    self.scheduler.add_job(
        self.my_custom_task,
        CronTrigger(hour=10, minute=30),  # Daily at 10:30 AM
        id="my_custom_task",
        name="My Custom Task"
    )
```

## 🕐 Schedule Patterns

### Cron Trigger (specific times)

```python
from apscheduler.triggers.cron import CronTrigger

# Daily at 9 AM
CronTrigger(hour=9, minute=0)

# Every Monday at 8 AM
CronTrigger(day_of_week='mon', hour=8, minute=0)

# First day of month at midnight
CronTrigger(day=1, hour=0, minute=0)

# Every weekday at 5 PM
CronTrigger(day_of_week='mon-fri', hour=17, minute=0)

# Every hour at :15 minutes past
CronTrigger(minute=15)
```

### Interval Trigger (regular intervals)

```python
from apscheduler.triggers.interval import IntervalTrigger

# Every 30 minutes
IntervalTrigger(minutes=30)

# Every 2 hours
IntervalTrigger(hours=2)

# Every day
IntervalTrigger(days=1)

# Every 5 seconds (for testing)
IntervalTrigger(seconds=5)
```

## 🎮 Managing Tasks via API

### List all tasks
```bash
GET /api/v1/tasks/list
```

### Get task details
```bash
GET /api/v1/tasks/{task_id}
```

### Trigger task immediately
```bash
POST /api/v1/tasks/{task_id}/trigger
```

### Pause a task
```bash
POST /api/v1/tasks/{task_id}/pause
```

### Resume a task
```bash
POST /api/v1/tasks/{task_id}/resume
```

### Get scheduler status
```bash
GET /api/v1/tasks/status/overview
```

## 🛠️ Alternative: System Cron (Linux/Mac)

If you prefer system cron instead of APScheduler:

### 1. Create a task runner script

```python
# tasks/run_task.py
import asyncio
from tasks.scheduler import scheduler

async def run_daily_enrichment():
    await scheduler.daily_resume_enrichment()

if __name__ == "__main__":
    asyncio.run(run_daily_enrichment())
```

### 2. Add to system crontab

```bash
# Edit crontab
crontab -e

# Add your task (daily at 9 AM)
0 9 * * * cd /path/to/backend && /path/to/venv/bin/python tasks/run_task.py
```

## 🪟 Alternative: Windows Task Scheduler

For Windows servers:

1. Open **Task Scheduler**
2. Create New Task
3. Set trigger (schedule)
4. Set action: Run Python script
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `tasks\run_task.py`
   - Start in: `C:\path\to\backend`

## ☁️ Alternative: Celery (Distributed Tasks)

For production with multiple workers:

```python
# Install Celery
pip install celery redis

# Create celery app
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379')

@celery_app.task
def enrich_resumes():
    # Task logic
    pass

# Schedule in celerybeat
celery_app.conf.beat_schedule = {
    'enrich-daily': {
        'task': 'tasks.enrich_resumes',
        'schedule': crontab(hour=9, minute=0)
    }
}
```

## 🧪 Testing Tasks

### Run task manually
```python
python -c "from tasks.scheduler import scheduler; import asyncio; asyncio.run(scheduler.daily_resume_enrichment())"
```

### Test with short interval
```python
# In register_tasks(), temporarily change schedule:
IntervalTrigger(seconds=10)  # Run every 10 seconds for testing
```

## 📊 Monitoring Tasks

- Check logs in `data/logs/` for task execution history
- Use `/api/v1/tasks/status/overview` endpoint
- Add monitoring tools (Sentry, DataDog, etc.)

## ⚠️ Important Notes

1. **Timezone**: APScheduler uses UTC by default. Configure timezone in scheduler:
   ```python
   from pytz import timezone
   self.scheduler = AsyncIOScheduler(timezone=timezone('America/New_York'))
   ```

2. **Persistence**: Tasks are in-memory. Use job store for persistence:
   ```python
   from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
   
   jobstores = {
       'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
   }
   self.scheduler = AsyncIOScheduler(jobstores=jobstores)
   ```

3. **Multiple Instances**: If running multiple API instances, use distributed task queue (Celery + Redis)

## 🎯 Common Use Cases

### Send daily candidate summary email
```python
async def daily_candidate_summary(self):
    # Get candidates from last 24 hours
    # Generate summary
    # Email to recruiters
    pass
```

### Auto-archive old applications
```python
async def archive_old_applications(self):
    # Find applications older than 90 days
    # Move to archive
    # Update database
    pass
```

### Refresh cached analytics
```python
async def refresh_analytics_cache(self):
    # Recalculate expensive analytics
    # Update cache/database
    pass
```

## 📚 Resources

- [APScheduler Documentation](https://apscheduler.readthedocs.io/)
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Celery Documentation](https://docs.celeryproject.org/)
