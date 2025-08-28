"""PyQt5용 다크 테마 정의"""


class PyQtDarkTheme:
    """PyQt5 다크 테마 설정"""
    
    # 색상 정의
    BG_PRIMARY = "#1a1a1a"
    BG_SECONDARY = "#242424"
    BG_CARD = "#2a2a2a"
    BG_INPUT = "#333333"
    BG_HOVER = "#3a3a3a"
    
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b3b3b3"
    TEXT_MUTED = "#808080"
    
    BORDER_COLOR = "#404040"
    BORDER_FOCUS = "#5294e2"
    
    ACCENT_PRIMARY = "#4a9eff"
    ACCENT_HOVER = "#66b0ff"
    ACCENT_ACTIVE = "#3388ee"
    
    SUCCESS = "#52c41a"
    WARNING = "#faad14"
    ERROR = "#ff4d4f"
    INFO = "#1890ff"
    
    # 폰트 설정
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_XS = 10
    FONT_SIZE_SM = 11
    FONT_SIZE_MD = 12
    FONT_SIZE_LG = 14
    FONT_SIZE_XL = 16
    FONT_SIZE_2XL = 20
    
    @classmethod
    def get_stylesheet(cls) -> str:
        """QSS 스타일시트 생성"""
        return f"""
        /* 전체 배경 */
        QMainWindow {{
            background-color: {cls.BG_PRIMARY};
        }}
        
        QWidget {{
            background-color: {cls.BG_PRIMARY};
            color: {cls.TEXT_PRIMARY};
            font-family: "{cls.FONT_FAMILY}";
            font-size: {cls.FONT_SIZE_MD}px;
        }}
        
        /* 프레임 */
        QFrame {{
            background-color: {cls.BG_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: 8px;
        }}
        
        QFrame#header {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.ACCENT_PRIMARY}, stop:1 {cls.ACCENT_ACTIVE});
            border: none;
            border-radius: 0;
        }}
        
        QFrame#stepFrame {{
            background-color: {cls.BG_SECONDARY};
            border: none;
            border-radius: 0;
        }}
        
        /* 라벨 */
        QLabel {{
            background-color: transparent;
            color: {cls.TEXT_PRIMARY};
            padding: 2px;
        }}
        
        QLabel#title {{
            font-size: {cls.FONT_SIZE_2XL}px;
            font-weight: bold;
            color: {cls.TEXT_PRIMARY};
        }}
        
        QLabel#subtitle {{
            font-size: {cls.FONT_SIZE_SM}px;
            color: {cls.TEXT_SECONDARY};
        }}
        
        QLabel#errorLabel {{
            color: {cls.ERROR};
            font-size: {cls.FONT_SIZE_SM}px;
        }}
        
        /* 입력 필드 */
        QLineEdit {{
            background-color: {cls.BG_INPUT};
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            padding: 10px;
            color: {cls.TEXT_PRIMARY};
            font-size: {cls.FONT_SIZE_MD}px;
        }}
        
        QLineEdit:focus {{
            border-color: {cls.BORDER_FOCUS};
            outline: none;
        }}
        
        QLineEdit:disabled {{
            background-color: {cls.BG_SECONDARY};
            color: {cls.TEXT_MUTED};
        }}
        
        /* 텍스트 영역 */
        QTextEdit, QPlainTextEdit {{
            background-color: {cls.BG_INPUT};
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            padding: 8px;
            color: {cls.TEXT_PRIMARY};
            font-size: {cls.FONT_SIZE_MD}px;
        }}
        
        QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {cls.BORDER_FOCUS};
        }}
        
        /* 버튼 */
        QPushButton {{
            background-color: {cls.ACCENT_PRIMARY};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            font-size: {cls.FONT_SIZE_MD}px;
            font-weight: 600;
            min-height: 36px;
        }}
        
        QPushButton:hover {{
            background-color: {cls.ACCENT_HOVER};
        }}
        
        QPushButton:pressed {{
            background-color: {cls.ACCENT_ACTIVE};
        }}
        
        QPushButton:disabled {{
            background-color: {cls.BG_HOVER};
            color: {cls.TEXT_MUTED};
        }}
        
        QPushButton#secondaryButton {{
            background-color: {cls.BG_SECONDARY};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_COLOR};
        }}
        
        QPushButton#secondaryButton:hover {{
            background-color: {cls.BG_HOVER};
        }}
        
        /* 체크박스 */
        QCheckBox {{
            color: {cls.TEXT_SECONDARY};
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: 3px;
            background-color: {cls.BG_INPUT};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {cls.ACCENT_PRIMARY};
            border-color: {cls.ACCENT_PRIMARY};
        }}
        
        QCheckBox::indicator:checked {{
            image: url(checkmark.png);  /* 체크마크 이미지 필요 시 */
        }}
        
        /* 콤보박스 */
        QComboBox {{
            background-color: {cls.BG_INPUT};
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            padding: 8px;
            color: {cls.TEXT_PRIMARY};
            min-width: 150px;
        }}
        
        QComboBox:hover {{
            border-color: {cls.ACCENT_PRIMARY};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            width: 12px;
            height: 12px;
            image: none;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 6px solid {cls.TEXT_SECONDARY};
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {cls.BG_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            selection-background-color: {cls.ACCENT_PRIMARY};
            color: {cls.TEXT_PRIMARY};
        }}
        
        /* 테이블 */
        QTableWidget {{
            background-color: {cls.BG_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            gridline-color: {cls.BORDER_COLOR};
        }}
        
        QTableWidget::item {{
            padding: 8px;
            color: {cls.TEXT_PRIMARY};
        }}
        
        QTableWidget::item:selected {{
            background-color: {cls.ACCENT_PRIMARY};
        }}
        
        QHeaderView::section {{
            background-color: {cls.BG_SECONDARY};
            color: {cls.TEXT_PRIMARY};
            padding: 8px;
            border: none;
            border-bottom: 2px solid {cls.BORDER_COLOR};
            font-weight: bold;
        }}
        
        /* 스크롤바 */
        QScrollBar:vertical {{
            background-color: {cls.BG_SECONDARY};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.BORDER_COLOR};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.TEXT_MUTED};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        
        /* 탭 위젯 */
        QTabWidget::pane {{
            background-color: {cls.BG_CARD};
            border: 1px solid {cls.BORDER_COLOR};
        }}
        
        QTabBar::tab {{
            background-color: {cls.BG_SECONDARY};
            color: {cls.TEXT_SECONDARY};
            padding: 10px 20px;
            border: none;
        }}
        
        QTabBar::tab:selected {{
            background-color: {cls.BG_CARD};
            color: {cls.TEXT_PRIMARY};
            border-bottom: 2px solid {cls.ACCENT_PRIMARY};
        }}
        
        QTabBar::tab:hover {{
            background-color: {cls.BG_HOVER};
        }}
        
        /* 진행 표시줄 */
        QProgressBar {{
            background-color: {cls.BG_SECONDARY};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            text-align: center;
            color: {cls.TEXT_PRIMARY};
        }}
        
        QProgressBar::chunk {{
            background-color: {cls.ACCENT_PRIMARY};
            border-radius: 3px;
        }}
        
        /* 메시지 박스 */
        QMessageBox {{
            background-color: {cls.BG_CARD};
            color: {cls.TEXT_PRIMARY};
        }}
        
        QMessageBox QPushButton {{
            min-width: 80px;
        }}
        
        /* 툴팁 */
        QToolTip {{
            background-color: {cls.BG_SECONDARY};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_COLOR};
            padding: 4px;
        }}
        
        /* 스텝 인디케이터 */
        QLabel#stepCircle {{
            background-color: {cls.BG_CARD};
            color: {cls.TEXT_MUTED};
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: 20px;
            min-width: 40px;
            max-width: 40px;
            min-height: 40px;
            max-height: 40px;
            font-weight: bold;
            font-size: {cls.FONT_SIZE_MD}px;
        }}
        
        QLabel#stepCircleActive {{
            background-color: {cls.ACCENT_PRIMARY};
            color: white;
            border-color: {cls.ACCENT_PRIMARY};
        }}
        
        QLabel#stepCircleCompleted {{
            background-color: {cls.SUCCESS};
            color: white;
            border-color: {cls.SUCCESS};
        }}
        
        QLabel#stepText {{
            color: {cls.TEXT_MUTED};
            font-size: {cls.FONT_SIZE_SM}px;
        }}
        
        QLabel#stepTextActive {{
            color: {cls.ACCENT_PRIMARY};
            font-weight: bold;
        }}
        
        QLabel#stepTextCompleted {{
            color: {cls.SUCCESS};
        }}
        
        /* 구분선 */
        QFrame#line {{
            background-color: {cls.BORDER_COLOR};
            max-height: 1px;
        }}
        """