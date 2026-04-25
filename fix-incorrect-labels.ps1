# Fix incorrect labels on issues
$repo = "Pulsefy/Soter"

# Get all open issues
$issues = gh issue list --repo $repo --state open --limit 100 --json number,title,labels | ConvertFrom-Json

foreach ($issue in $issues) {
    $issueNum = $issue.number
    $title = $issue.title.ToLower()
    $labelsToRemove = @()
    $labelsToAdd = @()
    
    # Get current labels
    $currentLabels = $issue.labels | ForEach-Object { $_.name }
    
    Write-Host "`nChecking Issue #$issueNum : $($issue.title)" -ForegroundColor Cyan
    Write-Host "  Current labels: $($currentLabels -join ', ')" -ForegroundColor Yellow
    
    # Frontend issues - should ONLY have Frontend label if its clearly a frontend/UI task
    if ($title -match "dashboard|ui|component|navigation|page|screen|wizard|export.*ux|settings page|review dashboard|import wizard|audit.*explorer") {
        if ("Frontend" -notin $currentLabels) {
            $labelsToAdd += "Frontend"
        }
    }
    # Remove Frontend from non-frontend issues
    elseif ("Frontend" -in $currentLabels -and $title -notmatch "dashboard|ui|component|navigation|page|screen|wizard|export.*ux|settings page|review dashboard|import wizard|audit.*explorer") {
        $labelsToRemove += "Frontend"
    }
    
    # Mobile issues - should ONLY have Mobile label if its clearly a mobile app task
    if ($title -match "mobile.*app|expo.*screen|app.*diagnostics|release.*notes.*app|multilingual.*app|claim.*receipt|offline.*evidence|push.*notification|ngo.*scan.*session") {
        if ("Mobile" -notin $currentLabels) {
            $labelsToAdd += "Mobile"
        }
    }
    # Remove Mobile from non-mobile issues
    elseif ("Mobile" -in $currentLabels -and $title -notmatch "mobile.*app|expo.*screen|app.*diagnostics|release.*notes.*app|multilingual.*app|claim.*receipt|offline.*evidence|push.*notification|ngo.*scan.*session") {
        $labelsToRemove += "Mobile"
    }
    
    # Soroban issues - ONLY smart contract/blockchain issues
    if ($title -match "soroban|escrow.*contract|onchain.*adapter|claim.*window.*time|package.*listing|recipient.*package.*count|contract.*readme") {
        if ("Soroban" -notin $currentLabels) {
            $labelsToAdd += "Soroban"
        }
    }
    # Remove Soroban from non-Soroban issues  
    elseif ("Soroban" -in $currentLabels -and $title -notmatch "soroban|escrow.*contract|onchain.*adapter|claim.*window.*time|package.*listing|recipient.*package.*count|contract.*readme|onchain.*module") {
        $labelsToRemove += "Soroban"
    }
    
    # AI Service issues - ONLY AI/ML/verification/OCR issues
    if ($title -match "ai.*service|ocr|verification|pii.*scrubber|proof.*life|evidence.*upload|ai.*fraud|camera.*integration.*evidence|deterministic.*test.*ai") {
        if ("ai-service" -notin $currentLabels) {
            $labelsToAdd += "ai-service"
            $labelsToAdd += "python"
        }
    }
    # Remove ai-service and python from non-AI issues
    elseif ("ai-service" -in $currentLabels -and $title -notmatch "ai.*service|ocr|verification|pii.*scrubber|proof.*life|evidence.*upload|ai.*fraud|camera.*integration.*evidence|deterministic.*test.*ai") {
        $labelsToRemove += "ai-service"
        $labelsToRemove += "python"
    }
    
    # Remove labels if needed
    if ($labelsToRemove.Count -gt 0) {
        Write-Host "  Removing: $($labelsToRemove -join ', ')" -ForegroundColor Red
        
        $removeArgs = $labelsToRemove | ForEach-Object { "--remove-label `"$_`"" }
        $removeString = $removeArgs -join " "
        
        $cmd = "gh issue edit $issueNum --repo $repo $removeString"
        Invoke-Expression $cmd
        
        Start-Sleep -Seconds 1
    }
    
    # Add labels if needed
    if ($labelsToAdd.Count -gt 0) {
        Write-Host "  Adding: $($labelsToAdd -join ', ')" -ForegroundColor Green
        
        $addArgs = $labelsToAdd | ForEach-Object { "--add-label `"$_`"" }
        $addString = $addArgs -join " "
        
        $cmd = "gh issue edit $issueNum --repo $repo $addString"
        Invoke-Expression $cmd
        
        Start-Sleep -Seconds 1
    }
    
    if ($labelsToRemove.Count -eq 0 -and $labelsToAdd.Count -eq 0) {
        Write-Host "  Labels are correct" -ForegroundColor Green
    }
}

Write-Host "`nAll label corrections complete" -ForegroundColor Green
