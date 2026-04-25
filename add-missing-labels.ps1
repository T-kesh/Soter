$repo = "Pulsefy/Soter"

$issues = @(
    @{Number=289; Title="Battery and Data Saver Mode"; Labels=@("Mobile")},
    @{Number=287; Title="Field Location Capture with Consent"; Labels=@("Mobile")},
    @{Number=286; Title="Wallet Session Recovery and Connection Health"; Labels=@("Mobile")},
    @{Number=274; Title="Add Structured Logging with Redaction Guarantees"; Labels=@("Backend")},
    @{Number=275; Title="Saved Filter Presets and Shareable URLs"; Labels=@("Frontend")},
    @{Number=273; Title="Empty-State Onboarding and Demo Data Prompts"; Labels=@("Frontend")},
    @{Number=271; Title="Evidence Artifact Viewer with Redaction States"; Labels=@("Frontend")},
    @{Number=269; Title="Request Correlation ID Propagation"; Labels=@("Backend")},
    @{Number=245; Title="Harden Form Upload Validation and Limits"; Labels=@("Backend", "security")},
    @{Number=244; Title="Standardize Error Envelope Across All Routes"; Labels=@("Backend")}
)

foreach ($issue in $issues) {
    Write-Host "`nIssue #$($issue.Number): $($issue.Title)" -ForegroundColor Cyan
    Write-Host "  Adding labels: $($issue.Labels -join ', ')" -ForegroundColor Yellow
    
    $labelArgs = $issue.Labels | ForEach-Object { "--add-label `"$_`"" }
    $labelString = $labelArgs -join " "
    
    $cmd = "gh issue edit $($issue.Number) --repo $repo $labelString"
    Invoke-Expression $cmd
    
    Start-Sleep -Seconds 1
}

Write-Host "`nAll labels added!" -ForegroundColor Green
