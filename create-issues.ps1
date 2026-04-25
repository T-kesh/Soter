# Bulk Issue Creator for Soter
# Reads issue definitions from markdown files and creates them on GitHub

$repo = "Pulsefy/Soter"

# Function to parse and create issues from a markdown file
function Create-IssuesFromFile {
    param (
        [string]$FilePath,
        [string]$Label
    )

    $content = Get-Content -Path $FilePath -Raw
    $issues = @()
    
    # Split by issue pattern (### Issue or ### Issue)
    $issueBlocks = $content -split '(?=### Issue \d+:)'
    
    foreach ($block in $issueBlocks) {
        if ($block -match "### Issue \d+: (.+)") {
            $title = $matches[1]
            
            # Extract complexity score
            $complexityMatch = $block -match "\*\*Complexity Score: (\d+)\*\*"
            $complexity = if ($complexityMatch) { $matches[1] } else { "N/A" }
            
            # Extract description and requirements
            $body = @"
## Complexity Score: $complexity

$(if ($block -match "#### Description\s+(.+?)(?=#### Requirements|\Z)" -or $block -match "#### Description\s+(.+?)\s+---") {
    $desc = $matches[1].Trim()
    "### Description`n$desc"
} else { "" })

$(if ($block -match "#### Requirements\s+(.+?)(?=---|\Z)" -or $block -match "#### Requirements\s+(.+?)\s+---") {
    $req = $matches[1].Trim()
    "### Requirements`n$req"
} else { "" })
"@

            # Remove any trailing whitespace
            $body = $body.Trim()
            
            Write-Host "`nCreating issue: $title (Complexity: $complexity)"
            
            # Create the issue
            $command = "gh issue create --repo $repo --title `"$title`" --body `"$body`" --label `"$Label`""
            Invoke-Expression $command
            
            Start-Sleep -Seconds 2  # Rate limiting pause
        }
    }
}

# Create issues from each file
Write-Host "=== Creating AI Service Issues ===" -ForegroundColor Cyan
Create-IssuesFromFile -FilePath "ai-service.md" -Label "ai-service"

Write-Host "`n=== Creating Contract Issues ===" -ForegroundColor Cyan
Create-IssuesFromFile -FilePath "issues_contract.md" -Label "smart-contract"

Write-Host "`n=== Creating Backend Issues ===" -ForegroundColor Cyan
Create-IssuesFromFile -FilePath "backendissue.md" -Label "backend"

Write-Host "`n=== Creating Frontend Issues ===" -ForegroundColor Cyan
Create-IssuesFromFile -FilePath "frontendissue.md" -Label "frontend"

Write-Host "`n=== Creating Mobile Issues ===" -ForegroundColor Cyan
Create-IssuesFromFile -FilePath "mobileissue.md" -Label "mobile"

Write-Host "`n=== All issues created! ===" -ForegroundColor Green
