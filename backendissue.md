
# Wave 4: Backend Issues for Soter

Wave 4 focuses on operational maturity, admin workflows, data governance, and safer multi-tenant scaling for the NestJS backend.

Complexity score scale:
- **100**: Beginner - Focused endpoint, guard, or DTO enhancement.
- **150**: Intermediate - Multi-module flow, service orchestration, or admin workflow.
- **200**: Advanced - Cross-cutting reliability, security, or data lifecycle work.

---

### Issue 1: Organization-Scoped Audit Log Export API
**Complexity Score: 150**

#### Description
Allow admins to export filtered audit logs for compliance reviews and incident investigations.

#### Requirements
- Add `GET /audit/export` with filters for organization, actor, action, and date range.
- Support CSV and JSON outputs without loading the entire dataset into memory.
- Enforce role and org-ownership checks so tenants cannot export each other's logs.

---

### Issue 2: Idempotency Keys for Mutating Endpoints
**Complexity Score: 200**

#### Description
Make critical write operations retry-safe so duplicate requests do not create duplicate campaigns, aid packages, or claims.

#### Requirements
- Add idempotency-key handling for high-value POST endpoints such as campaign creation, aid creation, and claim submission.
- Persist request fingerprints and replay the original response for safe retries.
- Add unit and e2e coverage for duplicate submissions, expired keys, and body mismatches.

---

### Issue 3: Bulk Recipient Import Validation Pipeline
**Complexity Score: 150**

#### Description
NGO operators need a safe way to import recipient lists in bulk with clear validation feedback before records are committed.

#### Requirements
- Add an import endpoint that accepts CSV uploads or parsed rows.
- Validate required fields, duplicate recipients, invalid wallet addresses, and malformed amounts.
- Return a structured validation report that separates blocking errors from warnings.

---

### Issue 4: Manual Verification Review Queue API
**Complexity Score: 150**

#### Description
Introduce a backend workflow for verifications that cannot be auto-resolved by the AI service and require human review.

#### Requirements
- Add queue/list endpoints for `pending_review`, `approved`, and `rejected` verification cases.
- Allow authorized reviewers to submit a decision, reason, and optional internal note.
- Record the review action in the audit trail and expose timestamps for SLA tracking.

---

### Issue 5: Resumable Evidence Upload Sessions
**Complexity Score: 200**

#### Description
Large evidence uploads should survive unstable networks and support resume semantics instead of restarting from zero.

#### Requirements
- Add upload-session creation and chunk/finalize endpoints for verification evidence.
- Track session state, chunk ordering, and upload expiry.
- Validate content type, size limits, and ownership before finalizing an upload.

---

### Issue 6: Campaign Budget Threshold Alerts
**Complexity Score: 150**

#### Description
Campaign owners should be warned when budget usage crosses important thresholds so funding gaps are caught early.

#### Requirements
- Add budget utilization calculations for configurable thresholds such as 50%, 80%, and 95%.
- Trigger internal notification jobs when a threshold is crossed for the first time.
- Prevent duplicate alerts for the same threshold unless the campaign is reset or reconfigured.

---

### Issue 7: API Key Rotation and Last-Used Tracking
**Complexity Score: 150**

#### Description
Strengthen service-to-service security by allowing safer API key lifecycle management.

#### Requirements
- Add endpoints to create, rotate, revoke, and list API keys with masked previews only.
- Track `lastUsedAt`, `createdBy`, and revocation metadata.
- Ensure revoked keys fail authorization immediately and add tests around rotation edge cases.

---

### Issue 8: Unified Search Endpoint for Admin Entities
**Complexity Score: 150**

#### Description
Operators need a fast way to search across campaigns, claims, recipients, and verification records from one admin search box.

#### Requirements
- Add a search endpoint that supports keyword matching plus optional entity filters.
- Return lightweight results with entity type, primary label, status, and navigation ID.
- Keep the response tenant-scoped and add indexes or query tuning where needed.

---

### Issue 9: Signed Artifact Access for Verification Evidence
**Complexity Score: 200**

#### Description
Sensitive evidence files should never be exposed through permanent public URLs.

#### Requirements
- Add short-lived signed download access for verification artifacts.
- Enforce role checks and org ownership before issuing a signed URL or proxy response.
- Log every artifact access event for later review.

---

### Issue 10: Route-Level Adaptive Rate Limiting
**Complexity Score: 150**

