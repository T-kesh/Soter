# Add appropriate labels to all open issues in Soter repo
$repo = "Pulsefy/Soter"

# Get all open issues
$issues = gh issue list --repo $repo --state open --limit 100 --json number,title,labels | ConvertFrom-Json

foreach ($issue in $issues) {
    $issueNum = $issue.number
    $title = $issue.title.ToLower()
    $labels = @()
    
    # Determine labels based on issue title keywords
    
    # Backend-related issues
    if ($title -match "backend|api|nest|endpoint|controller|service|module|database|prisma|query") {
        $labels += "Backend"
    }
    
    # Database-specific
    if ($title -match "database|prisma|query|index|migration|schema") {
        $labels += "database"
    }
    
    # Frontend-related issues
    if ($title -match "frontend|ui|component|dashboard|page|screen|navigation|button|form") {
        $labels += "Frontend"
    }
    
    # UX improvements
    if ($title -match "ux|user experience|usability|accessibility|responsive|mobile-friendly") {
        $labels += "ux"
    }
    
    # Soroban/Smart Contract issues
    if ($title -match "soroban|contract|escrow|on-chain|onchain|blockchain|stellar|wallet|claim") {
        $labels += "Soroban"
    }
    
    # AI Service issues
    if ($title -match "ai|ocr|verification|pii|scrubber|anonymization|proof-of-life|evidence") {
        $labels += "ai-service"
        $labels += "python"
    }
    
    # Security issues
    if ($title -match "security|hmac|authentication|authorization|encryption|cors|rate.limit|vulnerability|attack") {
        $labels += "security"
    }
    
    # Testing issues
    if ($title -match "test|e2e|unit test|coverage|jest|pytest|test suite|validation") {
        $labels += "testing"
    }
    
    # Performance issues
    if ($title -match "performance|optimization|cache|profiling|index|slow|bottleneck") {
        $labels += "performance"
    }
    
    # Architecture issues
    if ($title -match "architecture|refactor|design pattern|abstraction|modular") {
        $labels += "architecture"
    }
    
    # Mobile-specific
    if ($title -match "mobile|expo|react native|ios|android|app") {
        $labels += "Mobile"
    }
    
    # Analytics
    if ($title -match "analytics|metrics|monitoring|dashboard.*stat|tracking|reporting") {
        $labels += "analytics"
    }
    
    # Governance
    if ($title -match "governance|vote|approval|proposal|decision") {
        $labels += "governance"
    }
    
    # Infrastructure
    if ($title -match "docker|ci|cd|deploy|infrastructure|github.action|workflow|pipeline") {
        $labels += "infrastructure"
    }
    
    # Product features
    if ($title -match "campaign|recipient|aid.*package|donor|ngood") {
        $labels += "product"
    }
    
    # Workflow automation
    if ($title -match "workflow|automation|queue|background.*job|cron|scheduled") {
        $labels += "workflow"
    }
    
    # Remove duplicates
    $labels = $labels | Select-Object -Unique
    
    # Add labels if we found any
    if ($labels.Count -gt 0) {
        Write-Host "`nIssue #$issueNum : $title" -ForegroundColor Cyan
        Write-Host "  Adding labels: $($labels -join ', ')" -ForegroundColor Yellow
        
        $labelArgs = $labels | ForEach-Object { "--add-label `"$_`"" }
        $labelString = $labelArgs -join " "
        
        $cmd = "gh issue edit $issueNum --repo $repo $labelString"
        Invoke-Expression $cmd
        
        Start-Sleep -Seconds 1
    }
}

Write-Host "`n=== All issues labeled! ===" -ForegroundColor Green
