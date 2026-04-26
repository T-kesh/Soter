"""
Secure verification artifact download API with signed URLs and access control.

This module provides secure access to sensitive verification artifacts through:
- Short-lived signed URLs with expiration
- Role-based access control and organization ownership validation
- Comprehensive audit logging for all access events
"""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import logging
import json
import time

from config import settings
from schemas.errors import ErrorDetail, ErrorEnvelope

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai/artifacts", tags=["artifacts"])
security = HTTPBearer()

# Configuration
SIGNED_URL_EXPIRY_MINUTES = 15  # Short-lived URLs
MAX_FILE_SIZE_MB = 100  # Maximum file size for security
SIGNATURE_ALGORITHM = "HS256"

# In-memory storage for demo (replace with Redis/DB in production)
# Maps artifact_id -> artifact metadata
_artifact_store: Dict[str, Dict[str, Any]] = {
    "demo-artifact-1": {
        "id": "demo-artifact-1",
        "filename": "verification_document.pdf",
        "mime_type": "application/pdf",
        "size_bytes": 2048576,
        "organization_id": "org-123",
        "claim_id": "claim-456",
        "sensitivity_level": "high",
        "created_at": "2024-01-15T10:30:00Z",
        "created_by": "user-789",
        "classification": "sensitive_evidence",
        "download_url": "https://secure-storage.example.com/files/demo-artifact-1",
    },
    "demo-artifact-2": {
        "id": "demo-artifact-2",
        "filename": "id_card_scan.jpg",
        "mime_type": "image/jpeg",
        "size_bytes": 1024576,
        "organization_id": "org-123",
        "claim_id": "claim-457",
        "sensitivity_level": "high",
        "created_at": "2024-01-15T11:00:00Z",
        "created_by": "user-790",
        "classification": "personal_identification",
        "download_url": "https://secure-storage.example.com/files/demo-artifact-2",
    }
}

# In-memory storage for signed URLs (replace with Redis in production)
_signed_urls: Dict[str, Dict[str, Any]] = {}

# In-memory audit log (replace with database in production)
_audit_log: List[Dict[str, Any]] = []

# User roles and permissions (replace with auth service in production)
_user_roles: Dict[str, Dict[str, Any]] = {
    "admin-user": {
        "user_id": "admin-user",
        "organization_id": "org-123",
        "role": "admin",
        "permissions": ["view_all_artifacts", "manage_artifacts", "audit_access"]
    },
    "reviewer-user": {
        "user_id": "reviewer-user",
        "organization_id": "org-123",
        "role": "reviewer",
        "permissions": ["view_assigned_artifacts", "audit_access"]
    },
    "operator-user": {
        "user_id": "operator-user",
        "organization_id": "org-123",
        "role": "operator",
        "permissions": ["view_assigned_artifacts"]
    }
}


# Pydantic Models
class ArtifactAccessRequest(BaseModel):
    """Request model for artifact access"""
    artifact_id: str = Field(..., description="ID of the artifact to access")
    purpose: str = Field(..., description="Purpose of access (e.g., 'verification', 'review', 'audit')")
    justification: Optional[str] = Field(None, description="Additional justification for access")


class SignedURLRequest(BaseModel):
    """Request model for signed URL generation"""
    artifact_id: str = Field(..., description="ID of the artifact")
    expires_in_minutes: Optional[int] = Field(
        default=SIGNED_URL_EXPIRY_MINUTES,
        ge=1,
        le=60,
        description="URL expiration time in minutes (1-60)"
    )


class SignedURLResponse(BaseModel):
    """Response model for signed URL"""
    signed_url: str = Field(..., description="Short-lived signed download URL")
    expires_at: str = Field(..., description="UTC expiration timestamp")
    token: str = Field(..., description="Access token for audit tracking")


class ArtifactMetadata(BaseModel):
    """Artifact metadata response"""
    id: str
    filename: str
    mime_type: str
    size_bytes: int
    organization_id: str
    claim_id: Optional[str]
    sensitivity_level: str
    created_at: str
    classification: str


