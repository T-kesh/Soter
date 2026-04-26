"""
Pydantic schemas for artifact security and access control.

This module defines the data models used by the secure artifact download system,
including request/response models and validation schemas.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ArtifactType(str, Enum):
    """Supported artifact types"""
    IMAGE = "image"
    DOCUMENT = "document"
    TEXT = "text"
    VIDEO = "video"
    AUDIO = "audio"


class SensitivityLevel(str, Enum):
    """Artifact sensitivity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UserRole(str, Enum):
    """User roles for artifact access"""
    ADMIN = "admin"
    REVIEWER = "reviewer"
    OPERATOR = "operator"
    VIEWER = "viewer"
    AUDITOR = "auditor"


class AccessType(str, Enum):
    """Types of artifact access"""
    SIGNED_URL_GENERATED = "signed_url_generated"
    DOWNLOAD_ATTEMPT = "download_attempt"
    DOWNLOAD_COMPLETED = "download_completed"
    METADATA_VIEWED = "metadata_viewed"
    AUDIT_LOG_VIEWED = "audit_log_viewed"
    SIGNED_URL_REVOKED = "signed_url_revoked"


class ArtifactAccessRequest(BaseModel):
    """Request model for artifact access"""
    artifact_id: str = Field(..., description="ID of the artifact to access")
    purpose: str = Field(..., description="Purpose of access (e.g., 'verification', 'review', 'audit')")
    justification: Optional[str] = Field(None, description="Additional justification for access")
    
    @validator('purpose')
    def validate_purpose(cls, v):
        allowed_purposes = ['verification', 'review', 'audit', 'investigation', 'compliance']
        if v.lower() not in allowed_purposes:
            raise ValueError(f"Purpose must be one of: {', '.join(allowed_purposes)}")
        return v.lower()


class SignedURLRequest(BaseModel):
    """Request model for signed URL generation"""
    artifact_id: str = Field(..., description="ID of the artifact")
    expires_in_minutes: Optional[int] = Field(
        default=15,
        ge=1,
        le=60,
        description="URL expiration time in minutes (1-60)"
    )
    purpose: Optional[str] = Field("secure_download", description="Purpose of the signed URL")
    
    @validator('artifact_id')
    def validate_artifact_id(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Artifact ID cannot be empty")
        if len(v) > 100:
            raise ValueError("Artifact ID too long (max 100 characters)")
        return v.strip()


class SignedURLResponse(BaseModel):
    """Response model for signed URL"""
    signed_url: str = Field(..., description="Short-lived signed download URL")
    expires_at: str = Field(..., description="UTC expiration timestamp (ISO 8601)")
    token: str = Field(..., description="Access token for audit tracking")
    
    @validator('expires_at')
    def validate_expires_at(cls, v):
        try:
            datetime.fromisoformat(v.rstrip('Z'))
        except ValueError:
            raise ValueError("Invalid datetime format")
        return v


class ArtifactMetadata(BaseModel):
    """Artifact metadata response"""
    id: str = Field(..., description="Unique artifact identifier")
    filename: str = Field(..., description="Original filename")
    mime_type: str = Field(..., description="MIME type of the file")
    size_bytes: int = Field(..., ge=0, description="File size in bytes")
    organization_id: str = Field(..., description="Owning organization ID")
    claim_id: Optional[str] = Field(None, description="Associated claim ID")
    sensitivity_level: SensitivityLevel = Field(..., description="Sensitivity classification")
    created_at: str = Field(..., description="Creation timestamp (ISO 8601)")
    classification: str = Field(..., description="Security classification")
    artifact_type: ArtifactType = Field(..., description="Type of artifact")
    
    @validator('size_bytes')
    def validate_size(cls, v):
        max_size = 100 * 1024 * 1024  # 100MB
        if v > max_size:
            raise ValueError(f"File size too large (max {max_size} bytes)")
        return v
    
    @validator('created_at')
    def validate_created_at(cls, v):
        try:
            datetime.fromisoformat(v.rstrip('Z'))
        except ValueError:
            raise ValueError("Invalid datetime format")
        return v


class UserInfo(BaseModel):
    """User information for access control"""
    user_id: str = Field(..., description="Unique user identifier")
    organization_id: str = Field(..., description="User's organization ID")
    role: UserRole = Field(..., description="User role")
    permissions: List[str] = Field(..., description="User permissions")


class AccessLogEntry(BaseModel):
    """Access log entry model"""
    artifact_id: str = Field(..., description="ID of the accessed artifact")
    user_id: str = Field(..., description="ID of the accessing user")
    user_role: str = Field(..., description="Role of the accessing user")
    organization_id: str = Field(..., description="Organization ID")
    access_type: AccessType = Field(..., description="Type of access performed")
    timestamp: str = Field(..., description="Access timestamp (ISO 8601)")
    ip_address: str = Field(..., description="Client IP address")
    user_agent: str = Field(..., description="Client user agent")
    purpose: Optional[str] = Field(None, description="Purpose of access")
    justification: Optional[str] = Field(None, description="Access justification")
    success: bool = Field(..., description="Whether the access was successful")
    error_message: Optional[str] = Field(None, description="Error message if access failed")
    
    @validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v.rstrip('Z'))
        except ValueError:
            raise ValueError("Invalid datetime format")
        return v


