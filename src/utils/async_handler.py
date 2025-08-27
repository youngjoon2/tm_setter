"""비동기 처리를 위한 핸들러 모듈"""

import threading
import queue
from typing import Callable, Any, Optional
import time


class AsyncHandler:
    """GUI 응답성을 유지하면서 백그라운드 작업을 처리하는 핸들러"""
    
    def __init__(self):
        self.task_queue: queue.Queue = queue.Queue()
        self.result_callbacks: dict = {}
        self.error_callbacks: dict = {}
        self.worker_threads: list = []
        self.running: bool = True
        
    def run_async(self, 
                  func: Callable, 
                  args: tuple = (), 
                  kwargs: dict = None,
                  callback: Optional[Callable] = None,
                  error_callback: Optional[Callable] = None) -> str:
        """
        비동기로 함수를 실행
        
        Args:
            func: 실행할 함수
            args: 함수 인자 (튜플)
            kwargs: 함수 키워드 인자 (딕셔너리)
            callback: 성공 시 콜백 함수
            error_callback: 실패 시 콜백 함수
            
        Returns:
            task_id: 작업 ID
        """
        if kwargs is None:
            kwargs = {}
            
        task_id = f"task_{id(func)}_{time.time()}"
        
        if callback:
            self.result_callbacks[task_id] = callback
        if error_callback:
            self.error_callbacks[task_id] = error_callback
            
        # 작업을 큐에 추가
        self.task_queue.put({
            'id': task_id,
            'func': func,
            'args': args,
            'kwargs': kwargs
        })
        
        # 워커 스레드가 없으면 생성
        if not self.worker_threads or all(not t.is_alive() for t in self.worker_threads):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.worker_threads.append(worker)
            
        return task_id
    
    def _worker(self):
        """백그라운드 워커 스레드"""
        while self.running:
            try:
                # 큐에서 작업 가져오기 (1초 타임아웃)
                task = self.task_queue.get(timeout=1)
                
                task_id = task['id']
                func = task['func']
                args = task['args']
                kwargs = task['kwargs']
                
                try:
                    # 함수 실행
                    result = func(*args, **kwargs)
                    
                    # 성공 콜백 실행
                    if task_id in self.result_callbacks:
                        callback = self.result_callbacks[task_id]
                        callback(result)
                        del self.result_callbacks[task_id]
                        
                except Exception as e:
                    # 에러 콜백 실행
                    if task_id in self.error_callbacks:
                        error_callback = self.error_callbacks[task_id]
                        error_callback(e)
                        del self.error_callbacks[task_id]
                    else:
                        print(f"Error in async task {task_id}: {e}")
                        
                self.task_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Worker thread error: {e}")
                
    def stop(self):
        """핸들러 종료"""
        self.running = False
        for thread in self.worker_threads:
            if thread.is_alive():
                thread.join(timeout=2)


class LoadingIndicator:
    """로딩 인디케이터 관리"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.loading_window = None
        
    def show(self, message: str = "처리 중..."):
        """로딩 인디케이터 표시"""
        import tkinter as tk
        from tkinter import ttk
        
        if self.loading_window:
            return
            
        self.loading_window = tk.Toplevel(self.parent)
        self.loading_window.title("")
        self.loading_window.geometry("300x100")
        self.loading_window.resizable(False, False)
        
        # 부모 창 중앙에 위치
        self.loading_window.transient(self.parent)
        self.loading_window.grab_set()
        
        # 메시지 라벨
        label = tk.Label(self.loading_window, text=message, font=("Arial", 12))
        label.pack(pady=20)
        
        # 진행바
        progress = ttk.Progressbar(self.loading_window, mode='indeterminate')
        progress.pack(pady=10, padx=20, fill='x')
        progress.start(10)
        
        # 창 중앙 배치
        self.loading_window.update_idletasks()
        x = (self.loading_window.winfo_screenwidth() // 2) - (self.loading_window.winfo_width() // 2)
        y = (self.loading_window.winfo_screenheight() // 2) - (self.loading_window.winfo_height() // 2)
        self.loading_window.geometry(f"+{x}+{y}")
        
    def hide(self):
        """로딩 인디케이터 숨기기"""
        if self.loading_window:
            self.loading_window.destroy()
            self.loading_window = None