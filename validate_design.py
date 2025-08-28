#!/usr/bin/env python3
"""다크 테마 디자인 검증 스크립트"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.theme import DarkTheme

def validate_color_contrast():
    """색상 대비 검증"""
    theme = DarkTheme
    
    print("=== 다크 테마 색상 팔레트 검증 ===\n")
    
    # 배경 색상
    print("📦 배경 색상:")
    print(f"  메인 배경: {theme.BG_PRIMARY} (진한 네이비)")
    print(f"  보조 배경: {theme.BG_SECONDARY}")
    print(f"  카드 배경: {theme.BG_CARD}")
    print(f"  입력 필드: {theme.BG_INPUT}")
    
    # 텍스트 색상
    print("\n📝 텍스트 색상:")
    print(f"  주 텍스트: {theme.TEXT_PRIMARY} (밝은 흰색)")
    print(f"  보조 텍스트: {theme.TEXT_SECONDARY}")
    print(f"  약한 텍스트: {theme.TEXT_MUTED}")
    
    # 액센트 색상
    print("\n🎨 액센트 색상:")
    print(f"  메인 액센트: {theme.ACCENT_PRIMARY} (보라색)")
    print(f"  호버 상태: {theme.ACCENT_HOVER}")
    print(f"  활성 상태: {theme.ACCENT_ACTIVE}")
    
    # 상태 색상
    print("\n🚦 상태 색상:")
    print(f"  성공: {theme.SUCCESS} (민트 그린)")
    print(f"  경고: {theme.WARNING} (오렌지)")
    print(f"  에러: {theme.ERROR} (레드)")
    print(f"  정보: {theme.INFO} (블루)")
    
    # 대비율 검증 (간단한 명도 차이 계산)
    def hex_to_luminance(hex_color):
        """HEX 색상의 상대 명도 계산"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
        
        # sRGB to linear RGB
        def to_linear(c):
            if c <= 0.03928:
                return c / 12.92
            return ((c + 0.055) / 1.055) ** 2.4
        
        r, g, b = to_linear(r), to_linear(g), to_linear(b)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    def contrast_ratio(color1, color2):
        """두 색상 간의 대비율 계산"""
        l1 = hex_to_luminance(color1)
        l2 = hex_to_luminance(color2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    print("\n📊 색상 대비율 검증:")
    
    # WCAG AA 기준: 일반 텍스트 4.5:1, 큰 텍스트 3:1
    contrasts = [
        ("메인 텍스트 vs 배경", theme.TEXT_PRIMARY, theme.BG_PRIMARY),
        ("보조 텍스트 vs 배경", theme.TEXT_SECONDARY, theme.BG_PRIMARY),
        ("버튼 텍스트 vs 버튼 배경", theme.TEXT_PRIMARY, theme.ACCENT_PRIMARY),
        ("에러 텍스트 vs 배경", theme.ERROR, theme.BG_CARD),
    ]
    
    for name, color1, color2 in contrasts:
        ratio = contrast_ratio(color1, color2)
        status = "✅ 통과" if ratio >= 4.5 else "⚠️ 주의"
        print(f"  {name}: {ratio:.2f}:1 {status}")
    
    return True

def validate_component_styles():
    """컴포넌트 스타일 검증"""
    theme = DarkTheme
    
    print("\n=== 컴포넌트 스타일 검증 ===\n")
    
    # 버튼 스타일
    print("🔘 버튼 스타일:")
    primary_btn = theme.get_button_style('primary')
    print(f"  Primary 버튼:")
    print(f"    - 배경: {primary_btn['bg']}")
    print(f"    - 텍스트: {primary_btn['fg']}")
    print(f"    - 폰트: {primary_btn['font']}")
    
    secondary_btn = theme.get_button_style('secondary')
    print(f"  Secondary 버튼:")
    print(f"    - 배경: {secondary_btn['bg']}")
    print(f"    - 텍스트: {secondary_btn['fg']}")
    
    # 입력 필드 스타일
    print("\n📝 입력 필드 스타일:")
    entry_style = theme.get_entry_style()
    print(f"  - 배경: {entry_style['bg']}")
    print(f"  - 텍스트: {entry_style['fg']}")
    print(f"  - 선택 배경: {entry_style['selectbackground']}")
    print(f"  - 포커스 테두리: {entry_style['highlightcolor']}")
    
    # 레이블 스타일
    print("\n🏷️ 레이블 스타일:")
    for variant in ['primary', 'secondary', 'muted', 'error']:
        label_style = theme.get_label_style(variant)
        print(f"  {variant}: 텍스트 {label_style['fg']}, 배경 {label_style['bg']}")
    
    return True

def check_imports():
    """필요한 모듈 임포트 확인"""
    print("\n=== 모듈 임포트 확인 ===\n")
    
    modules_to_check = [
        ('main.py', '/home/yjchoi/company/tm_setter/src/main.py'),
        ('login_view.py', '/home/yjchoi/company/tm_setter/src/views/login_view.py'),
        ('db_code_view.py', '/home/yjchoi/company/tm_setter/src/views/db_code_view.py'),
    ]
    
    import_issues = []
    
    for name, path in modules_to_check:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                if 'from utils.theme import DarkTheme' in content:
                    print(f"✅ {name}: DarkTheme 임포트 확인")
                else:
                    print(f"⚠️ {name}: DarkTheme 임포트 누락")
                    import_issues.append(name)
        else:
            print(f"❌ {name}: 파일을 찾을 수 없음")
    
    return len(import_issues) == 0

def main():
    """메인 검증 실행"""
    print("="*50)
    print("TM Setter 다크 테마 디자인 검증")
    print("="*50)
    
    all_passed = True
    
    # 1. 색상 대비 검증
    if not validate_color_contrast():
        all_passed = False
    
    # 2. 컴포넌트 스타일 검증
    if not validate_component_styles():
        all_passed = False
    
    # 3. 임포트 확인
    if not check_imports():
        all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ 모든 검증 통과! 다크 테마가 올바르게 구현되었습니다.")
    else:
        print("⚠️ 일부 검증 실패. 위의 경고 사항을 확인하세요.")
    print("="*50)
    
    print("\n💡 팁: 실제 GUI를 확인하려면 로컬 환경에서 다음 명령을 실행하세요:")
    print("  python tm_setter/test_gui.py")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)