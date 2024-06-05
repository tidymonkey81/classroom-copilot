# PowerShell script to manage project services

# Load environment variables from .env file
$envPath = ".\.env"
Get-Content $envPath | ForEach-Object {
    $keyValue = $_.Split('=')
    [System.Environment]::SetEnvironmentVariable($keyValue[0], $keyValue[1], [System.EnvironmentVariableTarget]::Process)
}

# Function to display menu and get user choice
function Show-Menu {
    param (
        [string]$Title = 'Select an option:'
    )
    Clear-Host
    Write-Host "================ $Title ================"
    
    Write-Host "1: Instantiate all containers using docker-compose"
    Write-Host "2: Instantiate backend and Neo4j using docker-compose"
    Write-Host "3: Instantiate only backend using docker-compose"
    Write-Host "4: Run frontend and backend directly on host machine"
    Write-Host "5: Run only frontend on host machine"
    Write-Host "6: Run only backend on host machine"
    Write-Host "Q: Quit"
}

# Main loop
do {
    Show-Menu
    $input = Read-Host "Please make a selection"
    switch ($input) {
        '1' {
            docker-compose up
        }
        '2' {
            docker-compose up cc_backend cc_neo4j
        }
        '3' {
            docker-compose up cc_backend
        }
        '4' {
            Start-Process -NoNewWindow -FilePath npm -ArgumentList "run", "dev" -WorkingDirectory "./frontend"
            Start-Process -NoNewWindow -FilePath uvicorn -ArgumentList "app.main:app", "--host", "0.0.0.0", "--port", "8000" -WorkingDirectory "./backend"
        }
        '5' {
            Start-Process -NoNewWindow -FilePath npm -ArgumentList "run", "dev" -WorkingDirectory "./frontend"
        }
        '6' {
            Start-Process -NoNewWindow -FilePath uvicorn -ArgumentList "app.main:app", "--host", "0.0.0.0", "--port", "8000" -WorkingDirectory "./backend"
        }
        'Q' {
            return
        }
        default {
            Write-Host "Invalid option, please select a number from 1 to 6 or Q to quit."
        }
    }
    pause
}
while ($input -ne 'Q')