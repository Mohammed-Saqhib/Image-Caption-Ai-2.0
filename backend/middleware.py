"""
🛡️ Middleware for Request Validation, Rate Limiting & Security
Advanced middleware for production-ready API
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Dict, Any
import time
from datetime import datetime, timedelta
from collections import defaultdict
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============ File Validation ============

class FileValidator:
    """Validate uploaded files"""
    
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @classmethod
    def validate_file(cls, file_path: str, file_size: int) -> Dict[str, Any]:
        """Validate file type and size"""
        path = Path(file_path)
        extension = path.suffix.lower()
        
        # Check extension
        if extension not in cls.ALLOWED_EXTENSIONS:
            return {
                'is_valid': False,
                'error': f'Invalid file type. Allowed: {", ".join(cls.ALLOWED_EXTENSIONS)}'
            }
        
        # Check size
        if file_size > cls.MAX_FILE_SIZE:
            max_mb = cls.MAX_FILE_SIZE / (1024 * 1024)
            return {
                'is_valid': False,
                'error': f'File too large. Maximum size: {max_mb}MB'
            }
        
        return {
            'is_valid': True,
            'file_type': extension,
            'file_size': file_size
        }


# ============ Rate Limiting ============

class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        self.window = 60  # 1 minute window
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        
        # Remove old requests outside the time window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests"""
        now = time.time()
        recent = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window
        ]
        return max(0, self.requests_per_minute - len(recent))
    
    def get_reset_time(self, client_id: str) -> float:
        """Get time until rate limit resets"""
        if not self.requests[client_id]:
            return 0
        oldest = min(self.requests[client_id])
        return max(0, self.window - (time.time() - oldest))


# ============ Rate Limiting Middleware ============

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting"""
    
    def __init__(self, app, requests_per_minute: int = 30):
        super().__init__(app)
        self.rate_limiter = RateLimiter(requests_per_minute)
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Skip rate limiting for health checks and docs
        if request.url.path in ['/api/health', '/api/docs', '/api/redoc', '/openapi.json']:
            return await call_next(request)
        
        # Get client identifier (IP address)
        client_id = request.client.host
        
        # Check rate limit
        if not self.rate_limiter.is_allowed(client_id):
            reset_time = self.rate_limiter.get_reset_time(client_id)
            logger.warning(f"Rate limit exceeded for {client_id}")
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    'success': False,
                    'error': 'Rate limit exceeded',
                    'detail': f'Too many requests. Try again in {int(reset_time)} seconds.',
                    'retry_after': int(reset_time)
                },
                headers={
                    'Retry-After': str(int(reset_time)),
                    'X-RateLimit-Remaining': '0',
                    'X-RateLimit-Reset': str(int(time.time() + reset_time))
                }
            )
        
        # Add rate limit headers
        response = await call_next(request)
        remaining = self.rate_limiter.get_remaining(client_id)
        response.headers['X-RateLimit-Limit'] = str(self.rate_limiter.requests_per_minute)
        response.headers['X-RateLimit-Remaining'] = str(remaining)
        
        return response


# ============ Request Logging Middleware ============

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request logging"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        # Log request
        logger.info(f"🔵 {request.method} {request.url.path} - {request.client.host}")
        
        # Process request
        try:
            response = await call_next(request)
            processing_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"✅ {request.method} {request.url.path} - "
                f"Status: {response.status_code} - "
                f"Time: {processing_time:.3f}s"
            )
            
            # Add processing time header
            response.headers['X-Process-Time'] = f"{processing_time:.3f}"
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                f"❌ {request.method} {request.url.path} - "
                f"Error: {str(e)} - "
                f"Time: {processing_time:.3f}s"
            )
            raise


# ============ Error Handler ============

class APIError(Exception):
    """Custom API exception"""
    
    def __init__(
        self,
        error: str,
        detail: str = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "API_ERROR"
    ):
        self.error = error
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.error)


def create_error_response(error: str, detail: str = None, status_code: int = 400, error_code: str = "API_ERROR"):
    """Create standardized error response"""
    return JSONResponse(
        status_code=status_code,
        content={
            'success': False,
            'error': error,
            'detail': detail,
            'error_code': error_code,
            'timestamp': datetime.now().isoformat()
        }
    )


# ============ CORS Headers ============

def add_cors_headers(response):
    """Add CORS headers to response"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response
