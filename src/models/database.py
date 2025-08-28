"""데이터베이스 모델 및 연결 관리"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from pathlib import Path

class DatabaseManager:
    """데이터베이스 연결 및 쿼리 관리"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # 기본 데이터베이스 경로 설정
            home_dir = Path.home()
            app_dir = home_dir / '.tm_setter'
            app_dir.mkdir(exist_ok=True)
            db_path = str(app_dir / 'tm_setter.db')
            
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
        # 데이터베이스 초기화
        self._init_database()
    
    def _init_database(self):
        """데이터베이스 테이블 초기화"""
        with self.connect() as conn:
            cursor = conn.cursor()
            
            # Users 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    user_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            
            # DB Codes 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS db_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    description TEXT,
                    category TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Jira Issues 캐시 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jira_issues_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    issue_key TEXT UNIQUE NOT NULL,
                    summary TEXT,
                    status TEXT,
                    assignee TEXT,
                    issue_type TEXT,
                    data JSON,
                    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Sessions 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    db_codes JSON,
                    selected_issue TEXT,
                    options JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Settings 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value JSON,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            
            # 샘플 데이터 삽입 (없는 경우에만)
            self._insert_sample_data(cursor)
            conn.commit()
    
    def _insert_sample_data(self, cursor):
        """샘플 데이터 삽입"""
        # 샘플 DB Codes 확인 및 삽입
        cursor.execute("SELECT COUNT(*) FROM db_codes")
        if cursor.fetchone()[0] == 0:
            sample_codes = [
                ('DB001', 'Production Database', 'Production'),
                ('DB002', 'Development Database', 'Development'),
                ('DB003', 'Testing Database', 'Testing'),
                ('DB004', 'Staging Database', 'Staging'),
                ('DB005', 'Analytics Database', 'Analytics'),
            ]
            cursor.executemany(
                "INSERT OR IGNORE INTO db_codes (code, description, category) VALUES (?, ?, ?)",
                sample_codes
            )
    
    def connect(self):
        """데이터베이스 연결 컨텍스트 매니저"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # dict-like access
        return conn
    
    # User 관련 메서드
    def create_user(self, user_id: str, user_name: str) -> int:
        """사용자 생성"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO users (user_id, user_name) 
                VALUES (?, ?)
            """, (user_id, user_name))
            
            # 마지막 로그인 시간 업데이트
            cursor.execute("""
                UPDATE users SET last_login = CURRENT_TIMESTAMP 
                WHERE user_id = ?
            """, (user_id,))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """사용자 정보 조회"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    # DB Code 관련 메서드
    def get_db_codes(self, category: str = None) -> List[Dict[str, Any]]:
        """DB Code 목록 조회"""
        with self.connect() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute(
                    "SELECT * FROM db_codes WHERE category = ? AND is_active = 1 ORDER BY code",
                    (category,)
                )
            else:
                cursor.execute(
                    "SELECT * FROM db_codes WHERE is_active = 1 ORDER BY code"
                )
            return [dict(row) for row in cursor.fetchall()]
    
    def get_db_code_categories(self) -> List[str]:
        """DB Code 카테고리 목록 조회"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT category FROM db_codes WHERE is_active = 1 ORDER BY category"
            )
            return [row[0] for row in cursor.fetchall()]
    
    def add_db_code(self, code: str, description: str, category: str) -> int:
        """DB Code 추가"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO db_codes (code, description, category) 
                VALUES (?, ?, ?)
            """, (code, description, category))
            conn.commit()
            return cursor.lastrowid
    
    # Jira Issue 캐시 관련 메서드
    def cache_jira_issue(self, issue_key: str, summary: str, status: str, 
                        assignee: str, issue_type: str, data: Dict[str, Any]):
        """Jira Issue 캐싱"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO jira_issues_cache 
                (issue_key, summary, status, assignee, issue_type, data, cached_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (issue_key, summary, status, assignee, issue_type, json.dumps(data)))
            conn.commit()
    
    def get_cached_issues(self, max_age_minutes: int = 60) -> List[Dict[str, Any]]:
        """캐시된 Issue 목록 조회"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM jira_issues_cache 
                WHERE datetime(cached_at) > datetime('now', '-' || ? || ' minutes')
                ORDER BY issue_key
            """, (max_age_minutes,))
            
            issues = []
            for row in cursor.fetchall():
                issue = dict(row)
                issue['data'] = json.loads(issue['data']) if issue['data'] else {}
                issues.append(issue)
            return issues
    
    # Session 관련 메서드
    def create_session(self, user_id: str, db_codes: Dict[str, Any], 
                      selected_issue: str, options: Dict[str, Any]) -> int:
        """세션 기록 생성"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sessions (user_id, db_codes, selected_issue, options, completed_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (user_id, json.dumps(db_codes), selected_issue, json.dumps(options)))
            conn.commit()
            return cursor.lastrowid
    
    def get_user_sessions(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """사용자 세션 기록 조회"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM sessions 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (user_id, limit))
            
            sessions = []
            for row in cursor.fetchall():
                session = dict(row)
                session['db_codes'] = json.loads(session['db_codes']) if session['db_codes'] else {}
                session['options'] = json.loads(session['options']) if session['options'] else {}
                sessions.append(session)
            return sessions
    
    # Settings 관련 메서드
    def get_setting(self, key: str, default: Any = None) -> Any:
        """설정 값 조회"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return default
    
    def set_setting(self, key: str, value: Any):
        """설정 값 저장"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, json.dumps(value)))
            conn.commit()
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()