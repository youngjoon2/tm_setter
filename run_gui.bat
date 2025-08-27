@echo off
REM TM Setter GUI 실행 스크립트 (Windows)

echo TM Setter GUI를 시작합니다...
echo.
echo ===================================
echo 주의: Python 3.8 이상이 설치되어 있어야 합니다.
echo Windows에서는 tkinter가 기본으로 포함되어 있습니다.
echo ===================================
echo.

REM Python 버전 확인
python --version 2>NUL
if %errorlevel% neq 0 (
    echo Python이 설치되지 않았습니다!
    echo https://www.python.org 에서 Python을 다운로드하세요.
    pause
    exit /b 1
)

REM 필요 패키지 설치
echo 필요 패키지를 설치합니다...
pip install -r requirements.txt --quiet

REM GUI 실행
echo.
echo GUI를 실행합니다...
echo 로그인 테스트 계정: ID=admin, PW=admin
echo.
cd /d "%~dp0"
python src\main.py

if %errorlevel% neq 0 (
    echo.
    echo 오류가 발생했습니다!
    pause
)