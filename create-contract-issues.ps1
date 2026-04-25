# Create Contract (Soroban) Issues in Bulk
$repo = "Pulsefy/Soter"
$label = "Soroban"

$issues = @(
    @{
        Title = "Expiry Extension with Safety Limits"
        Complexity = "150"
        Description = "Allow authorized operators to extend package expiry without recreating a package."
        Requirements = "- Implement \`extend_expiry(env: Env, id: u64, new_expires_at: u64)\`.
- Restrict the action to an authorized admin role and only if the package is still active.
- Emit an event that records the old and new expiry values."
    },
    @{
        Title = "Recipient Recovery / Delegate Address"
        Complexity = "200"
        Description = "Some recipients may lose access to their primary wallet and need a pre-approved recovery path."
        Requirements = "- Extend package storage to support an optional delegate or recovery address.
- Allow claim authorization by either the primary recipient or the approved delegate.
- Prevent delegate reassignment after claim unless a strict admin-controlled flow is defined and tested."
    },
    @{
        Title = "Partial Claim Support"
        Complexity = "200"
        Description = "Enable controlled partial disbursements for packages that should be claimed in stages instead of all at once."
        Requirements = "- Track claimed amount and remaining amount per package.
- Prevent over-claiming and ensure package status transitions remain consistent.
- Update tests and aggregate views to account for partially claimed packages."
    },
    @{
        Title = "Cancel-and-Reissue Flow"
        Complexity = "150"
        Description = "Operators should be able to cancel a package and reissue a replacement without losing the audit trail."
        Requirements = "- Implement a reissue flow that links a new package ID to the cancelled original.
- Ensure locked balances are not double-counted across the old and new package.
- Emit events that make the relationship between old and new IDs explicit."
    },
    @{
        Title = "Action-Specific Pause Controls"
        Complexity = "200"
        Description = "A single emergency stop is often too blunt. The contract should support pausing only the risky action being mitigated."
        Requirements = "- Add independent pause flags for actions such as create, claim, and withdraw.
- Require admin authorization for pause and unpause operations.
- Add event coverage and tests showing paused actions fail while unaffected actions still work."
    },
    @{
        Title = "Event Schema Version Tagging"
        Complexity = "100"
        Description = "Off-chain indexers need a stable way to detect event payload changes over time."
        Requirements = "- Add a version marker to emitted events or event topics.
- Keep the versioning strategy consistent across create, claim, revoke, and admin events.
- Update snapshot tests to lock in the new schema format."
    },
    @{
        Title = "Per-Campaign Funding Caps"
        Complexity = "150"
        Description = "Campaigns should be prevented from locking more value than their configured on-chain budget allows."
        Requirements = "- Add campaign budget tracking keyed by \`campaign_id\` and token.
- Validate new package creation against the remaining campaign budget.
- Provide a view for remaining budget and total locked budget per campaign."
    },
    @{
        Title = "Merkle-Based Recipient Allowlist"
        Complexity = "200"
        Description = "Large distributions may require compressing recipient eligibility data instead of storing every recipient list item on-chain."
        Requirements = "- Add optional Merkle root storage for allowlisted recipient claims.
- Update claim flow to verify a provided Merkle proof before transfer.
- Keep the feature optional so the simpler direct-recipient flow still works."
    },
    @{
        Title = "Claim Window Start Time"
        Complexity = "100"
        Description = "Some aid packages should not be claimable immediately after creation."
        Requirements = "- Add \`claim_starts_at\` to the package model.
- Reject claims that arrive before the allowed start time.
- Cover edge cases where \`claim_starts_at\` equals creation time or expiry time."
    },
    @{
        Title = "Invariant Assertion Test Suite"
        Complexity = "150"
        Description = "The contract should continuously prove that core accounting invariants hold across every lifecycle transition."
        Requirements = "- Add tests that assert locked totals, claim totals, and surplus accounting remain consistent.
- Cover mixed flows including create, claim, revoke, reissue, and partial-claim scenarios where relevant.
- Fail tests loudly when any storage counter diverges from expected balances."
    },
    @{
        Title = "Token Decimal Safety and Amount Normalization"
        Complexity = "150"
        Description = "Different tokens may use different decimals, and package amounts should be handled consistently across integrations."
        Requirements = "- Define and document how token amounts are normalized or validated before storage.
- Reject invalid zero, negative-equivalent, or precision-breaking inputs.
- Add tests for tokens with different decimal conventions and boundary values."
    }
)

foreach ($issue in $issues) {
    $body = @"
## Complexity Score: $($issue.Complexity)

### Description
$($issue.Description)

### Requirements
$($issue.Requirements)
"@

    Write-Host "`nCreating: $($issue.Title) (Complexity: $($issue.Complexity))" -ForegroundColor Cyan
    
    $escapedBody = $body -replace '"', '\"' -replace '`', '``'
    
    & gh issue create --repo $repo --title $issue.Title --body $body --label $label
    
    Start-Sleep -Seconds 3
}

Write-Host "`n=== All Soroban contract issues created! ===" -ForegroundColor Green
