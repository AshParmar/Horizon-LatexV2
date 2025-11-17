# AI Recruitment Platform - Backend Setup Script

Write-Host "🚀 Setting up AI Recruitment Platform Backend..." -ForegroundColor Green

# Check Python installation
Write-Host "`n📦 Checking Python installation..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found! Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`n🔧 Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "✅ Virtual environment created!" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n🔌 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "`n📥 Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if doesn't exist
Write-Host "`n⚙️ Setting up environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host ".env file already exists." -ForegroundColor Gray
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file from .env.example" -ForegroundColor Green
    Write-Host "⚠️ Please edit .env and add your API keys!" -ForegroundColor Yellow
}

# Create data directories
Write-Host "`n📁 Setting up data directories..." -ForegroundColor Yellow
$directories = @("data/raw", "data/processed", "data/logs", "data/vectorstore")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "✅ Data directories created!" -ForegroundColor Green

Write-Host "`n✨ Setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your API keys" -ForegroundColor White
Write-Host "2. Get Composio Auth Configs from https://platform.composio.dev" -ForegroundColor White
Write-Host "3. Run: python main.py" -ForegroundColor White
Write-Host "`n📚 API Documentation will be at: http://localhost:8000/docs" -ForegroundColor Cyan
