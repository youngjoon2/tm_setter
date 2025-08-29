"""PyQt5 애니메이션 유틸리티"""

from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty, QPoint, QRect
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect


class AnimationHelper:
    """애니메이션 헬퍼 클래스"""
    
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 300):
        """페이드 인 애니메이션"""
        if not widget:
            return None
            
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # 애니메이션 완료 시 effect 제거 (완전히 불투명하게)
        animation.finished.connect(lambda: widget.setGraphicsEffect(None))
        animation.start()
        
        return animation
    
    @staticmethod
    def fade_out(widget: QWidget, duration: int = 300):
        """페이드 아웃 애니메이션"""
        if not widget:
            return None
            
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()
        
        return animation
    
    @staticmethod
    def slide_in(widget: QWidget, direction: str = "left", duration: int = 300):
        """슬라이드 인 애니메이션"""
        geometry = widget.geometry()
        
        if direction == "left":
            start_pos = QPoint(-geometry.width(), geometry.y())
        elif direction == "right":
            start_pos = QPoint(widget.parent().width(), geometry.y())
        elif direction == "top":
            start_pos = QPoint(geometry.x(), -geometry.height())
        else:  # bottom
            start_pos = QPoint(geometry.x(), widget.parent().height())
        
        end_pos = QPoint(geometry.x(), geometry.y())
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
        
        return animation
    
    @staticmethod
    def bounce(widget: QWidget, duration: int = 300):
        """바운스 애니메이션"""
        geometry = widget.geometry()
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(geometry)
        
        # 살짝 작아졌다가 다시 원래 크기로
        small = QRect(
            geometry.x() + 10,
            geometry.y() + 10,
            geometry.width() - 20,
            geometry.height() - 20
        )
        
        animation.setKeyValueAt(0.5, small)
        animation.setEndValue(geometry)
        animation.setEasingCurve(QEasingCurve.InOutElastic)
        animation.start()
        
        return animation
    
    @staticmethod
    def shake(widget: QWidget, duration: int = 500, amplitude: int = 10):
        """흔들기 애니메이션 (에러 표시용)"""
        pos = widget.pos()
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(pos)
        
        # 좌우로 흔들기
        animation.setKeyValueAt(0.1, QPoint(pos.x() + amplitude, pos.y()))
        animation.setKeyValueAt(0.2, QPoint(pos.x() - amplitude, pos.y()))
        animation.setKeyValueAt(0.3, QPoint(pos.x() + amplitude, pos.y()))
        animation.setKeyValueAt(0.4, QPoint(pos.x() - amplitude, pos.y()))
        animation.setKeyValueAt(0.5, QPoint(pos.x() + amplitude, pos.y()))
        animation.setKeyValueAt(0.6, QPoint(pos.x() - amplitude, pos.y()))
        animation.setKeyValueAt(0.7, QPoint(pos.x() + amplitude, pos.y()))
        animation.setKeyValueAt(0.8, QPoint(pos.x() - amplitude, pos.y()))
        animation.setKeyValueAt(0.9, QPoint(pos.x() + amplitude, pos.y()))
        
        animation.setEndValue(pos)
        animation.setEasingCurve(QEasingCurve.Linear)
        animation.start()
        
        return animation