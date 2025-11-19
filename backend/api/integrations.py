"""
Integrations API Endpoints

Handles third-party integrations (Gmail, Calendar, Sheets)
Contributors: Person 4 (Gmail Integration)
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from composio import Composio
from core.config import settings
from modules.resume.gmail_monitor import GmailMonitor
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# Request/Response Models
# ============================================================================

class IntegrationStatus(BaseModel):
    """Integration Status Schema"""
    service: str
    connected: bool
    user_email: Optional[str] = None
    connection_id: Optional[str] = None
    scopes: Optional[List[str]] = None


class GmailConnectionRequest(BaseModel):
    """Request to connect Gmail"""
    user_id: str  # Entity ID for Composio
    redirect_url: Optional[str] = "http://localhost:3000/callback"


class GmailConnectionStatus(BaseModel):
    """Gmail connection status"""
    user_id: str
    connected: bool
    message: str
    connection_id: Optional[str] = None


class ProcessResumesRequest(BaseModel):
    """Request to process Gmail resumes"""
    user_id: str  # Entity ID for Composio
    use_mock: bool = False


class ProcessResumesResponse(BaseModel):
    """Response from processing resumes"""
    status: str
    user_id: str
    candidates_found: int
    candidates: List[Dict[str, Any]]
    message: str


# ============================================================================
# Gmail Integration Endpoints
# ============================================================================

@router.get("/gmail/status/{user_id}")
async def check_gmail_status(user_id: str) -> GmailConnectionStatus:
    """
    Check if Gmail is connected for a user
    
    Args:
        user_id: Composio entity_id for the user
        
    Returns:
        Connection status
        
    Frontend Usage:
        GET /api/v1/integrations/gmail/status/user_123
    """
    try:
        composio = Composio(api_key=settings.COMPOSIO_API_KEY)
        
        # Try to fetch emails - if this works, Gmail is connected
        result = composio.tools.execute(
            slug="GMAIL_FETCH_EMAILS",
            arguments={"max_results": 1},
            user_id=user_id,
            dangerously_skip_version_check=True
        )
        
        if result.get('successful'):
            return GmailConnectionStatus(
                user_id=user_id,
                connected=True,
                message="Gmail is connected and working",
                connection_id=None  # Could fetch from Composio if needed
            )
        else:
            return GmailConnectionStatus(
                user_id=user_id,
                connected=False,
                message="Gmail connection failed"
            )
            
    except Exception as e:
        logger.error(f"Error checking Gmail status for {user_id}: {e}")
        return GmailConnectionStatus(
            user_id=user_id,
            connected=False,
            message=f"Not connected: {str(e)}"
        )


@router.get("/gmail/connect-url")
async def get_gmail_connect_url() -> Dict[str, str]:
    """
    Get instructions for connecting Gmail
    
    Returns:
        Instructions and URL for connecting Gmail
        
    Frontend Usage:
        GET /api/v1/integrations/gmail/connect-url
        
    Note: Due to Composio API limitations, users need to connect via
    the Composio web dashboard. This endpoint returns instructions.
    """
    return {
        "status": "info",
        "method": "composio_dashboard",
        "instructions": (
            "To connect Gmail:\n"
            "1. Go to https://app.composio.dev\n"
            "2. Login with your Composio account\n"
            "3. Click 'Connected Accounts' → 'Add Connection'\n"
            "4. Select 'Gmail'\n"
            "5. Set your Entity ID (provided by frontend)\n"
            "6. Complete the OAuth flow\n"
            "7. Return to the app"
        ),
        "dashboard_url": "https://app.composio.dev",
        "note": "Your entity_id will be: user_{your_user_id}"
    }


@router.post("/gmail/process-resumes")
async def process_gmail_resumes(request: ProcessResumesRequest) -> ProcessResumesResponse:
    """
    Process resumes from Gmail for a specific user
    
    Args:
        request: Contains user_id and optional use_mock flag
        
    Returns:
        List of processed candidates
        
    Frontend Usage:
        POST /api/v1/integrations/gmail/process-resumes
        {
            "user_id": "user_123",
            "use_mock": false
        }
    """
    try:
        # Check if Gmail is connected first
        status = await check_gmail_status(request.user_id)
        
        if not status.connected and not request.use_mock:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "gmail_not_connected",
                    "message": "Please connect your Gmail account first",
                    "user_id": request.user_id
                }
            )
        
        # Initialize Gmail monitor
        monitor = GmailMonitor(data_dir=f"./data/users/{request.user_id}")
        
        # Process emails
        candidates = monitor.process_new_emails(
            user_id=request.user_id,
            use_mock=request.use_mock
        )
        
        return ProcessResumesResponse(
            status="success",
            user_id=request.user_id,
            candidates_found=len(candidates),
            candidates=candidates,
            message=f"Successfully processed {len(candidates)} resume(s)"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing resumes for {request.user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resumes: {str(e)}"
        )


# ============================================================================
# Legacy/General Integration Endpoints
# ============================================================================


@router.get("/status")
async def get_integrations_status():
    """
    Get status of all integrations
    
    TODO: Implement integration status check
    - Check Gmail connection
    - Check Calendar connection
    - Check Sheets connection
    - Return health status
    
    Returns:
        Status of all integrations
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/connect/{service}")
async def connect_service(service: str):
    """
    Initiate OAuth connection for a service
    
    TODO: Implement OAuth flow
    - Use modules/integrations/oauth.py
    - Generate OAuth URL
    - Handle user redirect
    - Store connection tokens
    
    Use: modules.integrations.oauth.initiate_connection()
    
    Args:
        service: Service name (gmail, calendar, sheets)
        
    Returns:
        OAuth URL to redirect user
    """
    raise HTTPException(status_code=501, detail="Not implemented - add logic in modules/integrations/oauth.py")


