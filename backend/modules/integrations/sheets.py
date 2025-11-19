"""
Google Sheets Integration - Person 4
"""
from typing import List, Dict, Any
import logging
from composio import Composio
from core.config import settings

logger = logging.getLogger(__name__)

class SheetsIntegration:
    def __init__(self, composio_client=None):
        self.composio = composio_client or Composio(api_key=settings.COMPOSIO_API_KEY)
    
    def push_candidate_to_sheet(self, entity_id: str, spreadsheet_id: str,
                               candidate_data: Dict[str, Any], sheet_name: str = "Candidates"):
        try:
            values = [[
                candidate_data.get('name', ''),
                candidate_data.get('email', ''),
                candidate_data.get('phone', ''),
                ', '.join(candidate_data.get('skills', [])[:10]),
                candidate_data.get('experience_years', 0),
                candidate_data.get('status', 'New')
            ]]
            result = self.composio.tools.execute(
                slug="GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND",
                arguments={"spreadsheet_id": spreadsheet_id, "range": f"{sheet_name}!A:F",
                          "values": values, "value_input_option": "RAW"},
                user_id=entity_id, dangerously_skip_version_check=True)
            return {'success': result.get('successful')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_status(self, entity_id: str, spreadsheet_id: str, row: int,
                     status: str, sheet_name: str = "Candidates"):
        try:
            result = self.composio.tools.execute(
                slug="GOOGLESHEETS_UPDATE_SPREADSHEET_PROPERTIES",
                arguments={"spreadsheet_id": spreadsheet_id,
                          "range": f"{sheet_name}!F{row}", "values": [[status]]},
                user_id=entity_id, dangerously_skip_version_check=True)
            return {'success': result.get('successful')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_all_candidates(self, entity_id: str, spreadsheet_id: str,
                          sheet_name: str = "Candidates"):
        try:
            result = self.composio.tools.execute(
                slug="GOOGLESHEETS_BATCH_GET",
                arguments={"spreadsheet_id": spreadsheet_id, "ranges": [f"{sheet_name}!A:F"]},
                user_id=entity_id, dangerously_skip_version_check=True)
            if result.get('successful'):
                return result.get('data', {}).get('valueRanges', [{}])[0].get('values', [])
            return []
        except:
            return []
    
    def get_selected_candidates(self, entity_id: str, spreadsheet_id: str,
                               status: str = "Selected", sheet_name: str = "Candidates"):
        all_candidates = self.get_all_candidates(entity_id, spreadsheet_id, sheet_name)
        return [c for c in all_candidates if len(c) > 5 and c[5] == status]
