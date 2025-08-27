# TM Setter GUI 실행 스크립트 (Windows PowerShell)

Write-Host "TM Setter GUI를 시작합니다..." -ForegroundColor Green
Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "주의: Python 3.8 이상이 설치되어 있어야 합니다."
Write-Host "Windows에서는 tkinter가 기본으로 포함되어 있습니다."
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Python 설치 확인
try {
    $pythonVersion = python --version 2>&1
    Write-Host "설치된 Python: $pythonVersion" -ForegroundColor Yellow
} catch {
    Write-Host "Python이 설치되지 않았습니다!" -ForegroundColor Red
    Write-Host "https://www.python.org 에서 Python을 다운로드하세요."
    Read-Host "Enter를 눌러 종료하세요"
    exit 1
}

# 필요 패키지 설치
Write-Host "필요 패키지를 설치합니다..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# GUI 실행
Write-Host ""
Write-Host "GUI를 실행합니다..." -ForegroundColor Green
Write-Host "로그인 테스트 계정: ID=admin, PW=admin" -ForegroundColor Cyan
Write-Host ""

Set-Location $PSScriptRoot
python src\main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "오류가 발생했습니다!" -ForegroundColor Red
    Read-Host "Enter를 눌러 종료하세요"
}