# TM Setter

사용자 인증을 통해 데이터베이스 코드를 선택하고 Jira 이슈를 관리하는 GUI 애플리케이션

## 기능

- ✅ 사용자 로그인/인증
- ✅ DB Code 3단계 선택
- ✅ Jira Issue 검색 및 선택
- ✅ 옵션 설정 (Repository, SW 버전)
- ✅ 비동기 처리로 UI 응답성 유지

## 요구사항

- Python 3.8 이상
- tkinter (GUI 프레임워크)

## 설치

### 1. tkinter 설치

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**CentOS/RHEL:**
```bash
sudo yum install python3-tkinter
```

**macOS:**
- tkinter는 기본으로 포함되어 있습니다

**Windows:**
- Python 설치 시 tkinter가 포함됩니다

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

## 실행

### 방법 1: 실행 스크립트 사용
```bash
./run_gui.sh
```

### 방법 2: Python 직접 실행
```bash
cd tm_setter
python3 src/main.py
```

## 테스트 계정

- ID: `admin`
- Password: `admin`

## 프로젝트 구조

```
tm_setter/
├── src/
│   ├── main.py              # 메인 애플리케이션
│   ├── views/               # GUI 화면들
│   │   ├── login_view.py    # 로그인 화면
│   │   ├── db_code_view.py  # DB Code 선택 화면
│   │   ├── jira_issue_view.py # Jira Issue 선택 화면
│   │   └── options_view.py  # 옵션 설정 화면
│   └── utils/
│       ├── async_handler.py # 비동기 처리
│       └── config.py        # 설정 관리
├── docs/                    # 문서
├── prototype/              # HTML 프로토타입
└── tests/                  # 테스트 코드
```

## 화면 흐름

1. **로그인** → 사용자 인증
2. **DB Code 선택** → 3개 항목 선택
3. **Jira Issue 선택** → Issue 검색 및 선택
4. **옵션 설정** → Repository 및 SW 버전 설정 (선택사항)
5. **완료** → 작업 처리 및 초기화

## 설정 파일

설정은 `~/.tm_setter/config.json`에 저장됩니다.

## 문제 해결

### tkinter 오류
```
ModuleNotFoundError: No module named 'tkinter'
```
→ 위의 tkinter 설치 방법 참조

### Display 오류 (SSH 접속 시)
```
_tkinter.TclError: no display name and no $DISPLAY environment variable
```
→ X11 Forwarding 활성화 또는 VNC 사용

## 개발

### 테스트 실행
```bash
pytest tests/
```

### 새로운 화면 추가
1. `src/views/` 디렉토리에 새 뷰 파일 생성
2. `src/main.py`의 `_init_views()` 메서드에 추가
3. 스텝 인디케이터 업데이트

## 라이선스

Private