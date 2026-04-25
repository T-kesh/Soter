# Wave 4: AI Service Issues for Soter
  
Wave 4 focuses on reliability, security, evaluation, and production readiness for the FastAPI-based AI service in [app/ai-service](file:///c:/Users/g-ekoh/Desktop/Soter/app/ai-service).
  
Complexity score scale:
- **100**: Beginner - Isolated endpoint/test improvements or small refactors.
- **150**: Intermediate - Multi-module changes, new flows, or measurable quality improvements.
- **200**: Advanced - Security, privacy, evaluation rigor, or architectural work.
  
---
  
### Issue 1: Standardize Error Envelope Across All Routes
**Complexity Score: 100**
  
#### Description
Unify error responses so the backend and frontend can reliably parse AI-service failures.
  
#### Requirements
- Implement a consistent JSON error envelope with `code`, `message`, and `details`.
- Ensure FastAPI exception handlers map validation errors, downstream errors, and internal errors into the envelope.
- Add tests that assert response shape for at least 5 representative failure cases.
  
---
  
### Issue 2: Request Correlation ID Propagation
**Complexity Score: 150**
  
#### Description
Enable end-to-end tracing by propagating correlation IDs through logs and outbound requests.
  
#### Requirements
- Accept `X-Request-Id` and/or generate one when missing.
- Include the correlation ID in every log line and outbound HTTP request headers.
- Add tests verifying correlation IDs are present in responses and logs for at least one route.
  
---
  
### Issue 3: Harden Form Upload Validation and Limits
**Complexity Score: 150**
  
#### Description
Improve security and stability for endpoints that accept evidence uploads or multipart form data.
  
#### Requirements
- Enforce maximum file size, allowed MIME types, and allowed file extensions.
- Reject ambiguous inputs (multiple files when only one is expected, missing fields, invalid filenames).
- Add tests for boundary sizes and malicious/invalid MIME scenarios.
  
---
  
### Issue 4: Add Structured Logging with Redaction Guarantees
**Complexity Score: 200**
  
#### Description
Move to structured logs while ensuring PII never leaks to logs.
  
#### Requirements
- Adopt JSON structured logging with a stable schema (timestamp, level, requestId, route, latencyMs, outcome).
- Ensure redaction is applied to all known sensitive fields before logging.
- Add tests that confirm PII-like strings are not present in logs for key endpoints.
  
---
  
### Issue 5: Improve PII Scrubber Coverage with Regression Test Set
**Complexity Score: 150**
  
#### Description
Increase confidence that PII scrubbing is correct and stays correct over time.
  
#### Requirements
- Create a curated set of anonymization fixtures (emails, phone numbers, IDs, addresses, names).
- Add unit tests that validate expected transformations and non-destructive behavior on safe text.
- Include at least one “false positive” guard test to prevent over-redaction.
  
---
  
### Issue 6: Deterministic Test Mode for AI Outputs
**Complexity Score: 150**
  
#### Description
Make tests stable by offering deterministic behavior for AI-driven steps.
  
#### Requirements
- Add a test mode config that forces deterministic results for verification scoring and classification.
- Ensure the mode can be enabled via environment variable in CI.
- Add tests that confirm deterministic outputs remain stable across runs.
  
---
  
### Issue 7: Add Health Check with Dependency Probes
**Complexity Score: 100**
  
#### Description
Expose a health endpoint that validates not just “process is alive” but “service is healthy.”
  
#### Requirements
- Add a `GET /health` endpoint (or expand existing) to include dependency checks (e.g., model availability, filesystem/temp access).
- Return a minimal, stable JSON shape with status and version info.
- Add tests asserting behavior for healthy and simulated-unhealthy states.
  
---
  
### Issue 8: Introduce Versioned API Routes for AI Service
**Complexity Score: 150**
  
#### Description
Prepare for non-breaking evolution by versioning the API surface.
  
#### Requirements
- Add a version prefix strategy (e.g., `/v1`) for all routes.
- Keep backwards compatibility with non-versioned routes temporarily via redirects or dual mounting.
- Add tests that ensure both paths behave consistently (where intended).
  
---
  
### Issue 9: Evidence Preprocessing Pipeline Metrics
**Complexity Score: 150**
  
#### Description
Measure and monitor preprocessing costs (OCR, normalization, scrubbing) to prevent regressions.
  
#### Requirements
- Add timing metrics for major pipeline steps (preprocess, OCR, scrub, verify).
- Export metrics in a format consistent with current service metrics approach.
- Add tests or lightweight assertions that metrics are emitted on requests.
  
---
  
### Issue 10: Upload-to-Verification “Session” Abstraction
**Complexity Score: 200**
  
#### Description
Create a first-class session concept so multi-step verification flows are easier to reason about and retry.
  
#### Requirements
- Define a session model (in-memory or lightweight persistence) with status transitions.
- Ensure idempotent handling of repeated client submissions for the same session.
- Add tests covering duplicate submissions, resume, and finalization behavior.
  
---
  
### Issue 11: Strict OpenAPI Schema and Examples for All Routes
**Complexity Score: 100**
  
#### Description
Improve contributor velocity by ensuring the AI service OpenAPI docs are complete and accurate.
  
#### Requirements
- Ensure all endpoints have accurate request/response models.
- Add at least one valid example payload per route.
- Add tests (or CI checks) that fail when OpenAPI generation breaks.
  
---
  
### Issue 12: Add Security Headers and CORS Policy Review
**Complexity Score: 150**
  
#### Description
Lock down defaults to reduce exposure in deployed environments.
  
#### Requirements
- Add explicit CORS configuration with environment-based allowlists.
- Ensure recommended security headers are present for API responses where applicable.
- Add tests for CORS behavior and header presence.
  
---
  
### Issue 13: Rate Limit High-Cost Endpoints
**Complexity Score: 150**
  
#### Description
Prevent abuse and cost blowups by rate limiting endpoints that trigger expensive processing.
  
#### Requirements
- Apply route-level rate limiting for OCR and verification endpoints.
- Use a strategy compatible with multi-instance deployments (avoid in-memory-only limits).
- Add tests for limit exhaustion and reset behavior.
  
---
  
### Issue 14: Golden Dataset Evaluation Harness
**Complexity Score: 200**
  
#### Description
Introduce a reproducible evaluation harness so changes can be measured against known-good datasets.
  
#### Requirements
- Define a golden dataset format for inputs and expected outputs (scrubbing, OCR, verification scoring bands).
- Add a command or test suite that runs evaluation and outputs a summary report.
- Add CI gating that prevents large regressions in key metrics.
  
---
  
### Issue 15: Add Background Task Queue Interface Stub
**Complexity Score: 150**
  
#### Description
Prepare the AI service for async processing without committing to a single queue implementation immediately.
  
#### Requirements
- Define an abstraction interface for enqueueing and processing AI tasks (OCR, verification).
- Add a local in-process implementation for development/testing.
- Add tests that validate task submission, processing, and error capture semantics.
