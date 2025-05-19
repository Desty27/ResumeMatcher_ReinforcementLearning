# Create directories
New-Item -ItemType Directory -Force -Path "app/parsers", "app/matching", "tests", "data/resumes", "data/job_descriptions"

# Create empty Python files
@("__init__", "main", "models", "database") | ForEach-Object {
    New-Item -ItemType File -Force -Path "app/$_.py"
}
@("__init__", "resume_parser") | ForEach-Object {
    New-Item -ItemType File -Force -Path "app/parsers/$_.py"
}
@("__init__", "scoring") | ForEach-Object {
    New-Item -ItemType File -Force -Path "app/matching/$_.py"
}

# Create .env file if not exists
if (-Not (Test-Path ".env")) {
    Set-Content -Path ".env" -Value @"
OPENAI_API_KEY=your_api_key_here
POSTGRES_PASSWORD=postgres
"@
}

Write-Host "✅ Project structure ready!" -ForegroundColor Green