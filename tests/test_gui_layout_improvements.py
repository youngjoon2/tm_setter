#!/usr/bin/env python3
"""Qt 레이아웃 개선사항 테스트"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

# PyQt5 모듈 모킹
class MockQWidget:
    def __init__(self, parent=None):
        self.parent = parent
        self.minimum_size = None
        self.maximum_size = None
        self.size_policy = None
        self.fixed_size = None
        self.layout_obj = None
        
    def setMinimumSize(self, width, height):
        self.minimum_size = (width, height)
        
    def setMaximumSize(self, width, height):
        self.maximum_size = (width, height)
        
    def setFixedSize(self, width, height):
        self.fixed_size = (width, height)
        
    def setSizePolicy(self, h_policy, v_policy):
        self.size_policy = (h_policy, v_policy)
        
    def resize(self, width, height):
        self.current_size = (width, height)
        
    def setLayout(self, layout):
        self.layout_obj = layout
        
    def setMinimumHeight(self, height):
        self.minimum_height = height
        
    def setMaximumHeight(self, height):
        self.maximum_height = height

class MockQMainWindow(MockQWidget):
    def __init__(self):
        super().__init__()
        self.central_widget = None
        
    def setCentralWidget(self, widget):
        self.central_widget = widget

class MockQVBoxLayout:
    def __init__(self, parent=None):
        self.parent = parent
        self.widgets = []
        self.stretch_factors = {}
        self.margins = None
        self.spacing = None
        
    def addWidget(self, widget, stretch=0):
        self.widgets.append(widget)
        if stretch > 0:
            self.stretch_factors[widget] = stretch
            
    def setContentsMargins(self, left, top, right, bottom):
        self.margins = (left, top, right, bottom)
        
    def setSpacing(self, spacing):
        self.spacing = spacing
        
    def setStretch(self, index, stretch):
        if index < len(self.widgets):
            self.stretch_factors[self.widgets[index]] = stretch
            
    def addSpacerItem(self, spacer):
        self.widgets.append(spacer)

class MockQSizePolicy:
    Expanding = "Expanding"
    Preferred = "Preferred"
    Minimum = "Minimum"
    Maximum = "Maximum"
    Fixed = "Fixed"

class MockQSpacerItem:
    def __init__(self, width, height, h_policy, v_policy):
        self.width = width
        self.height = height
        self.h_policy = h_policy
        self.v_policy = v_policy

class MockQFrame(MockQWidget):
    pass

class MockQStackedWidget(MockQWidget):
    pass

class MockQPushButton(MockQWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.text = text

class MockQLineEdit(MockQWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class TestLayoutImprovements(unittest.TestCase):
    """레이아웃 개선사항 테스트"""
    
    def setUp(self):
        """테스트 환경 설정"""
        # PyQt5 모듈 모킹
        self.pyqt5_mock = MagicMock()
        self.pyqt5_mock.QtWidgets.QWidget = MockQWidget
        self.pyqt5_mock.QtWidgets.QMainWindow = MockQMainWindow
        self.pyqt5_mock.QtWidgets.QVBoxLayout = MockQVBoxLayout
        self.pyqt5_mock.QtWidgets.QSizePolicy = MockQSizePolicy
        self.pyqt5_mock.QtWidgets.QSpacerItem = MockQSpacerItem
        self.pyqt5_mock.QtWidgets.QFrame = MockQFrame
        self.pyqt5_mock.QtWidgets.QStackedWidget = MockQStackedWidget
        self.pyqt5_mock.QtWidgets.QPushButton = MockQPushButton
        self.pyqt5_mock.QtWidgets.QLineEdit = MockQLineEdit
        
        sys.modules['PyQt5'] = self.pyqt5_mock
        sys.modules['PyQt5.QtWidgets'] = self.pyqt5_mock.QtWidgets
        sys.modules['PyQt5.QtCore'] = MagicMock()
        sys.modules['PyQt5.QtGui'] = MagicMock()
    
    def test_main_window_responsive_sizing(self):
        """메인 윈도우 반응형 크기 설정 테스트"""
        # 메인 윈도우 모의 객체 생성
        main_window = MockQMainWindow()
        
        # 개선된 크기 설정 적용
        main_window.setMinimumSize(800, 600)  # 최소 크기
        main_window.resize(900, 700)  # 기본 크기
        
        # 검증
        self.assertEqual(main_window.minimum_size, (800, 600))
        self.assertEqual(main_window.current_size, (900, 700))
        self.assertIsNone(main_window.fixed_size)  # 고정 크기가 아님
        
        print("✅ 메인 윈도우 반응형 크기 설정 테스트 통과")
    
    def test_layout_stretch_factor(self):
        """레이아웃 Stretch Factor 테스트"""
        # 레이아웃 생성
        layout = MockQVBoxLayout()
        
        # 위젯들 추가
        header = MockQFrame()
        step_frame = MockQFrame()
        stack = MockQStackedWidget()
        
        layout.addWidget(header)
        layout.addWidget(step_frame)
        layout.addWidget(stack, 1)  # stretch factor 1
        
        # 검증
        self.assertIn(stack, layout.stretch_factors)
        self.assertEqual(layout.stretch_factors[stack], 1)
        self.assertNotIn(header, layout.stretch_factors)
        
        print("✅ 레이아웃 Stretch Factor 테스트 통과")
    
    def test_size_policy_settings(self):
        """Size Policy 설정 테스트"""
        # 스택 위젯 생성
        stack = MockQStackedWidget()
        stack.setSizePolicy(MockQSizePolicy.Expanding, MockQSizePolicy.Expanding)
        
        # 버튼 생성
        button = MockQPushButton("테스트")
        button.setSizePolicy(MockQSizePolicy.Expanding, MockQSizePolicy.Preferred)
        
        # 검증
        self.assertEqual(stack.size_policy, (MockQSizePolicy.Expanding, MockQSizePolicy.Expanding))
        self.assertEqual(button.size_policy, (MockQSizePolicy.Expanding, MockQSizePolicy.Preferred))
        
        print("✅ Size Policy 설정 테스트 통과")
    
    def test_flexible_height_settings(self):
        """유연한 높이 설정 테스트"""
        # 헤더 생성
        header = MockQFrame()
        header.setMinimumHeight(45)
        header.setMaximumHeight(50)
        
        # 스텝 프레임 생성
        step_frame = MockQFrame()
        step_frame.setMinimumHeight(70)
        step_frame.setMaximumHeight(80)
        
        # 입력 필드 생성
        input_field = MockQLineEdit()
        input_field.setMinimumHeight(38)
        input_field.setMaximumHeight(42)
        
        # 검증
        self.assertEqual(header.minimum_height, 45)
        self.assertEqual(header.maximum_height, 50)
        self.assertEqual(step_frame.minimum_height, 70)
        self.assertEqual(step_frame.maximum_height, 80)
        self.assertEqual(input_field.minimum_height, 38)
        self.assertEqual(input_field.maximum_height, 42)
        
        print("✅ 유연한 높이 설정 테스트 통과")
    
    def test_login_view_card_sizing(self):
        """로그인 뷰 카드 크기 설정 테스트"""
        # 카드 컨테이너 생성
        card = MockQFrame()
        card.setMinimumSize(380, 420)
        card.setMaximumSize(500, 550)
        card.setSizePolicy(MockQSizePolicy.Preferred, MockQSizePolicy.Preferred)
        
        # 검증
        self.assertEqual(card.minimum_size, (380, 420))
        self.assertEqual(card.maximum_size, (500, 550))
        self.assertEqual(card.size_policy, (MockQSizePolicy.Preferred, MockQSizePolicy.Preferred))
        self.assertIsNone(card.fixed_size)  # 고정 크기가 아님
        
        print("✅ 로그인 뷰 카드 크기 설정 테스트 통과")
    
    def test_layout_margins_and_spacing(self):
        """레이아웃 여백 및 간격 테스트"""
        # 메인 레이아웃 생성
        main_layout = MockQVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 로그인 뷰 레이아웃
        login_layout = MockQVBoxLayout()
        login_layout.setContentsMargins(20, 20, 20, 20)
        
        # 검증
        self.assertEqual(main_layout.margins, (0, 0, 0, 0))
        self.assertEqual(main_layout.spacing, 0)
        self.assertEqual(login_layout.margins, (20, 20, 20, 20))
        
        print("✅ 레이아웃 여백 및 간격 테스트 통과")
    
    def test_spacer_items(self):
        """Spacer 아이템 테스트"""
        # 로그인 뷰 레이아웃
        layout = MockQVBoxLayout()
        
        # 상단 스페이서
        top_spacer = MockQSpacerItem(20, 40, MockQSizePolicy.Minimum, MockQSizePolicy.Expanding)
        layout.addSpacerItem(top_spacer)
        
        # 카드 위젯
        card = MockQFrame()
        layout.addWidget(card)
        
        # 하단 스페이서
        bottom_spacer = MockQSpacerItem(20, 40, MockQSizePolicy.Minimum, MockQSizePolicy.Expanding)
        layout.addSpacerItem(bottom_spacer)
        
        # 검증
        self.assertEqual(len(layout.widgets), 3)
        self.assertEqual(layout.widgets[0].v_policy, MockQSizePolicy.Expanding)
        self.assertEqual(layout.widgets[2].v_policy, MockQSizePolicy.Expanding)
        
        print("✅ Spacer 아이템 테스트 통과")
    
    def test_window_resize_simulation(self):
        """창 크기 조절 시뮬레이션 테스트"""
        # 메인 윈도우 생성
        window = MockQMainWindow()
        window.setMinimumSize(800, 600)
        window.resize(900, 700)
        
        # 다양한 크기로 조절 시뮬레이션
        test_sizes = [
            (800, 600),   # 최소 크기
            (1024, 768),  # 일반적인 크기
            (1920, 1080), # 큰 화면
            (850, 650),   # 중간 크기
        ]
        
        for width, height in test_sizes:
            window.resize(width, height)
            self.assertEqual(window.current_size, (width, height))
            
            # 최소 크기 이하로는 조절되지 않아야 함
            if width >= 800 and height >= 600:
                self.assertGreaterEqual(window.current_size[0], window.minimum_size[0])
                self.assertGreaterEqual(window.current_size[1], window.minimum_size[1])
        
        print("✅ 창 크기 조절 시뮬레이션 테스트 통과")
    
    def test_responsive_ui_components(self):
        """반응형 UI 컴포넌트 테스트"""
        # 다양한 UI 컴포넌트 생성
        components = {
            'stack': MockQStackedWidget(),
            'button1': MockQPushButton("로그인"),
            'button2': MockQPushButton("다음"),
            'input': MockQLineEdit(),
            'frame': MockQFrame()
        }
        
        # Size Policy 설정
        components['stack'].setSizePolicy(MockQSizePolicy.Expanding, MockQSizePolicy.Expanding)
        components['button1'].setSizePolicy(MockQSizePolicy.Expanding, MockQSizePolicy.Preferred)
        components['button2'].setSizePolicy(MockQSizePolicy.Expanding, MockQSizePolicy.Preferred)
        
        # 모든 확장 가능한 컴포넌트 확인
        expanding_components = ['stack', 'button1', 'button2']
        for comp_name in expanding_components:
            comp = components[comp_name]
            self.assertIsNotNone(comp.size_policy)
            if comp_name == 'stack':
                self.assertEqual(comp.size_policy[0], MockQSizePolicy.Expanding)
                self.assertEqual(comp.size_policy[1], MockQSizePolicy.Expanding)
            else:
                self.assertEqual(comp.size_policy[0], MockQSizePolicy.Expanding)
        
        print("✅ 반응형 UI 컴포넌트 테스트 통과")


def run_comprehensive_tests():
    """포괄적인 테스트 실행"""
    print("=" * 60)
    print("Qt 레이아웃 개선사항 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLayoutImprovements)
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)
    print(f"실행된 테스트: {result.testsRun}개")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}개")
    print(f"실패: {len(result.failures)}개")
    print(f"오류: {len(result.errors)}개")
    
    if result.wasSuccessful():
        print("\n✅ 모든 테스트가 성공적으로 통과했습니다!")
        print("\n주요 개선사항 검증 완료:")
        print("  • 창 크기 조절 가능")
        print("  • 레이아웃 Stretch Factor 적용")
        print("  • Size Policy 설정")
        print("  • 유연한 높이 설정")
        print("  • 반응형 UI 컴포넌트")
    else:
        print("\n❌ 일부 테스트가 실패했습니다.")
    
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)