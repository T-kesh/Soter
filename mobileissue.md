# Wave 4: Mobile App Issues for Soter

Wave 4 focuses on field resilience, operator workflows, accessibility, and stronger mobile reliability for aid recipients and NGO teams.

Complexity score scale:
- **100**: Beginner - Screen polish, navigation, or focused local-state work.
- **150**: Intermediate - API-backed flows, background sync, or richer device UX.
- **200**: Advanced - Offline-first workflows, platform integration, or complex state handling.

---

### Issue 1: Manual Review Status Inbox
**Complexity Score: 150**

#### Description
Recipients and operators should be able to see when a verification is waiting on manual review and what action is needed next.

#### Requirements
- Add an inbox or status center screen for verification cases.
- Show states such as `pending_review`, `approved`, `rejected`, and `needs_resubmission`.
- Provide clear next-step messaging and deep links into the relevant screen.

---

### Issue 2: Draft Autosave for Verification Forms
**Complexity Score: 100**

#### Description
Users in unstable network conditions should not lose partially completed verification progress.

#### Requirements
- Persist draft form state locally for in-progress verification flows.
- Restore drafts when the user reopens the app or returns to the screen.
- Add a clear discard/reset option so stale drafts can be removed intentionally.

---

### Issue 3: Background Sync for Pending Actions
**Complexity Score: 200**

#### Description
Pending uploads, claim confirmations, and status refreshes should retry automatically when the device regains connectivity.

#### Requirements
- Queue pending network actions locally with retry metadata.
- Trigger background or foreground sync when connectivity returns.
- Surface sync state to the user so they know whether actions are still pending.

---

### Issue 4: Push Notification Deep Links
**Complexity Score: 150**

#### Description
Important claim and verification updates should open directly to the relevant screen from a push notification.

#### Requirements
- Integrate push notifications for key lifecycle updates.
- Support deep links into package details, review status, and settings screens.
- Handle cold-start, background, and foreground notification tap scenarios.

---

### Issue 5: NGO Bulk Scan Session Mode
**Complexity Score: 150**

#### Description
Field operators often need to process many recipients in one session without bouncing through repeated navigation flows.

#### Requirements
- Add a session mode optimized for repeated package lookups or scans.
- Keep the operator on a fast loop for success, failure, and retry handling.
- Show session totals such as scanned, verified, failed, and skipped counts.

---

### Issue 6: Secure Offline Evidence Queue
**Complexity Score: 200**

#### Description
Evidence captured in the field should be stored safely until it can be uploaded.

#### Requirements
- Queue pending evidence files locally with encrypted or protected storage where feasible.
- Track upload status per file and allow manual retry or removal.
- Prevent duplicate uploads when the same queued item is retried multiple times.

---

### Issue 7: Multilingual App Copy and Locale Switching
**Complexity Score: 150**

#### Description
Soter's field usage will span diverse regions, so the app should support multiple languages from the start.

#### Requirements
- Externalize user-facing copy into translation resources.
- Add a locale setting with at least one secondary language path prepared.
- Ensure dates, numbers, and status labels respect locale formatting.

---

### Issue 8: Accessibility Pass for Screen Readers
**Complexity Score: 100**

#### Description
Core mobile flows should be usable with VoiceOver, TalkBack, and larger text settings.

#### Requirements
- Audit important screens for accessibility labels, roles, and focus order.
- Improve contrast and tap targets where needed.
- Verify the app remains usable under larger font sizes without broken layouts.

---

### Issue 9: Claim Receipt Share Sheet
**Complexity Score: 100**

#### Description
Recipients and NGO operators may need a simple proof that a claim or verification step was completed.

#### Requirements
- Add a shareable claim receipt view or summary card.
- Include core details such as package ID, status, timestamp, and token amount.
- Support native share-sheet integration for sending the receipt externally.

---

### Issue 10: Wallet Session Recovery and Connection Health
**Complexity Score: 150**

#### Description
Wallet disconnects and stale sessions should be easy to diagnose and recover from on mobile.

#### Requirements
- Detect broken or expired wallet sessions and show actionable recovery steps.
- Add reconnect and reset flows without requiring a full app restart.
- Surface basic connection health indicators in wallet-related screens.

---

### Issue 11: In-App Release Notes and Force-Upgrade Gate
**Complexity Score: 150**

#### Description
Critical mobile fixes may require users to update quickly, while non-critical updates should still be communicated clearly.

#### Requirements
- Add a lightweight release-notes surface for new app versions.
- Support a configurable force-upgrade gate for unsupported builds.
- Ensure blocked users still see a clear explanation and store update path.

---

### Issue 12: Field Location Capture with Consent
**Complexity Score: 150**

#### Description
Some field workflows benefit from optional location context, but it must be collected transparently and only with consent.

#### Requirements
- Add optional location capture during selected verification or delivery flows.
- Show a clear consent prompt and explain why the location is being requested.
- Handle denied permissions gracefully without blocking unrelated app features.

---

### Issue 13: App Diagnostics Screen
**Complexity Score: 100**

#### Description
Support teams need a quick way to inspect environment, API, and device state when debugging field reports.

#### Requirements
- Add a diagnostics screen showing app version, environment, API reachability, and network state.
- Include safe copy-to-clipboard actions for non-sensitive diagnostics.
- Ensure no secrets or tokens are exposed in the UI.

---

### Issue 14: NGO Assignment and Task List Screen
**Complexity Score: 150**

#### Description
Operators should be able to see the packages or cases assigned to them for the current field session.

#### Requirements
- Add a task list screen with assigned packages, due state, and current status.
- Support pull-to-refresh and offline last-known data.
- Allow quick navigation from a task item into detail, scan, or verification actions.

---

### Issue 15: Battery and Data Saver Mode
**Complexity Score: 150**

#### Description
The app should degrade gracefully on older devices and expensive data connections.

#### Requirements
- Add a saver mode that reduces polling, disables heavy media previews, and limits background refresh.
- Let users toggle the mode manually and optionally auto-enable it under poor conditions.
- Show when saver mode is active so reduced behavior is understandable.
