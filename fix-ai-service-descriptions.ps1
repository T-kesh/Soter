$repo = "Pulsefy/Soter"

$issues = @(
    @{
        Number = 244
        Title = "Standardize Error Envelope Across All Routes"
        Body = @"
## Complexity Score: 100

### Description
Unify error responses so the backend and frontend can reliably parse AI-service failures.

### Requirements
- Implement a consistent JSON error envelope with code, message, and details.
- Ensure FastAPI exception handlers map validation errors, downstream errors, and internal errors into the envelope.
- Add tests that assert response shape for at least 5 representative failure cases.
"@
    },
    @{
        Number = 269
        Title = "Request Correlation ID Propagation"
        Body = @"
## Complexity Score: 150

### Description
Enable end-to-end tracing by propagating correlation IDs through logs and outbound requests.

### Requirements
- Accept X-Request-Id and/or generate one when missing.
- Include the correlation ID in every log line and outbound HTTP request headers.
- Add tests verifying correlation IDs are present in responses and logs for at least one route.
"@
    },
    @{
        Number = 274
        Title = "Add Structured Logging with Redaction Guarantees"
        Body = @"
## Complexity Score: 200

### Description
Move to structured logs while ensuring PII never leaks to logs.

### Requirements
- Adopt JSON structured logging with a stable schema (timestamp, level, requestId, route, latencyMs, outcome).
- Ensure redaction is applied to all known sensitive fields before logging.
- Add tests that confirm PII-like strings are not present in logs for key endpoints.
"@
    },
    @{
        Number = 245
        Title = "Harden Form Upload Validation and Limits"
        Body = @"
## Complexity Score: 150

### Description
Improve security and stability for endpoints that accept evidence uploads or multipart form data.

### Requirements
- Enforce maximum file size, allowed MIME types, and allowed file extensions.
- Reject ambiguous inputs (multiple files when only one is expected, missing fields, invalid filenames).
- Add tests for boundary sizes and malicious/invalid MIME scenarios.
"@
    },
    @{
        Number = 246
        Title = "Improve PII Scrubber Coverage with Regression Test Set"
        Body = @"
## Complexity Score: 150

### Description
Increase confidence that PII scrubbing is correct and stays correct over time.

### Requirements
- Create a curated set of anonymization fixtures (emails, phone numbers, IDs, addresses, names).
- Add unit tests that validate expected transformations and non-destructive behavior on safe text.
- Include at least one false positive guard test to prevent over-redaction.
"@
    },
    @{
        Number = 247
        Title = "Deterministic Test Mode for AI Outputs"
        Body = @"
## Complexity Score: 150

### Description
Make tests stable by offering deterministic behavior for AI-driven steps.

### Requirements
- Add a test mode config that forces deterministic results for verification scoring and classification.
- Ensure the mode can be enabled via environment variable in CI.
- Add tests that confirm deterministic outputs remain stable across runs.
"@
    },
    @{
        Number = 248
        Title = "Introduce Versioned API Routes for AI Service"
        Body = @"
## Complexity Score: 150

### Description
Prepare for non-breaking evolution by versioning the API surface.

### Requirements
- Add a version prefix strategy (e.g., /v1) for all routes.
- Keep backwards compatibility with non-versioned routes temporarily via redirects or dual mounting.
- Add tests that ensure both paths behave consistently (where intended).
"@
    },
    @{
        Number = 249
        Title = "Evidence Preprocessing Pipeline Metrics"
        Body = @"
## Complexity Score: 150

### Description
Measure and monitor preprocessing costs (OCR, normalization, scrubbing) to prevent regressions.

### Requirements
- Add timing metrics for major pipeline steps (preprocess, OCR, scrub, verify).
- Export metrics in a format consistent with current service metrics approach.
- Add tests or lightweight assertions that metrics are emitted on requests.
"@
    },
    @{
        Number = 250
        Title = "Upload-to-Verification Session Abstraction"
        Body = @"
## Complexity Score: 200

### Description
Create a first-class session concept so multi-step verification flows are easier to reason about and retry.

### Requirements
- Define a session model (in-memory or lightweight persistence) with status transitions.
- Ensure idempotent handling of repeated client submissions for the same session.
- Add tests covering duplicate submissions, resume, and finalization behavior.
"@
    }
)

foreach ($issue in $issues) {
    Write-Host "`nFixing Issue #$( $issue.Number): $($issue.Title)" -ForegroundColor Cyan
    
    gh issue edit $issue.Number --repo $repo --body $issue.Body
    
    Start-Sleep -Seconds 1
}

Write-Host "`nAll issue descriptions added!" -ForegroundColor Green
