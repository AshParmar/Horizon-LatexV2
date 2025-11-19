"""
Google Calendar Integration - Person 4
"""
from typing import List, Dict, Any
import logging
from datetime import datetime, timedelta
from composio import Composio
from core.config import settings

logger = logging.getLogger(__name__)

class CalendarIntegration:
    def __init__(self, composio_client=None):
        self.composio = composio_client or Composio(api_key=settings.COMPOSIO_API_KEY)
    
    def create_event(self, entity_id: str, summary: str, start_time: str, end_time: str,
                    attendees: List[str], description: str = "", calendar_id: str = "primary"):
        try:
            result = self.composio.tools.execute(
                slug="GOOGLECALENDAR_CREATE_EVENT",
                arguments={"calendar_id": calendar_id, "summary": summary,
                          "description": description,
                          "start": {"dateTime": start_time, "timeZone": "UTC"},
                          "end": {"dateTime": end_time, "timeZone": "UTC"},
                          "attendees": [{"email": e} for e in attendees]},
                user_id=entity_id, dangerously_skip_version_check=True)
            if result.get('successful'):
                return {'success': True, 'event_id': result['data'].get('id')}
            return {'success': False, 'error': result.get('error')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_events(self, entity_id: str, max_results: int = 10):
        try:
            result = self.composio.tools.execute(
                slug="GOOGLECALENDAR_EVENTS_LIST",
                arguments={"calendar_id": "primary", "max_results": max_results},
                user_id=entity_id, dangerously_skip_version_check=True)
            return result.get('data', {}).get('items', []) if result.get('successful') else []
        except:
            return []
    
    def cancel_event(self, entity_id: str, event_id: str):
        try:
            result = self.composio.tools.execute(
                slug="GOOGLECALENDAR_DELETE_EVENT",
                arguments={"calendar_id": "primary", "event_id": event_id},
                user_id=entity_id, dangerously_skip_version_check=True)
            return {'success': result.get('successful')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
