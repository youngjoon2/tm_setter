# TM Setter TODO List

## ✅ 완료된 작업

### 1단계: 프로토타입 개발
- [x] HTML/CSS/JS 프로토타입 완성
  - [x] 로그인 화면 디자인
  - [x] DB Code 선택 화면 디자인
  - [x] Jira Issue 선택 화면 디자인
  - [x] 옵션 설정 화면 디자인
  - [x] 화면 전환 애니메이션

### 2단계: 기본 구조 구현
- [x] 프로젝트 초기 설정
  - [x] 필요 패키지 설치 (requirements.txt)
  - [x] 설정 파일 구조 정의
- [x] 메인 애플리케이션 프레임워크
  - [x] GUI 프레임워크 선택 및 설정 (Tkinter)
  - [x] 화면 전환 매니저 구현
  - [x] 전역 상태 관리 구현

### 3단계: 핵심 기능 구현
- [x] 로그인 기능
  - [x] 로그인 UI 구현
  - [x] 인증 로직 구현
  - [x] 세션 관리
  - [x] 에러 핸들링
- [x] DB Code 선택 기능
  - [x] 선택 UI 구현
  - [x] 데이터 로드 로직
  - [x] 선택 검증 로직
- [x] Jira Issue 관리
  - [x] Issue 리스트 UI
  - [x] 검색 및 필터 기능
- [x] 옵션 설정
  - [x] 설정 UI 구현
  - [x] 설정 저장/로드

### 4단계: 비동기 처리
- [x] 백그라운드 작업 시스템
  - [x] 스레드 풀 구현
  - [x] 작업 큐 구현
  - [x] 콜백 시스템
- [x] UI 응답성 개선
  - [x] 로딩 인디케이터
  - [x] 비동기 API 호출

### 5단계: 크로스 플랫폼 지원
- [x] Windows 지원
  - [x] run_gui.bat 스크립트
  - [x] run_gui.ps1 스크립트
- [x] Linux/macOS 지원
  - [x] run_gui.sh 스크립트
- [x] 플랫폼별 설치 가이드 문서화

## 📋 진행 예정 작업

### 6단계: 실제 API 연동
- [x] Jira API 연동
  - [x] 기본 인증 구현 (API Token 방식)
  - [x] 실제 Issue 조회
  - [x] Issue 생성/수정
  - [x] Atlassian API 모듈 통합
  - [x] 로그인 화면에 Jira URL 입력 필드 추가
  - [x] JiraController와 실제 API 연결
  - [x] 통합 테스트 작성 및 검증
- [ ] 데이터베이스 연동
  - [ ] DB 연결 설정
  - [ ] 실제 DB Code 조회

### 7단계: 테스트
- [ ] 단위 테스트
  - [ ] 인증 모듈 테스트
  - [ ] DB Code 모듈 테스트
  - [ ] Jira 모듈 테스트
- [ ] 플랫폼별 테스트
  - [ ] Windows 10/11 테스트
  - [ ] macOS 테스트
  - [ ] Ubuntu/Debian 테스트

### 8단계: 최적화 및 개선
- [ ] 성능 최적화
  - [ ] 렌더링 최적화
  - [ ] 메모리 사용 최적화
- [ ] UX 개선
  - [ ] 키보드 단축키
  - [ ] 툴팁 추가
  - [ ] 다크 모드
- [ ] 보안 강화
  - [ ] 입력 검증 강화
  - [ ] API 키 암호화

### 9단계: 배포 준비
- [ ] 실행 파일 생성
  - [ ] Windows용 exe (PyInstaller)
  - [ ] macOS용 app
  - [ ] Linux용 AppImage
- [ ] 설치 프로그램
  - [ ] Windows Installer (MSI)
  - [ ] macOS DMG
  - [ ] Linux DEB/RPM
- [ ] 자동 업데이트 기능

## 🐛 알려진 이슈
- Linux에서 tkinter 별도 설치 필요 (`python3-tk`)
- SSH 환경에서 Display 설정 필요

## 💡 개선 아이디어
- 다크 모드 지원
- 다국어 지원 (한국어/영어)
- 자동 로그인 옵션
- 최근 선택 항목 저장
- 즐겨찾기 기능
- 데이터 내보내기 (CSV, Excel)
- 웹 버전 개발 (Flask/FastAPI)

## 📝 메모
- ✅ GUI 프레임워크: Tkinter 선택 완료
- ✅ 크로스 플랫폼 지원 완료
- ✅ 비동기 처리 구현 완료
- Jira API 접근 권한 확인 필요
- 실제 데이터베이스 연결 정보 필요