#### Description
Different API surfaces have different abuse profiles, so a single global limit is too coarse.

#### Requirements
- Apply route-specific rate limits for auth-like operations, verification starts, and search endpoints.
- Support stricter limits for anonymous/public routes and more permissive limits for trusted API keys.
- Add tests covering limit exhaustion, reset behavior, and tenant isolation.

---

### Issue 11: Data Retention and Purge Workflows
**Complexity Score: 200**

#### Description
Operational data and PII should follow explicit retention policies instead of growing indefinitely.

#### Requirements
- Define retention windows for audit logs, evidence artifacts, and verification session records.
- Add purge jobs that soft-delete or hard-delete data according to policy.
- Produce an audit event whenever a retention purge removes or anonymizes records.

---

### Issue 12: Versioned API Deprecation Headers
**Complexity Score: 100**

#### Description
Consumers need advance warning when endpoints or response fields are being phased out.

#### Requirements
- Add reusable helpers for `Deprecation`, `Sunset`, and replacement-link headers.
- Apply the helpers to at least one deprecated route or field path in the API.
- Document and test the header behavior in the e2e suite.

---

### Issue 13: Analytics Snapshot Caching Layer
**Complexity Score: 150**

#### Description
High-traffic dashboards should be able to serve recent analytics without recomputing every request.

#### Requirements
- Cache expensive analytics responses with explicit TTL and cache-key rules.
- Add targeted cache invalidation when campaigns, claims, or aid packages change state.
- Expose cache hit/miss metrics so performance gains are measurable.

---

### Issue 14: Correlation ID Propagation into Background Jobs
**Complexity Score: 150**

#### Description
Tracing a request from HTTP entrypoint into notification, verification, and on-chain jobs should be straightforward during incident response.

#### Requirements
- Pass correlation IDs from inbound requests into queued jobs and downstream logs.
- Update job payload interfaces to preserve trace context safely.
- Add tests proving correlation IDs appear consistently in job processing logs.

---

### Issue 15: Replay-Safe AI Callback Processing
**Complexity Score: 150**

#### Description
AI callback endpoints should ignore duplicate deliveries and safely handle out-of-order webhook retries.

#### Requirements
- Add event or delivery identifiers to callback processing and reject exact duplicates.
- Prevent stale callback payloads from overwriting newer verification states.
- Add tests for duplicate, delayed, and conflicting callback deliveries.

---

### Issue 16: Organization Membership Invitation Flow
**Complexity Score: 150**

#### Description
Create a proper backend flow for inviting staff into an NGO organization with controlled roles.

#### Requirements
- Add invitation create, accept, revoke, and list endpoints.
- Support role assignment during invite acceptance with validation against allowed role scopes.
- Expire unused invites automatically and record all invite actions in the audit module.

---

### Issue 17: Internal Notes Timeline for Claims and Verifications
**Complexity Score: 100**

#### Description
Operators need a secure place to store investigation notes without exposing them to recipients.

#### Requirements
- Add internal note create/list endpoints for claims and verification records.
- Store author, timestamp, and optional category metadata on each note.
- Restrict note visibility to staff roles only and include audit coverage.

---

### Issue 18: CSV Export Endpoints for Claims and Campaigns
**Complexity Score: 100**

#### Description
Operations teams often need spreadsheet-ready exports for reporting and donor reconciliation.

#### Requirements
- Add CSV export endpoints for campaign summaries and claim records.
- Support standard filter inputs such as date range, status, organization, and token.
- Ensure exported fields exclude secrets and sensitive internal-only data.

---

### Issue 19: Notification Outbox Pattern for Reliable Dispatch
**Complexity Score: 200**

#### Description
Notification requests should be persisted before dispatch so transient worker failures do not silently lose messages.

#### Requirements
- Introduce an outbox table or queue-backed persistence model for notification intents.
- Mark items through lifecycle states such as `pending`, `sent`, and `failed`.
- Add retry metadata and observability for stuck or aging outbox records.

---

### Issue 20: Seeded Demo Tenant and Sandbox Admin Endpoints
**Complexity Score: 100**

#### Description
Contributors and reviewers need a fast way to spin up realistic demo data for local development and previews.

#### Requirements
- Add protected sandbox-only endpoints or scripts to generate demo organizations, campaigns, and claims.
- Keep the feature disabled outside local or explicitly enabled demo environments.
- Document the seed shapes in code comments or DTO examples so contributors can extend them safely.