class AuditLogResponse(BaseModel):
    """Response model for audit log queries"""
    logs: List[AccessLogEntry] = Field(..., description="List of access log entries")
    total: int = Field(..., ge=0, description="Total number of entries returned")
    has_more: Optional[bool] = Field(None, description="Whether more entries are available")
    next_cursor: Optional[str] = Field(None, description="Cursor for next page (if paginated)")


class SignedURLInfo(BaseModel):
    """Internal model for signed URL information"""
    payload: Dict[str, Any] = Field(..., description="Signed URL payload")
    signature: str = Field(..., description="HMAC signature")
    created_at: str = Field(..., description="Creation timestamp")
    access_count: int = Field(..., ge=0, description="Number of times accessed")
    max_access: int = Field(..., ge=1, description="Maximum allowed accesses")
    
    @validator('created_at')
    def validate_created_at(cls, v):
        try:
            datetime.fromisoformat(v.rstrip('Z'))
        except ValueError:
            raise ValueError("Invalid datetime format")
        return v


class ArtifactStorageInfo(BaseModel):
    """Model for artifact storage information"""
    id: str = Field(..., description="Artifact ID")
    filename: str = Field(..., description="Original filename")
    mime_type: str = Field(..., description="MIME type")
    size_bytes: int = Field(..., ge=0, description="File size")
    organization_id: str = Field(..., description="Owning organization")
    claim_id: Optional[str] = Field(None, description="Associated claim")
    sensitivity_level: SensitivityLevel = Field(..., description="Sensitivity level")
    created_at: str = Field(..., description="Creation time")
    created_by: str = Field(..., description="Creator user ID")
    classification: str = Field(..., description="Security classification")
    download_url: str = Field(..., description="Secure storage URL")
    checksum: Optional[str] = Field(None, description="File checksum for integrity")
    encryption_status: str = Field("encrypted", description="Encryption status")
    
    @validator('size_bytes')
    def validate_size(cls, v):
        max_size = 100 * 1024 * 1024  # 100MB
        if v > max_size:
            raise ValueError(f"File size too large (max {max_size} bytes)")
        return v


class SecurityConfig(BaseModel):
    """Configuration for artifact security settings"""
    signed_url_expiry_minutes: int = Field(default=15, ge=1, le=60)
    max_file_size_mb: int = Field(default=100, ge=1, le=1000)
    require_justification_for_high_sensitivity: bool = Field(default=True)
    audit_retention_days: int = Field(default=365, ge=30, le=2555)  # 5 years max
    enforce_ip_whitelist: bool = Field(default=False)
    allowed_ip_ranges: List[str] = Field(default_factory=list)
    rate_limit_per_minute: int = Field(default=10, ge=1, le=100)
    
    @validator('signed_url_expiry_minutes')
    def validate_expiry_minutes(cls, v):
        if v < 1 or v > 60:
            raise ValueError("Expiry minutes must be between 1 and 60")
        return v


class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")
    
    @validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v.rstrip('Z'))
        except ValueError:
            raise ValueError("Invalid datetime format")
        return v


class SecurityViolation(BaseModel):
    """Model for security violations"""
    violation_type: str = Field(..., description="Type of security violation")
    user_id: str = Field(..., description="User who committed violation")
    artifact_id: Optional[str] = Field(None, description="Related artifact ID")
    timestamp: str = Field(..., description="Violation timestamp")
    ip_address: str = Field(..., description="Client IP address")
    user_agent: str = Field(..., description="Client user agent")
    details: Dict[str, Any] = Field(..., description="Violation details")
    severity: str = Field(..., description="Severity level (low, medium, high, critical)")
    
    @validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v.rstrip('Z'))
        except ValueError:
            raise ValueError("Invalid datetime format")
        return v


class ArtifactPermission(BaseModel):
    """Model for artifact-specific permissions"""
    can_view: bool = Field(default=False, description="Can view artifact")
    can_download: bool = Field(default=False, description="Can download artifact")
    can_share: bool = Field(default=False, description="Can share artifact")
    can_delete: bool = Field(default=False, description="Can delete artifact")
    can_manage_permissions: bool = Field(default=False, description="Can manage permissions")
    expires_at: Optional[str] = Field(None, description="Permission expiration")
    
    @validator('expires_at')
    def validate_expires_at(cls, v):
        if v is not None:
            try:
                datetime.fromisoformat(v.rstrip('Z'))
            except ValueError:
                raise ValueError("Invalid datetime format")
        return v


class PermissionGrant(BaseModel):
    """Model for granting artifact permissions"""
    user_id: str = Field(..., description="User to grant permissions to")
    artifact_id: str = Field(..., description="Artifact ID")
    permissions: ArtifactPermission = Field(..., description="Permissions to grant")
    granted_by: str = Field(..., description="User granting permissions")
    justification: str = Field(..., description="Reason for granting permissions")
    expires_at: Optional[str] = Field(None, description="Permission expiration")
    
    @validator('expires_at')
    def validate_expires_at(cls, v):
        if v is not None:
            try:
                datetime.fromisoformat(v.rstrip('Z'))
            except ValueError:
                raise ValueError("Invalid datetime format")
        return v
