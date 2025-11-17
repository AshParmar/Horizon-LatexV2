"""
Logging Configuration
Setup logging middleware and utilities

TODO: Contributors configure logging as needed
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.config import settings
import time


def setup_logging(app: FastAPI):
    """
    Setup logging configuration for FastAPI
    
    TODO: Configure production logging
    - Add file rotation
    - Configure log levels per environment
    - Add structured logging (JSON format)
    - Integrate with logging service (e.g., CloudWatch, DataDog)
    
    Args:
        app: FastAPI application instance
    """
    
    # Create logs directory
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
            )
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")
    
    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """
        Log all incoming requests
        
        TODO: Add more request details
        - User ID
        - Request body (careful with sensitive data)
        - Response size
        """
        start_time = time.time()
        
        logger.info(f"Request: {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            logger.info(
                f"Response: {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Duration: {process_time:.4f}s"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Request failed: {request.method} {request.url.path} Error: {str(e)}")
            raise
    
    # Add exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """
        Global exception handler
        
        TODO: Add proper error tracking
        - Send to error monitoring service (Sentry, etc.)
        - Format errors consistently
        - Add request context
        """
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc) if settings.DEBUG else "An error occurred"
            }
        )


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
