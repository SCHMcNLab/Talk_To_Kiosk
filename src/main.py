# main.py
from llm import KioskAI
import db
from shop_list import ShoppingList
import result_parser as parser
import stt
import tts

import argparse
import threading
import time
from typing import Optional

from nicegui import ui, app
from kiosk_ui import build_ui, run_ui
import tts_engine


# -----------------------------
# 전역 공유 상태 (스레드 간 통신)
# -----------------------------
_pending_event = threading.Event()   # STT가 사용자 텍스트를 넣으면 set
_pending_text: str = ""

_reply_event = threading.Event()     # LLM/파싱 완료 후 set
_reply_text: str = ""

_ui_mode_lock = threading.Lock()
_ui_mode = 'listening'               # 'listening' | 'thinking' | 'speaking'
_stt_preview_text = ""               # STT 미리보기 텍스트

_worker_started = False
_worker_lock = threading.Lock()

_proc_lock = threading.Lock()        # LLM 처리 동시성 제한

_update_caption = None               # (str) -> None
_set_status = None                   # ('listening'|'thinking'|'speaking') -> None

# 정책 플래그
_llm_busy = threading.Event()        # LLM 추론/파싱 중이면 set()
ALLOW_LISTEN_DURING_TTS = True       # TTS 중에도 다시 듣기 허용(원치 않으면 False)


# -----------------------------
# 공용 헬퍼
# -----------------------------
def _set_mode(mode: str, preview: str = "") -> None:
    """워커/백그라운드에서 호출: UI는 건드리지 말고 플래그만 변경."""
    global _ui_mode, _stt_preview_text
    with _ui_mode_lock:
        _ui_mode = mode
        if preview:
            _stt_preview_text = preview


def handle_text(text: str) -> None:
    """모든 입력 경로의 단일 진입점: 텍스트를 큐에 적재."""
    global _pending_text
    if not text:
        return
    _pending_text = text
    _pending_event.set()


def _install_http_endpoint() -> None:
    """POST /api/say { "text": "..." }"""
    from fastapi import Request

    @app.post('/api/say')
    async def say(req: Request):
        payload = await req.json()
        text = (payload or {}).get('text', '')
        if text:
            _set_mode('thinking', preview=str(text))  # 도트/캡션 thinking 준비
            handle_text(str(text))                    # 동일 파이프라인으로 전달
        return {'ok': True}


