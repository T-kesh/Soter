# Wave 4: Frontend Issues for Soter

Wave 4 focuses on admin productivity, safer transaction UX, contributor-friendly polish, and stronger dashboard workflows for the Next.js frontend.

Complexity score scale:
- **100**: Beginner - UI polish, routing, or focused component work.
- **150**: Intermediate - New data flow, dashboard workflow, or role-aware UX.
- **200**: Advanced - Complex state, transaction UX, or performance-sensitive features.

---

### Issue 1: Manual Verification Review Dashboard
**Complexity Score: 150**

#### Description
Build a staff-facing dashboard for reviewing verification cases that were flagged for manual review.

#### Requirements
- Add a review queue page with filters for status, risk level, and date.
- Show evidence summary, AI score, and reviewer decision history.
- Wire approve/reject actions to the backend with optimistic UI states and error recovery.

---

### Issue 2: Bulk Recipient Import Wizard
**Complexity Score: 150**

#### Description
Create a guided UI for uploading recipient lists and resolving validation issues before import.

#### Requirements
- Add a multi-step import wizard for file upload, preview, validation, and confirmation.
- Surface row-level errors and warnings clearly.
- Allow users to download a validation report for correction.

---

### Issue 3: Audit Trail Explorer
**Complexity Score: 150**

#### Description
Admins need a searchable interface to inspect audit activity across campaigns, claims, and staff actions.

#### Requirements
- Build an audit explorer page with filters for actor, action, entity type, and date range.
- Support pagination and empty/error states.
- Add export actions that connect to the audit export backend endpoint.

---

### Issue 4: Role-Aware Navigation Shell
**Complexity Score: 100**

#### Description
Navigation should adapt to the signed-in user's role so operators only see relevant tools.

#### Requirements
- Update the main navigation to show or hide items based on role.
- Add clear access-denied handling for restricted routes.
- Keep the role logic centralized so future permissions stay maintainable.

---

### Issue 5: Transaction Activity Center
**Complexity Score: 150**

#### Description
Users need one place to track pending, succeeded, and failed on-chain actions triggered from the UI.

#### Requirements
- Add an activity center component for transaction and job statuses.
- Show timestamps, current step, retry guidance, and explorer links where relevant.
- Persist recent activity locally so refreshes do not erase context.

---

### Issue 6: API Key Management Settings Page
**Complexity Score: 150**

#### Description
Provide an admin UI for viewing, rotating, and revoking service API keys without leaving the product.

#### Requirements
- Add a settings page for API key lifecycle actions.
- Show masked key previews, creator, creation date, and last-used timestamps.
- Require confirmation before revoke or rotate actions.

---

### Issue 7: Campaign Budget Alert Widgets
**Complexity Score: 100**

#### Description
Expose budget threshold warnings directly on campaign views so funding risk is visible without opening reports.

#### Requirements
- Add warning badges or cards for threshold crossings such as 50%, 80%, and 95%.
- Show remaining budget, utilization percentage, and last-updated time.
- Ensure alert states are accessible and responsive.

---

### Issue 8: Analytics Export UX
**Complexity Score: 100**

#### Description
Operations teams need polished export controls for campaign, claim, and analytics reporting.

#### Requirements
- Add export buttons with format selection and filter-aware exports.
- Show loading, success, and failure feedback for export generation.
- Prevent duplicate export submissions while a request is already in progress.

---

### Issue 9: Evidence Artifact Viewer with Redaction States
**Complexity Score: 150**

#### Description
Staff reviewing evidence should be able to inspect files safely and understand what has already been redacted or anonymized.

#### Requirements
- Build an artifact viewer for images and documents with metadata panels.
- Show privacy/redaction status, access warnings, and download restrictions.
- Handle expired or unauthorized artifact links gracefully.

---

### Issue 10: Optimistic Mutation UX for Campaign Actions
**Complexity Score: 150**

#### Description
Improve perceived performance for common admin actions such as pause, archive, and update workflows.

#### Requirements
- Add optimistic state updates for safe campaign mutations.
- Roll back UI state cleanly when the backend rejects a mutation.
- Standardize toast and inline feedback patterns across mutation-heavy screens.

---

### Issue 11: Empty-State Onboarding and Demo Data Prompts
**Complexity Score: 100**

#### Description
New contributors and reviewers should immediately understand how to explore the app when real data is missing.

#### Requirements
- Improve empty states across dashboard, campaigns, and verification views.
- Add clear CTA paths for creating sample data or viewing docs/help.
- Keep the messaging role-aware so recipients and admins see different guidance.

---

### Issue 12: Saved Filter Presets and Shareable URLs
**Complexity Score: 150**

#### Description
Teams often revisit the same filtered views, so dashboards should support reusable presets and sharable URL state.

#### Requirements
- Allow users to save named filter presets for major admin lists.
- Sync filters with URL parameters for easy sharing and bookmarking.
- Support restoring defaults and deleting stale presets.

---

### Issue 13: Unified Error Recovery UX
**Complexity Score: 150**

#### Description
Wallet, API, and network failures should guide users toward recovery instead of leaving them stranded.

#### Requirements
- Standardize error surfaces for fetch failures, rejected signatures, and transient backend outages.
- Add retry actions, support hints, and context-aware remediation steps.
- Ensure errors are readable on both desktop and mobile breakpoints.

---

### Issue 14: Organization Members and Invite Management UI
**Complexity Score: 150**

#### Description
Add a team management interface so organizations can invite staff and manage roles from the frontend.

#### Requirements
- Build a members page with active users, pending invites, and role chips.
- Support invite creation, revoke, resend, and accept flows.
- Show audit-friendly timestamps such as invited at, accepted at, and revoked at.

---

### Issue 15: Dashboard Performance Optimization Pass
**Complexity Score: 200**

#### Description
As more widgets land, the dashboard should remain responsive on lower-end devices and weak connections.

#### Requirements
- Audit bundle-heavy components and add lazy loading where appropriate.
- Reduce unnecessary re-renders in filter-heavy dashboard sections.
- Add lightweight measurements or profiling notes so future regressions are easier to catch.
