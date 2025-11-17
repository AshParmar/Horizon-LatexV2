"""
Tasks Management API Endpoints

TODO: Implement task management endpoints
Contributors: Add endpoints to view and manage scheduled tasks
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from tasks.scheduler import scheduler
from datetime import datetime

router = APIRouter()


class TaskInfo(BaseModel):
    """Task information schema"""
    id: str
    name: str
    next_run_time: str | None
    trigger: str


@router.get("/list", response_model=List[TaskInfo])
async def list_scheduled_tasks():
    """
    List all scheduled tasks
    
    Returns:
        List of scheduled tasks with their info
    """
    jobs = scheduler.scheduler.get_jobs()
    
    task_list = []
    for job in jobs:
        task_list.append({
            "id": job.id,
            "name": job.name,
            "next_run_time": str(job.next_run_time) if job.next_run_time else None,
            "trigger": str(job.trigger)
        })
    
    return task_list


@router.get("/{task_id}")
async def get_task_info(task_id: str):
    """
    Get information about a specific task
    
    Args:
        task_id: Task ID
        
    Returns:
        Task details
    """
    job = scheduler.scheduler.get_job(task_id)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return {
        "id": job.id,
        "name": job.name,
        "next_run_time": str(job.next_run_time) if job.next_run_time else None,
        "trigger": str(job.trigger),
        "max_instances": job.max_instances,
        "coalesce": job.coalesce
    }


@router.post("/{task_id}/trigger")
async def trigger_task_now(task_id: str):
    """
    Manually trigger a task to run immediately
    
    TODO: Implement manual task triggering
    
    Args:
        task_id: Task ID to trigger
        
    Returns:
        Trigger status
    """
    job = scheduler.scheduler.get_job(task_id)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    # Trigger the job immediately
    job.modify(next_run_time=datetime.now())
    
    return {
        "status": "triggered",
        "task_id": task_id,
        "message": f"Task {task_id} will run immediately"
    }


@router.post("/{task_id}/pause")
async def pause_task(task_id: str):
    """
    Pause a scheduled task
    
    Args:
        task_id: Task ID to pause
        
    Returns:
        Pause status
    """
    job = scheduler.scheduler.get_job(task_id)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    scheduler.scheduler.pause_job(task_id)
    
    return {
        "status": "paused",
        "task_id": task_id,
        "message": f"Task {task_id} has been paused"
    }


@router.post("/{task_id}/resume")
async def resume_task(task_id: str):
    """
    Resume a paused task
    
    Args:
        task_id: Task ID to resume
        
    Returns:
        Resume status
    """
    job = scheduler.scheduler.get_job(task_id)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    scheduler.scheduler.resume_job(task_id)
    
    return {
        "status": "resumed",
        "task_id": task_id,
        "message": f"Task {task_id} has been resumed"
    }


@router.get("/status/overview")
async def get_scheduler_status():
    """
    Get overall scheduler status
    
    Returns:
        Scheduler status and statistics
    """
    jobs = scheduler.scheduler.get_jobs()
    
    return {
        "running": scheduler.scheduler.running,
        "total_jobs": len(jobs),
        "state": scheduler.scheduler.state,
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "next_run": str(job.next_run_time) if job.next_run_time else None
            }
            for job in jobs
        ]
    }
