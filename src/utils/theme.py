"""다크 테마 스타일 정의"""

class DarkTheme:
    """다크 테마 색상 및 스타일"""
    
    # 메인 색상
    BG_PRIMARY: str = "#1a1a2e"      # 메인 배경 (진한 네이비)
    BG_SECONDARY: str = "#16213e"    # 보조 배경
    BG_TERTIARY: str = "#0f3460"     # 세번째 배경
    
    # 카드 및 컨테이너
    BG_CARD: str = "#1e2139"         # 카드 배경
    BG_HOVER: str = "#252844"        # 호버 상태
    BG_INPUT: str = "#2a2d4a"        # 입력 필드 배경
    
    # 액센트 색상
    ACCENT_PRIMARY: str = "#7c3aed"   # 메인 액센트 (보라색)
    ACCENT_HOVER: str = "#6d28d9"     # 호버 액센트
    ACCENT_ACTIVE: str = "#5b21b6"    # 활성 액센트
    
    # 성공, 경고, 에러
    SUCCESS: str = "#10b981"          # 성공 (민트 그린)
    WARNING: str = "#f59e0b"          # 경고 (오렌지)
    ERROR: str = "#ef4444"            # 에러 (레드)
    INFO: str = "#3b82f6"            # 정보 (블루)
    
    # 텍스트 색상
    TEXT_PRIMARY: str = "#f8fafc"     # 주 텍스트 (밝은 흰색)
    TEXT_SECONDARY: str = "#cbd5e1"   # 보조 텍스트 (회색빛 흰색)
    TEXT_MUTED: str = "#94a3b8"       # 약한 텍스트
    TEXT_DISABLED: str = "#64748b"    # 비활성 텍스트
    
    # 보더 색상
    BORDER_COLOR: str = "#334155"     # 일반 보더
    BORDER_FOCUS: str = "#7c3aed"     # 포커스 보더
    
    # 그림자 효과
    SHADOW_SM: str = "0 1px 2px 0 rgba(0, 0, 0, 0.5)"
    SHADOW_MD: str = "0 4px 6px -1px rgba(0, 0, 0, 0.5)"
    SHADOW_LG: str = "0 10px 15px -3px rgba(0, 0, 0, 0.5)"
    
    # 폰트
    FONT_FAMILY: str = "Segoe UI"
    FONT_SIZE_XS: int = 9
    FONT_SIZE_SM: int = 11
    FONT_SIZE_MD: int = 13
    FONT_SIZE_LG: int = 16
    FONT_SIZE_XL: int = 20
    FONT_SIZE_2XL: int = 24
    FONT_SIZE_3XL: int = 30
    
    # 간격
    SPACING_XS: int = 4
    SPACING_SM: int = 8
    SPACING_MD: int = 12
    SPACING_LG: int = 16
    SPACING_XL: int = 20
    SPACING_2XL: int = 24
    SPACING_3XL: int = 32
    
    # 보더 반경
    RADIUS_SM: int = 4
    RADIUS_MD: int = 8
    RADIUS_LG: int = 12
    RADIUS_XL: int = 16
    RADIUS_FULL: int = 9999
    
    @classmethod
    def get_button_style(cls, variant: str = "primary") -> dict:
        """버튼 스타일 반환"""
        base_style = {
            'font': (cls.FONT_FAMILY, cls.FONT_SIZE_MD, 'bold'),
            'relief': 'flat',
            'cursor': 'hand2',
            'borderwidth': 0,
            'padx': cls.SPACING_LG,
            'pady': cls.SPACING_SM,
        }
        
        if variant == "primary":
            base_style.update({
                'bg': cls.ACCENT_PRIMARY,
                'fg': cls.TEXT_PRIMARY,
                'activebackground': cls.ACCENT_HOVER,
                'activeforeground': cls.TEXT_PRIMARY,
            })
        elif variant == "secondary":
            base_style.update({
                'bg': cls.BG_CARD,
                'fg': cls.TEXT_PRIMARY,
                'activebackground': cls.BG_HOVER,
                'activeforeground': cls.TEXT_PRIMARY,
            })
        elif variant == "danger":
            base_style.update({
                'bg': cls.ERROR,
                'fg': cls.TEXT_PRIMARY,
                'activebackground': '#dc2626',
                'activeforeground': cls.TEXT_PRIMARY,
            })
        elif variant == "success":
            base_style.update({
                'bg': cls.SUCCESS,
                'fg': cls.TEXT_PRIMARY,
                'activebackground': '#059669',
                'activeforeground': cls.TEXT_PRIMARY,
            })
            
        return base_style
    
    @classmethod
    def get_entry_style(cls) -> dict:
        """입력 필드 스타일 반환"""
        return {
            'bg': cls.BG_INPUT,
            'fg': cls.TEXT_PRIMARY,
            'insertbackground': cls.TEXT_PRIMARY,
            'selectbackground': cls.ACCENT_PRIMARY,
            'selectforeground': cls.TEXT_PRIMARY,
            'font': (cls.FONT_FAMILY, cls.FONT_SIZE_MD),
            'relief': 'flat',
            'borderwidth': 2,
            'highlightthickness': 1,
            'highlightbackground': cls.BORDER_COLOR,
            'highlightcolor': cls.BORDER_FOCUS,
        }
    
    @classmethod
    def get_label_style(cls, variant: str = "primary") -> dict:
        """레이블 스타일 반환"""
        base_style = {
            'font': (cls.FONT_FAMILY, cls.FONT_SIZE_MD),
            'bg': cls.BG_PRIMARY,
        }
        
        if variant == "primary":
            base_style['fg'] = cls.TEXT_PRIMARY
        elif variant == "secondary":
            base_style['fg'] = cls.TEXT_SECONDARY
        elif variant == "muted":
            base_style['fg'] = cls.TEXT_MUTED
        elif variant == "error":
            base_style['fg'] = cls.ERROR
        elif variant == "success":
            base_style['fg'] = cls.SUCCESS
            
        return base_style
    
    @classmethod
    def get_frame_style(cls, variant: str = "primary") -> dict:
        """프레임 스타일 반환"""
        if variant == "primary":
            return {'bg': cls.BG_PRIMARY}
        elif variant == "secondary":
            return {'bg': cls.BG_SECONDARY}
        elif variant == "card":
            return {
                'bg': cls.BG_CARD,
                'relief': 'flat',
                'borderwidth': 1,
                'highlightbackground': cls.BORDER_COLOR,
                'highlightthickness': 1,
            }
        else:
            return {'bg': cls.BG_PRIMARY}
    
    @classmethod
    def get_ttk_style_config(cls) -> dict:
        """ttk 스타일 설정 반환"""
        return {
            'TButton': {
                'configure': {
                    'background': cls.ACCENT_PRIMARY,
                    'foreground': cls.TEXT_PRIMARY,
                    'borderwidth': 0,
                    'focuscolor': 'none',
                    'font': (cls.FONT_FAMILY, cls.FONT_SIZE_MD, 'bold'),
                },
                'map': {
                    'background': [('active', cls.ACCENT_HOVER)],
                    'foreground': [('active', cls.TEXT_PRIMARY)],
                }
            },
            'TLabel': {
                'configure': {
                    'background': cls.BG_PRIMARY,
                    'foreground': cls.TEXT_PRIMARY,
                    'font': (cls.FONT_FAMILY, cls.FONT_SIZE_MD),
                }
            },
            'TEntry': {
                'configure': {
                    'fieldbackground': cls.BG_INPUT,
                    'background': cls.BG_INPUT,
                    'foreground': cls.TEXT_PRIMARY,
                    'insertcolor': cls.TEXT_PRIMARY,
                    'font': (cls.FONT_FAMILY, cls.FONT_SIZE_MD),
                }
            },
            'TFrame': {
                'configure': {
                    'background': cls.BG_PRIMARY,
                    'borderwidth': 0,
                }
            },
            'TLabelframe': {
                'configure': {
                    'background': cls.BG_CARD,
                    'foreground': cls.TEXT_PRIMARY,
                    'borderwidth': 1,
                    'relief': 'flat',
                }
            },
            'TNotebook': {
                'configure': {
                    'background': cls.BG_PRIMARY,
                    'borderwidth': 0,
                    'tabmargins': [0, 0, 0, 0],
                }
            },
            'TNotebook.Tab': {
                'configure': {
                    'background': cls.BG_CARD,
                    'foreground': cls.TEXT_SECONDARY,
                    'padding': [cls.SPACING_LG, cls.SPACING_SM],
                    'font': (cls.FONT_FAMILY, cls.FONT_SIZE_MD),
                },
                'map': {
                    'background': [('selected', cls.BG_HOVER)],
                    'foreground': [('selected', cls.TEXT_PRIMARY)],
                }
            },
            'TProgressbar': {
                'configure': {
                    'background': cls.ACCENT_PRIMARY,
                    'troughcolor': cls.BG_INPUT,
                    'borderwidth': 0,
                    'lightcolor': cls.ACCENT_PRIMARY,
                    'darkcolor': cls.ACCENT_PRIMARY,
                }
            },
            'TScrollbar': {
                'configure': {
                    'background': cls.BG_SECONDARY,
                    'troughcolor': cls.BG_PRIMARY,
                    'borderwidth': 0,
                    'arrowcolor': cls.TEXT_MUTED,
                    'width': 12,
                },
                'map': {
                    'background': [('active', cls.BG_HOVER)],
                }
            },
            'Treeview': {
                'configure': {
                    'background': cls.BG_CARD,
                    'foreground': cls.TEXT_PRIMARY,
                    'fieldbackground': cls.BG_CARD,
                    'font': (cls.FONT_FAMILY, cls.FONT_SIZE_MD),
                },
                'map': {
                    'background': [('selected', cls.ACCENT_PRIMARY)],
                    'foreground': [('selected', cls.TEXT_PRIMARY)],
                }
            },
            'Treeview.Heading': {
                'configure': {
                    'background': cls.BG_SECONDARY,
                    'foreground': cls.TEXT_PRIMARY,
                    'font': (cls.FONT_FAMILY, cls.FONT_SIZE_MD, 'bold'),
                }
            },
        }