#!/bin/bash

# TM Setter GUI 실행 스크립트

echo "TM Setter GUI를 시작합니다..."
echo ""
echo "==================================="
echo "주의: tkinter가 설치되어 있어야 합니다."
echo "Ubuntu/Debian: sudo apt-get install python3-tk"
echo "CentOS/RHEL: sudo yum install python3-tkinter"
echo "macOS: tkinter는 기본으로 포함되어 있습니다"
echo "==================================="
echo ""

# Python 버전 확인
python3 --version

# 필요 패키지 설치 확인
echo "필요 패키지를 설치합니다..."
pip3 install -r requirements.txt --quiet

# GUI 실행
echo "GUI를 실행합니다..."
cd "$(dirname "$0")"
python3 src/main.py