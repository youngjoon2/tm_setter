# TM Setter

데이터베이스 코드 선택과 Jira 이슈 관리를 위한 도구입니다.
GUI와 CLI 두 가지 버전을 제공합니다.

## 특징

### GUI 버전 (PyQt5)
- ✅ 모던한 다크 테마 UI
- ✅ 애니메이션 효과 및 키보드 단축키
- ✅ 비동기 처리로 UI 응답성 유지
- ✅ 크로스 플랫폼 지원 (Windows, macOS, Linux)

### CLI 버전 (신규)
- ✅ 대화형 모드와 개별 명령어 모드
- ✅ 단계별 진행 및 이전 단계로 돌아가기
- ✅ 페이지네이션과 검색 기능
- ✅ 안전한 비밀번호 입력 (getpass)

### 공통 기능
- ✅ 사용자 로그인/인증
- ✅ DB Code 3단계 선택
- ✅ Jira Issue 검색 및 선택
- ✅ 옵션 설정 (Repository, SW 버전)
- ✅ 설정 저장 및 불러오기

## 요구사항

- Python 3.8 이상
- pip 패키지 관리자

## 설치

```bash
# 의존성 설치
pip install -r requirements.txt
```

### GUI 버전 추가 요구사항
- PyQt5 (`pip install PyQt5`)
- GUI 환경 (X11, Wayland 등)

### CLI 버전 선택적 패키지
- rich (향상된 터미널 출력) - `pip install rich`

## 사용법

### CLI 버전

#### 대화형 모드 (추천)
```bash
python3 -m cli.main
```

#### 개별 명령어
```bash
# 로그인
python3 -m cli.main login --id username

# DB 선택
python3 -m cli.main select-db --db1 "Database A" --db2 "Schema X" --db3 "Table Alpha"

# Jira Issue 선택
python3 -m cli.main select-issue --issue PROJ-123

# 옵션 설정
python3 -m cli.main configure --repo my-repo --version v2.1.0

# 도움말
python3 -m cli.main --help
```

### GUI 버전

```bash
# PyQt5 GUI 실행
python3 src/main_pyqt.py
```

## 테스트 계정

- ID: `admin`
- Password: `admin`

## 프로젝트 구조

```
tm_setter/
├── cli/                # CLI 버전
│   ├── main.py        # CLI 진입점
│   └── commands/      # CLI 명령어 모듈
├── src/               # GUI 버전
│   ├── main_pyqt.py   # GUI 진입점
│   ├── pyqt_views/    # PyQt5 화면
│   ├── controllers/   # 비즈니스 로직
│   ├── models/        # 데이터 모델
│   ├── utils/         # 유틸리티
│   └── widgets/       # 커스텀 위젯
├── tests/             # 테스트 코드
├── docs/              # 문서
├── atlassian_api/     # Jira API 모듈
└── prototype/         # HTML 프로토타입
```

## 화면 흐름

1. **로그인** → 사용자 인증
2. **DB Code 선택** → 3개 항목 선택
3. **Jira Issue 선택** → Issue 검색 및 선택
4. **옵션 설정** → Repository 및 SW 버전 설정 (선택사항)
5. **완료** → 작업 처리 및 초기화

## 설정 파일

설정은 `~/.tm_setter/config.json`에 저장됩니다.

## 테스트

```bash
# CLI 테스트 실행
python3 -m unittest tests/cli/test_cli_commands.py

# GUI 테스트 실행  
python3 -m unittest tests/test_gui_integration.py

# 전체 테스트 실행
python3 -m unittest discover tests
```

## 개발

### 기여 방법
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 코드 스타일
- PEP 8 준수
- Type hints 사용
- Docstring 작성 필수

## 문서

자세한 내용은 [docs/](docs/) 디렉토리를 참조하세요:
- [요구사항](docs/요구사항.md)
- [구현 상황](docs/구현 상황.md)
- [TODO](docs/TODO.md)

## 라이선스

Private