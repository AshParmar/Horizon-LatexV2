"""
OAuth Handler Module

Person 4: OAuth Authentication for Google Services
Handles OAuth flow and credential management using Composio
Based on: https://docs.composio.dev/docs/custom-auth-configs
"""

from typing import Dict, Any, Optional, List
import os
import logging
from composio import Composio
from core.config import settings

logger = logging.getLogger(__name__)


class OAuthManager:
    """
    OAuth Manager using Composio
    Handles authentication for Gmail, Calendar, and Sheets
    
    Based on Composio's official OAuth2 flow:
    https://docs.composio.dev/docs/custom-auth-configs
    """
    
    def __init__(self):
        """Initialize OAuth Manager with Composio"""
        self.composio_api_key = settings.COMPOSIO_API_KEY
        self.composio = None
        
        # Auth config IDs from environment (optional - uses default if not set)
        self.auth_configs = {
            'gmail': getattr(settings, 'AC_GMAIL', None),
            'calendar': getattr(settings, 'AC_GOOGLE_CALENDAR', None),
            'sheets': getattr(settings, 'AC_GOOGLE_SHEETS', None)
        }
        
        try:
            self.composio = Composio(api_key=self.composio_api_key)
            logger.info("OAuthManager initialized with Composio")
        except Exception as e:
            logger.error(f"Failed to initialize Composio: {e}")
    
    
    def initiate_connection(
        self,
        service: str,
        user_id: str,
        redirect_url: Optional[str] = None,
        auth_config_id: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Initiate OAuth connection for a service
        
        Official Composio method from docs:
        composio.connected_accounts.initiate(user_id, auth_config_id)
        
        Args:
            service: Service name ('gmail', 'calendar', 'sheets')
            user_id: User's ID (entity_id for Composio)
            redirect_url: Optional custom redirect URL
            auth_config_id: Optional custom auth config ID
            
        Returns:
            Dict with redirect_url and connection_request details
        """
        if not self.composio:
            raise RuntimeError("Composio not initialized")
        
        try:
            # Use provided auth_config_id or get from settings
            if not auth_config_id:
                auth_config_id = self.auth_configs.get(service.lower())
            
            logger.info(f"Initiating connection for {service} (user: {user_id})")
            
            # Official Composio method from documentation
            connection_request = self.composio.connected_accounts.initiate(
                user_id=user_id,
                auth_config_id=auth_config_id,  # Can be None to use default
                redirect_url=redirect_url
            )
            
            logger.info(f"✅ Connection initiated: {connection_request.redirectUrl}")
            
            return {
                'redirect_url': connection_request.redirectUrl,
                'connection_id': connection_request.connectionId if hasattr(connection_request, 'connectionId') else None,
                'user_id': user_id,
                'service': service,
                'status': 'initiated'
            }
            
        except Exception as e:
            logger.error(f"Error initiating connection for {service}: {e}")
            raise
    
    
    def wait_for_connection(
        self,
        connection_request,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        Wait for OAuth connection to be established
        
        Official Composio method from docs:
        connection_request.wait_for_connection()
        
        Args:
            connection_request: Connection request object
            timeout: Timeout in seconds (default: 5 minutes)
            
        Returns:
            Connected account details
        """
        try:
            logger.info("Waiting for user to complete OAuth...")
            
            # Official Composio method
            connected_account = connection_request.wait_for_connection(timeout=timeout)
            
            logger.info("✅ Connection established!")
            return {
                'status': 'connected',
                'account_id': connected_account.id if hasattr(connected_account, 'id') else None,
                'connected': True
            }
            
        except Exception as e:
            logger.error(f"Error waiting for connection: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'connected': False
            }
    
    
    def get_auth_url(
        self,
        service: str,
        entity_id: str,
        redirect_url: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Get OAuth authorization URL for a service (simplified wrapper)
        
        Args:
            service: Service name ('gmail', 'calendar', 'sheets')
            entity_id: User's entity ID
            redirect_url: Optional redirect URL after auth
            
        Returns:
            Dict with auth_url and connection_id
        """
        return self.initiate_connection(service, entity_id, redirect_url)
    
    
    def check_connection(
        self,
        service: str,
        entity_id: str
    ) -> Dict[str, Any]:
        """
        Check if service is connected for user
        
        Args:
            service: Service name ('gmail', 'calendar', 'sheets')
            entity_id: User's entity ID
            
        Returns:
            Connection status and details
        """
        if not self.composio:
            return {'connected': False, 'error': 'Composio not initialized'}
        
        try:
            app_map = {
                'gmail': 'GMAIL',
                'calendar': 'GOOGLECALENDAR',
                'sheets': 'GOOGLESHEETS'
            }
            
            app_name = app_map.get(service.lower())
            if not app_name:
                raise ValueError(f"Unsupported service: {service}")
            
            # Get entity's connections
            entity = self.composio.get_entity(entity_id)
            connections = entity.get_connections(app_name=app_name)
            
            if connections:
                connection = connections[0]
                return {
                    'connected': True,
                    'service': service,
                    'entity_id': entity_id,
                    'connection_id': connection.id,
                    'status': connection.status
                }
            else:
                return {
                    'connected': False,
                    'service': service,
                    'entity_id': entity_id,
                    'message': f'{service} not connected'
                }
                
        except Exception as e:
            logger.error(f"Error checking connection for {service}: {e}")
            return {
                'connected': False,
                'service': service,
                'error': str(e)
            }
    
    
    def get_credentials(self, service: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get credentials for a service"""
        connection_status = self.check_connection(service, entity_id)
        return connection_status if connection_status.get('connected') else None
    
    
    def get_gmail_service(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get Gmail service credentials"""
        return self.get_credentials('gmail', entity_id)
    
    
    def get_sheets_service(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get Google Sheets service credentials"""
        return self.get_credentials('sheets', entity_id)
    
    
    def get_calendar_service(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get Google Calendar service credentials"""
        return self.get_credentials('calendar', entity_id)
    
    
    def get_all_connections(self, entity_id: str) -> Dict[str, Any]:
        """Get all service connections for a user"""
        services = ['gmail', 'calendar', 'sheets']
        connections = {}
        
        for service in services:
            connections[service] = self.check_connection(service, entity_id)
        
        return {
            'entity_id': entity_id,
            'connections': connections,
            'total': len([c for c in connections.values() if c.get('connected')])
        }