@router.get("/callback")
async def oauth_callback(code: str, state: str):
    """
    Handle OAuth callback
    
    TODO: Implement OAuth callback handling
    - Exchange code for tokens
    - Store tokens securely
    - Update integration status
    
    Use: modules.integrations.oauth.handle_callback()
    
    Args:
        code: OAuth authorization code
        state: State parameter for security
        
    Returns:
        Connection status
    """
    raise HTTPException(status_code=501, detail="Not implemented - add logic in modules/integrations/oauth.py")


@router.delete("/disconnect/{service}")
async def disconnect_service(service: str):
    """
    Disconnect a service
    
    TODO: Implement disconnection
    - Revoke OAuth tokens
    - Remove from database
    - Clean up related data
    
    Args:
        service: Service name
        
    Returns:
        Disconnection status
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/test/{service}")
async def test_integration(service: str):
    """
    Test if integration is working
    
    TODO: Implement integration testing
    - Make a simple API call
    - Verify credentials work
    - Return connection health
    
    
    Args:
        service: Service name
        
    Returns:
        Test results
    """
    raise HTTPException(status_code=501, detail="Not implemented")


# ============================================================================
# Google Services Integration Endpoints (Person 4)
# ============================================================================

from modules.integrations.oauth import OAuthManager
from modules.integrations.calendar import CalendarIntegration
from modules.integrations.sheets import SheetsIntegration


class ConnectRequest(BaseModel):
    entity_id: str
    redirect_url: Optional[str] = None


class EventRequest(BaseModel):
    entity_id: str
    summary: str
    start_time: str  # ISO format
    end_time: str
    attendees: List[str]
    description: Optional[str] = ""


class SheetRequest(BaseModel):
    entity_id: str
    spreadsheet_id: str
    candidate_data: Dict[str, Any]


@router.post("/connect/google")
async def connect_google_service(service: str, request: ConnectRequest):
    """Get OAuth URL for Google service (gmail/calendar/sheets)"""
    try:
        oauth = OAuthManager()
        auth_data = oauth.get_auth_url(service, request.entity_id, request.redirect_url)
        return {"auth_url": auth_data['auth_url'], "message": f"Visit URL to connect {service}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{entity_id}")
async def get_all_integrations_status(entity_id: str):
    """Get connection status for all Google services"""
    try:
        oauth = OAuthManager()
        return oauth.get_all_connections(entity_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calendar/schedule")
async def schedule_interview(request: EventRequest):
    """Schedule interview on Google Calendar"""
    try:
        calendar = CalendarIntegration()
        result = calendar.create_event(
            entity_id=request.entity_id,
            summary=request.summary,
            start_time=request.start_time,
            end_time=request.end_time,
            attendees=request.attendees,
            description=request.description
        )
        if result.get('success'):
            return result
        raise HTTPException(status_code=400, detail=result.get('error'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar/events/{entity_id}")
async def list_calendar_events(entity_id: str, max_results: int = 10):
    """List upcoming calendar events"""
    try:
        calendar = CalendarIntegration()
        return {"events": calendar.list_events(entity_id, max_results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/calendar/event/{entity_id}/{event_id}")
async def cancel_calendar_event(entity_id: str, event_id: str):
    """Cancel a calendar event"""
    try:
        calendar = CalendarIntegration()
        result = calendar.cancel_event(entity_id, event_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sheets/push")
async def push_to_sheets(request: SheetRequest):
    """Push candidate data to Google Sheets"""
    try:
        sheets = SheetsIntegration()
        result = sheets.push_candidate_to_sheet(
            entity_id=request.entity_id,
            spreadsheet_id=request.spreadsheet_id,
            candidate_data=request.candidate_data
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sheets/candidates/{entity_id}/{spreadsheet_id}")
async def get_sheet_candidates(entity_id: str, spreadsheet_id: str):
    """Get all candidates from Google Sheets"""
    try:
        sheets = SheetsIntegration()
        candidates = sheets.get_all_candidates(entity_id, spreadsheet_id)
        return {"candidates": candidates, "total": len(candidates)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sheets/sync/{jd_id}")
async def sync_to_sheets(jd_id: str):
    """
    Sync candidates to Google Sheets
    
    TODO: Implement Sheets sync
    - Use modules/integrations/sheets.py
    - Export candidates to spreadsheet
    - Format data nicely
    - Update on changes
    
    Use: modules.integrations.sheets.export_candidates()
    
    Args:
        jd_id: Job description ID
        
    Returns:
        Sync status and spreadsheet URL
    """
    raise HTTPException(status_code=501, detail="Not implemented - add logic in modules/integrations/sheets.py")

