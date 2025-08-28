"""인증 컨트롤러 - 로그인/로그아웃 비즈니스 로직"""

import hashlib
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class AuthController:
    """인증 관련 비즈니스 로직 처리"""
    
    def __init__(self):
        self.max_login_attempts = 5
        self.lockout_duration = 30  # minutes
        self.failed_attempts = {}  # user_id: {'count': int, 'last_attempt': datetime}
        
    def authenticate(self, user_id: str, password: str, jira_url: str = None) -> Dict[str, Any]:
        """
        사용자 인증 처리
        
        Returns:
            dict: 인증 결과 {'success': bool, 'user_info': dict, 'error': str}
        """
        # 로그인 시도 제한 확인
        if self.is_account_locked(user_id):
            return {'success': False, 'error': '계정이 잠겼습니다. 30분 후 다시 시도하세요.'}
        
        # Jira API 인증 시도 (jira_url이 제공된 경우)
        if jira_url and user_id and password:
            try:
                # Jira API 모듈을 사용한 인증 테스트
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'atlassian_api'))
                from atlassian_api import JiraAPI
                
                jira_client = JiraAPI(
                    domain_url=jira_url,
                    user_id=user_id,
                    password=password
                )
                # 연결 테스트
                user_info = jira_client.get_current_user()
                
                return {
                    'success': True,
                    'user_info': {
                        'user_id': user_id,
                        'user_name': user_info.get('displayName', user_id),
                        'email': user_info.get('emailAddress', ''),
                        'jira_url': jira_url,
                        'role': 'user',
                        'permissions': ['read', 'write'],
                        'last_login': datetime.now().isoformat()
                    },
                    'token': self.generate_token(user_id),
                    'jira_credentials': {
                        'url': jira_url,
                        'user_id': user_id,
                        'password': password
                    }
                }
            except Exception as e:
                print(f"Jira 인증 실패: {e}")
                # Jira 인증 실패 시 계속 진행
        
        # 기존 로컬 인증 (개발용)
        if user_id == 'admin' and password == 'admin':
            return {
                'success': True,
                'user_info': {
                    'user_id': user_id,
                    'user_name': 'Administrator',
                    'role': 'admin',
                    'permissions': ['all'],
                    'last_login': datetime.now().isoformat()
                },
                'token': self.generate_token(user_id)
            }
        
        # 실패 처리
        self.record_failed_attempt(user_id)
        return {
            'success': False,
            'error': '아이디 또는 비밀번호가 올바르지 않습니다.'
        }
    
    def validate_input(self, user_id: str, password: str) -> tuple[bool, str]:
        """
        입력값 유효성 검증
        
        TODO: [입력 검증 로직]
        - SQL Injection 방지
        - XSS 방지
        - 형식 검증
        """
        if not user_id or not password:
            return False, "아이디와 비밀번호를 입력해주세요."
        
        # TODO: 추가 검증 로직
        # if len(password) < 8:
        #     return False, "비밀번호는 8자 이상이어야 합니다."
        
        # if not re.match(r'^[a-zA-Z0-9_]+$', user_id):
        #     return False, "아이디는 영문자, 숫자, 언더스코어만 사용 가능합니다."
        
        return True, ""
    
    def hash_password(self, password: str) -> str:
        """
        비밀번호 해싱
        
        TODO: [보안 강화]
        - bcrypt 또는 argon2 사용
        - Salt 추가
        """
        # 임시 SHA256 해싱 (실제로는 bcrypt 사용 권장)
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_token(self, user_id: str) -> str:
        """
        인증 토큰 생성
        
        TODO: [JWT 토큰 구현]
        - JWT 라이브러리 사용
        - 만료 시간 설정
        - Refresh token 구현
        """
        # 임시 토큰 생성
        timestamp = str(int(time.time()))
        token_str = f"{user_id}:{timestamp}"
        return hashlib.sha256(token_str.encode()).hexdigest()
    
    def verify_token(self, token: str) -> bool:
        """
        토큰 유효성 검증
        
        TODO: [토큰 검증 로직]
        - 서명 검증
        - 만료 시간 확인
        """
        # 임시 구현
        return len(token) == 64  # SHA256 길이
    
    def record_failed_attempt(self, user_id: str):
        """
        실패한 로그인 시도 기록
        
        TODO: [보안 강화]
        - 데이터베이스에 기록
        - IP 주소별 추적
        """
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = {'count': 0, 'last_attempt': None}
        
        self.failed_attempts[user_id]['count'] += 1
        self.failed_attempts[user_id]['last_attempt'] = datetime.now()
    
    def is_account_locked(self, user_id: str) -> bool:
        """
        계정 잠금 상태 확인
        
        TODO: [잠금 정책 구현]
        - 시간 기반 잠금 해제
        - 관리자 잠금 해제
        """
        if user_id not in self.failed_attempts:
            return False
        
        attempts = self.failed_attempts[user_id]
        if attempts['count'] >= self.max_login_attempts:
            if attempts['last_attempt']:
                lockout_until = attempts['last_attempt'] + timedelta(minutes=self.lockout_duration)
                if datetime.now() < lockout_until:
                    return True
                else:
                    # 잠금 해제
                    self.failed_attempts[user_id] = {'count': 0, 'last_attempt': None}
        
        return False
    
    def logout(self, token: str) -> bool:
        """
        로그아웃 처리
        
        TODO: [로그아웃 구현]
        - 토큰 무효화
        - 세션 정리
        - 로그 기록
        """
        # TODO: 토큰 블랙리스트 추가
        # blacklist.add_token(token)
        
        return True
    
    def check_mfa(self, user_id: str, otp_code: str) -> bool:
        """
        다단계 인증 확인
        
        TODO: [MFA 구현]
        - TOTP/HOTP 검증
        - SMS OTP
        - 이메일 OTP
        """
        # 임시 구현
        return otp_code == "123456"
    
    def get_user_permissions(self, user_id: str) -> list:
        """
        사용자 권한 조회
        
        TODO: [권한 관리]
        - RBAC 구현
        - 동적 권한 로드
        """
        # 임시 권한
        if user_id == 'admin':
            return ['read', 'write', 'delete', 'admin']
        else:
            return ['read', 'write']