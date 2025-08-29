#!/usr/bin/env python3
"""모든 GUI 테스트 실행 스크립트"""

import sys
import os
import subprocess

def run_test(test_file, description):
    """개별 테스트 파일 실행"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=False,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 테스트 실행 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("🚀 TM Setter GUI 테스트 스위트 실행")
    print("=" * 70)
    
    # 테스트 목록
    tests = [
        ("test_layout_improvements.py", "레이아웃 개선사항 검증"),
        ("tests/test_gui_layout_improvements.py", "GUI 레이아웃 단위 테스트"),
        ("tests/test_gui_integration.py", "GUI 통합 테스트")
    ]
    
    results = []
    
    # 각 테스트 실행
    for test_file, description in tests:
        success = run_test(test_file, description)
        results.append((description, success))
    
    # 최종 결과 출력
    print("\n" + "=" * 70)
    print("📊 테스트 결과 요약")
    print("=" * 70)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {description}")
    
    print("=" * 70)
    print(f"총 테스트: {total_tests}개")
    print(f"성공: {passed_tests}개")
    print(f"실패: {total_tests - passed_tests}개")
    
    if passed_tests == total_tests:
        print("\n🎉 모든 테스트가 성공적으로 통과했습니다!")
        print("\n✨ 주요 개선사항:")
        print("  1. Qt 레이아웃 시스템 적용")
        print("  2. 창 크기 조절 가능")
        print("  3. 반응형 UI 구현")
        print("  4. Size Policy 설정")
        print("  5. Stretch Factor 적용")
        print("  6. 다양한 화면 비율 지원")
    else:
        print(f"\n⚠️ {total_tests - passed_tests}개의 테스트가 실패했습니다.")
    
    print("=" * 70)
    
    return 0 if passed_tests == total_tests else 1

if __name__ == "__main__":
    sys.exit(main())