# -----------------------------
# 메인
# -----------------------------
def main(argv: Optional[list[str]] = None):
    # --- 인자 파싱 ---
    p = argparse.ArgumentParser()
    p.add_argument('--native', action='store_true', help='네이티브 창 실행(배포 모드)')
    p.add_argument('--rate', type=int, default=170)
    p.add_argument('--voice', type=str, default='Heami')
    args = p.parse_args(argv)

    # === 무거운 객체는 반드시 main() 안에서 생성 ===
    shop_list = ShoppingList()
    llm_obj = KioskAI(db.prepare_chat_prompt(1))
    stt_handler = stt.STTProcessor(
        aggressiveness=2,
        whisper_model_name="base",
        noise_threshold_db=-40,
        silence_threshold_seconds=3.0
    )

    # 1) TTS 워커 시작
    tts_engine.start(rate=args.rate, volume=1.0, voice_keyword=args.voice)

    # 2) UI 빌드
    global _update_caption, _set_status
    _update_caption, _set_status = build_ui()
    _set_status('listening')
    _update_caption('어서 오십시오. 무엇을 도와드릴까요?')

    # 3) HTTP 테스트 엔드포인트
    _install_http_endpoint()

    # (3.5) STT 워커 시작 (중복 방지)
    def _stt_worker():
        while True:
            try:
                # LLM 처리 중이면 마이크 대기 금지
                if _llm_busy.is_set():
                    time.sleep(0.05)
                    continue

                # 선택: TTS 중 재청취 허용/차단 정책
                if not ALLOW_LISTEN_DURING_TTS and tts_engine.is_speaking():
                    time.sleep(0.05)
                    continue

                _set_mode('listening')  # 듣는 중(플래그만)
                text = stt_handler.record_sound_to_text()  # 블로킹 대기
                if not text:
                    continue

                # STT 결과 생성 직후: 도트/캡션 thinking을 위한 플래그만 설정
                _set_mode('thinking', preview=text)
                handle_text(text)  # 실제 처리는 poll()에서
            except Exception as e:
                print(f"[STT] 오류: {e}")
                time.sleep(0.2)

    def _start_stt_worker_once():
        global _worker_started
        with _worker_lock:
            if _worker_started:
                return
            threading.Thread(target=_stt_worker, name="STTWorker", daemon=True).start()
            _worker_started = True

    _start_stt_worker_once()

    # 4) UI 타이머: 상태/대기열 반영 + LLM 비동기 트리거
    def _process_text_async(user_text: str):
        """무거운 처리(LLM/DB/파서)는 백그라운드에서 실행 → 결과만 이벤트로 전달."""
        global _reply_text
        with _proc_lock:
            try:
                # === 실제 로직 시작 ===
                # 1) LLM 호출
                llm_response = llm_obj.ask(user_text)

                # 2) LLM 응답 파싱 (대화 텍스트, 함수 호출 목록)
                conversation_text, function_calls = parser.parse_llm_response(llm_response)

                # 3) 장바구니 반영
                try:
                    if function_calls is None:
                        function_calls = []
                    elif not isinstance(function_calls, list):
                        function_calls = [function_calls]
                    for call in function_calls:
                        shop_list.apply(call)
                except Exception as e:
                    print("[Cart] apply 실패:", e)

                # 4) 사용자에게 표시할 응답 텍스트 정리
                reply_text = (conversation_text or "").strip() or "처리되었습니다."
                print(reply_text)  # 로그 출력
                # === 실제 로직 끝 ===

            except Exception as e:
                reply_text = f"오류가 발생했습니다: {e}"
                print("[PROC] 예외:", e)

            finally:
                _reply_text = reply_text
                _reply_event.set()   # 결과 준비 완료
                _llm_busy.clear()    # LLM 종료 → STT 재개 허용

    def poll():
        # 상태 결정 우선순위: speaking > thinking > listening
        speaking_now = tts_engine.is_speaking()
        llm_busy_now = _llm_busy.is_set()

        with _ui_mode_lock:
            current_mode = _ui_mode
            preview = _stt_preview_text

        if speaking_now:
            _set_status('speaking')
        elif llm_busy_now or current_mode == 'thinking':
            _set_status('thinking')
            if preview:
                _update_caption(preview)
        else:
            _set_status('listening')

        # 1) STT가 새 텍스트를 넣었으면 → LLM 비동기 처리 시작
        if _pending_event.is_set():
            _pending_event.clear()
            text = _pending_text.strip()
            if text:
                # thinking 표시는 위에서 이미 처리됨(우선순위로 보호됨)
                _update_caption(text)
                _llm_busy.set()  # LLM 시작: STT 금지
                threading.Thread(
                    target=_process_text_async, args=(text,), name="LLMWorker", daemon=True
                ).start()

        # 2) 비동기 처리 결과가 도착했으면 → 답변중 + 자막 + TTS
        if _reply_event.is_set():
            _reply_event.clear()
            reply = _reply_text
            _set_status('speaking')
            _update_caption(reply)
            tts_engine.speak(reply)

        # speaking/end는 다음 틱에서 우선순위 로직으로 자동 반영됨

    ui.timer(0.05, poll)

    # 5) 실행
    try:
        run_ui(native=bool(args.native), reload=False)
    finally:
        # 6) 종료 처리
        try:
            # STT 리소스 정리
            if hasattr(stt_handler, 'audio'):
                stt_handler.audio.terminate()
        except Exception:
            pass
        tts_engine.stop()


if __name__ == '__main__':
    main(["--native"])
