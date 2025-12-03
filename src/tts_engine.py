# tts_engine.py
# 큐 없이: 공유변수 + Event로 pyttsx3 전용 스레드에 텍스트 전달
import threading
import time
import pyttsx3

# --- 내부 공유 상태 ---
_new_text_event = threading.Event()
_shutdown_event = threading.Event()
_speaking_event = threading.Event()
_shared_text = ""

_worker_thread: threading.Thread | None = None


def _pick_korean_voice(engine, keyword: str | None = "Heami"):
    """한국어 보이스가 있으면 선택(없으면 기본 유지)"""
    try:
        voices = engine.getProperty('voices')
        # 1) 키워드 우선
        if keyword:
            for v in voices:
                name_id = f"{getattr(v,'name','')} {getattr(v,'id','')}".lower()
                if keyword.lower() in name_id:
                    engine.setProperty('voice', v.id)
                    return
        # 2) 한국어 힌트
        for v in voices:
            name_id = f"{getattr(v,'name','')} {getattr(v,'id','')}".lower()
            if "korean" in name_id or "ko-" in name_id or "heami" in name_id:
                engine.setProperty('voice', v.id)
                return
    except Exception:
        pass


def _worker(rate=170, volume=1.0, voice_keyword="Heami"):
    # Windows SAPI5: 워커 스레드에서 COM STA 초기화 권장
    pythoncom = None
    try:
        import pythoncom
        pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
    except Exception:
        pythoncom = None

    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', int(rate))
    engine.setProperty('volume', float(volume))
    _pick_korean_voice(engine, voice_keyword)

    # 발화 종료/에러 시 speaking 해제
    def _on_finished(name, completed):
        _speaking_event.clear()

    def _on_error(name, exc):
        _speaking_event.clear()

    engine.connect('finished-utterance', _on_finished)
    engine.connect('error', _on_error)

    # 논블로킹 루프 시작
    engine.startLoop(False)
    try:
        while not _shutdown_event.is_set():
            if _new_text_event.is_set():
                _new_text_event.clear()
                text = _get_pending_text().strip()
                if text:
                    try:
                        # 잔류 발화/큐 정리
                        try:
                            engine.stop()
                        except Exception:
                            pass
                        _speaking_event.set()   # 상태: 말하는 중
                        engine.say(text)
                    except Exception:
                        _speaking_event.clear()

            engine.iterate()
            time.sleep(0.005)  # CPU 점유 방지
    finally:
        try:
            engine.endLoop()
            engine.stop()
        except Exception:
            pass
        if pythoncom:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass


def _get_pending_text() -> str:
    return _shared_text


def speak(text: str) -> None:
    """최신 텍스트만 유지(덮어쓰기)"""
    global _shared_text
    _shared_text = text
    _new_text_event.set()


def is_speaking() -> bool:
    """현재 '말하는 중' 여부"""
    return _speaking_event.is_set()


def start(rate: int = 170, volume: float = 1.0, voice_keyword: str | None = "Heami"):
    """전용 워커 스레드 기동 (한 번만 호출)"""
    global _worker_thread
    if _worker_thread and _worker_thread.is_alive():
        return
    _shutdown_event.clear()
    _worker_thread = threading.Thread(
        target=_worker,
        kwargs={"rate": rate, "volume": volume, "voice_keyword": voice_keyword},
        name="TTSWorker",
        daemon=True,
    )
    _worker_thread.start()


def stop(timeout: float = 1.5):
    """전용 워커 스레드 종료"""
    _shutdown_event.set()
    if _worker_thread:
        _worker_thread.join(timeout=timeout)