class AccessLogEntry(BaseModel):
    """Access log entry model"""
    artifact_id: str
    user_id: str
    user_role: str
    organization_id: str
    access_type: str  # 'signed_url_generated', 'download_attempt', 'download_completed'
    timestamp: str
    ip_address: str
    user_agent: str
    purpose: Optional[str]
    justification: Optional[str]
    success: bool
    error_message: Optional[str]


# Helper Functions
def generate_signed_token() -> str:
    """Generate a cryptographically secure token"""
    return secrets.token_urlsafe(32)


def create_signature(payload: Dict[str, Any], secret: str) -> str:
    """Create HMAC signature for payload"""
    payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    return hmac.new(
        secret.encode('utf-8'),
        payload_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def verify_signature(payload: Dict[str, Any], signature: str, secret: str) -> bool:
    """Verify HMAC signature"""
    expected_signature = create_signature(payload, secret)
    return hmac.compare_digest(signature, expected_signature)


def log_access_event(
    artifact_id: str,
    user_id: str,
    user_role: str,
    organization_id: str,
    access_type: str,
    request: Request,
    purpose: Optional[str] = None,
    justification: Optional[str] = None,
    success: bool = True,
    error_message: Optional[str] = None
):
    """Log artifact access event for audit"""
    entry = {
        "artifact_id": artifact_id,
        "user_id": user_id,
        "user_role": user_role,
        "organization_id": organization_id,
        "access_type": access_type,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ip_address": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
        "purpose": purpose,
        "justification": justification,
        "success": success,
        "error_message": error_message
    }
    
    _audit_log.append(entry)
    logger.info(f"Artifact access logged: {artifact_id} by {user_id} ({user_role}) - {access_type}")


def verify_user_permissions(
    user_id: str,
    artifact_id: str,
    required_permission: str
) -> Dict[str, Any]:
    """Verify user has required permissions for artifact access"""
    # Get user role information
    user_info = _user_roles.get(user_id)
    if not user_info:
        raise HTTPException(
            status_code=403,
            detail="User not found or unauthorized"
        )
    
    # Get artifact information
    artifact = _artifact_store.get(artifact_id)
    if not artifact:
        raise HTTPException(
            status_code=404,
            detail="Artifact not found"
        )
    
    # Verify organization ownership
    if user_info["organization_id"] != artifact["organization_id"]:
        raise HTTPException(
            status_code=403,
            detail="User does not have access to artifacts from this organization"
        )
    
    # Verify required permission
    if required_permission not in user_info["permissions"]:
        raise HTTPException(
            status_code=403,
            detail=f"Insufficient permissions. Required: {required_permission}"
        )
    
    return user_info


# Dependencies
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Extract and validate user from JWT token"""
    # In production, this would validate JWT token and extract user info
    # For demo, we'll extract user_id from token (simplified)
    token = credentials.credentials
    
    # Mock JWT validation - in production, use proper JWT validation
    if token.startswith("user-"):
        user_id = token
        user_info = _user_roles.get(user_id)
        if not user_info:
            raise HTTPException(
                status_code=401,
                detail="Invalid user token"
            )
        return user_info
    
    raise HTTPException(
        status_code=401,
        detail="Invalid authentication token"
    )


# API Endpoints
@router.post("/signed-url", response_model=SignedURLResponse)
async def generate_signed_url(
    request_data: SignedURLRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate a short-lived signed URL for secure artifact download.
    
    This endpoint:
    - Verifies user permissions and organization ownership
    - Creates a signed URL with limited validity (max 60 minutes)
    - Logs the access request for audit purposes
    """
    try:
        # Verify user permissions
        user_info = verify_user_permissions(
            current_user["user_id"],
            request_data.artifact_id,
            "view_all_artifacts" if current_user["role"] == "admin" else "view_assigned_artifacts"
        )
        
        # Generate signed token and URL
        token = generate_signed_token()
        expires_at = datetime.utcnow() + timedelta(minutes=request_data.expires_in_minutes)
        
        # Create signed URL payload
        payload = {
            "artifact_id": request_data.artifact_id,
            "user_id": current_user["user_id"],
            "token": token,
            "expires_at": expires_at.isoformat() + "Z",
            "purpose": "secure_download"
        }
        
        # Create signature
        signature = create_signature(payload, settings.secret_key if hasattr(settings, 'secret_key') else "demo-secret")
        
        # Store signed URL info
        _signed_urls[token] = {
            "payload": payload,
            "signature": signature,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "access_count": 0,
            "max_access": 1  # One-time use URL
        }
        
        # Build signed URL
        base_url = str(request.base_url).rstrip('/')
        signed_url = f"{base_url}/v1/ai/artifacts/download/{token}"
        
        # Log access event
        log_access_event(
            artifact_id=request_data.artifact_id,
            user_id=current_user["user_id"],
            user_role=current_user["role"],
            organization_id=current_user["organization_id"],
            access_type="signed_url_generated",
            request=request,
            purpose="secure_download",
            success=True
        )
        
        return SignedURLResponse(
            signed_url=signed_url,
            expires_at=expires_at.isoformat() + "Z",
            token=token
        )
        
    except HTTPException:
        # Log failed access attempt
        log_access_event(
            artifact_id=request_data.artifact_id,
            user_id=current_user["user_id"],
            user_role=current_user["role"],
            organization_id=current_user["organization_id"],
            access_type="signed_url_generated",
            request=request,
            success=False,
            error_message="Permission denied or artifact not found"
        )
        raise
    except Exception as e:
        logger.error(f"Error generating signed URL: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/download/{token}")
async def download_artifact(
    token: str,
    request: Request
):
    """
    Download artifact using signed URL token.
    
    This endpoint:
    - Validates the signed URL token and signature
    - Enforces expiration and one-time use
    - Logs the download for audit
    - Returns the artifact or proxies the download
    """
    try:
        # Get signed URL info
        signed_url_info = _signed_urls.get(token)
        if not signed_url_info:
            log_access_event(
                artifact_id="unknown",
                user_id="unknown",
                user_role="unknown",
                organization_id="unknown",
                access_type="download_attempt",
                request=request,
                success=False,
                error_message="Invalid or expired token"
            )
            raise HTTPException(
                status_code=404,
                detail="Invalid or expired download URL"
            )
        
        payload = signed_url_info["payload"]
        signature = signed_url_info["signature"]
        
        # Verify signature
        if not verify_signature(
            payload,
            signature,
            settings.secret_key if hasattr(settings, 'secret_key') else "demo-secret"
        ):
            log_access_event(
                artifact_id=payload["artifact_id"],
                user_id=payload["user_id"],
                user_role="unknown",
                organization_id="unknown",
                access_type="download_attempt",
                request=request,
                success=False,
                error_message="Invalid signature"
            )
            raise HTTPException(
                status_code=403,
                detail="Invalid download URL signature"
            )
        
        # Check expiration
        expires_at = datetime.fromisoformat(payload["expires_at"].rstrip('Z'))
        if datetime.utcnow() > expires_at:
            log_access_event(
                artifact_id=payload["artifact_id"],
                user_id=payload["user_id"],
                user_role="unknown",
                organization_id="unknown",
                access_type="download_attempt",
                request=request,
                success=False,
                error_message="URL expired"
            )
            raise HTTPException(
                status_code=410,
                detail="Download URL has expired"
            )
        
        # Check access count
        if signed_url_info["access_count"] >= signed_url_info["max_access"]:
            log_access_event(
                artifact_id=payload["artifact_id"],
                user_id=payload["user_id"],
                user_role="unknown",
                organization_id="unknown",
                access_type="download_attempt",
                request=request,
                success=False,
                error_message="URL already used"
            )
            raise HTTPException(
                status_code=410,
                detail="Download URL has already been used"
            )
        
        # Get artifact
        artifact = _artifact_store.get(payload["artifact_id"])
        if not artifact:
            log_access_event(
                artifact_id=payload["artifact_id"],
                user_id=payload["user_id"],
                user_role="unknown",
                organization_id="unknown",
                access_type="download_attempt",
                request=request,
                success=False,
                error_message="Artifact not found"
            )
            raise HTTPException(
                status_code=404,
                detail="Artifact not found"
            )
        
        # Increment access count
        signed_url_info["access_count"] += 1
        
        # Get user info for logging
        user_info = _user_roles.get(payload["user_id"])
        
        # Log successful download
        log_access_event(
            artifact_id=payload["artifact_id"],
            user_id=payload["user_id"],
            user_role=user_info["role"] if user_info else "unknown",
            organization_id=user_info["organization_id"] if user_info else "unknown",
            access_type="download_completed",
            request=request,
            success=True
        )
        
        # In production, this would:
        # 1. Stream the file from secure storage
        # 2. Or redirect to a secure storage URL
        # 3. Or proxy the download through the service
        
        # For demo, we'll return a mock download response
        return Response(
            content=f"Mock file content for {artifact['filename']}".encode(),
            media_type=artifact["mime_type"],
            headers={
                "Content-Disposition": f"attachment; filename={artifact['filename']}",
                "Content-Length": str(len(f"Mock file content for {artifact['filename']}".encode())),
                "X-Artifact-ID": artifact["id"],
                "X-Access-Token": token
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading artifact: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/{artifact_id}/metadata", response_model=ArtifactMetadata)
async def get_artifact_metadata(
    artifact_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get artifact metadata without exposing sensitive content.
    
    This endpoint:
    - Verifies user permissions and organization ownership
    - Returns only metadata, not the actual file content
    - Logs the metadata access for audit
    """
    try:
        # Verify user permissions
        user_info = verify_user_permissions(
            current_user["user_id"],
            artifact_id,
            "view_all_artifacts" if current_user["role"] == "admin" else "view_assigned_artifacts"
        )
        
        # Get artifact
        artifact = _artifact_store.get(artifact_id)
        if not artifact:
            raise HTTPException(
                status_code=404,
                detail="Artifact not found"
            )
        
        # Log metadata access
        log_access_event(
            artifact_id=artifact_id,
            user_id=current_user["user_id"],
            user_role=current_user["role"],
            organization_id=current_user["organization_id"],
            access_type="metadata_viewed",
            request=request,
            success=True
        )
        
        return ArtifactMetadata(**artifact)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting artifact metadata: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/audit/log")
async def get_audit_log(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    artifact_id: Optional[str] = None,
    limit: int = 100
):
    """
    Get audit log for artifact access (admin/auditor only).
    
    This endpoint:
    - Requires audit permissions
    - Returns filtered access logs
    - Supports pagination and filtering
    """
    try:
        # Verify user has audit permissions
        if "audit_access" not in current_user["permissions"]:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions for audit access"
            )
        
        # Filter logs
        filtered_logs = _audit_log
        
        # Filter by artifact_id if specified
        if artifact_id:
            filtered_logs = [log for log in filtered_logs if log["artifact_id"] == artifact_id]
        
        # Filter by organization
        filtered_logs = [log for log in filtered_logs if log["organization_id"] == current_user["organization_id"]]
        
        # Sort by timestamp (newest first) and limit
        filtered_logs.sort(key=lambda x: x["timestamp"], reverse=True)
        filtered_logs = filtered_logs[:limit]
        
        # Log audit access
        log_access_event(
            artifact_id="audit_system",
            user_id=current_user["user_id"],
            user_role=current_user["role"],
            organization_id=current_user["organization_id"],
            access_type="audit_log_viewed",
            request=request,
            success=True
        )
        
        return {"logs": filtered_logs, "total": len(filtered_logs)}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting audit log: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.delete("/signed-url/{token}")
async def revoke_signed_url(
    token: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Revoke a signed URL before expiration (admin only).
    
    This endpoint:
    - Requires admin permissions
    - Immediately invalidates the signed URL
    - Logs the revocation for audit
    """
    try:
        # Verify admin permissions
        if current_user["role"] != "admin":
            raise HTTPException(
                status_code=403,
                detail="Only administrators can revoke signed URLs"
            )
        
        # Remove signed URL
        if token not in _signed_urls:
            raise HTTPException(
                status_code=404,
                detail="Signed URL not found"
            )
        
        artifact_id = _signed_urls[token]["payload"]["artifact_id"]
        del _signed_urls[token]
        
        # Log revocation
        log_access_event(
            artifact_id=artifact_id,
            user_id=current_user["user_id"],
            user_role=current_user["role"],
            organization_id=current_user["organization_id"],
            access_type="signed_url_revoked",
            request=request,
            success=True
        )
        
        return {"message": "Signed URL revoked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error revoking signed URL: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
