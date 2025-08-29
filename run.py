#!/usr/bin/env python3
"""간단한 실행 스크립트"""

import sys
import os

# src 디렉토리를 path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# PyQt5와 메인 모듈 임포트
from PyQt5.QtWidgets import QApplication
from main_pyqt import TMSetterMainWindow

if __name__ == "__main__":
    # QApplication 생성
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 메인 윈도우 생성 및 표시
    window = TMSetterMainWindow()
    window.show()
    
    # 이벤트 루프 실행
    sys.exit(app.exec_())