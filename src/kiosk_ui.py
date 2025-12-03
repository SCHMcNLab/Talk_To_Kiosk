# kiosk_ui.py
from __future__ import annotations
from nicegui import ui, app
from typing import Callable
from pathlib import Path

# 전역 윈도우/앱 설정
app.native.window_args['title'] = 'AI Kiosk'
app.native.window_args['width'] = 480
app.native.window_args['height'] = 720
app.native.start_args['debug'] = False

_UI_CSS = '''
:root { color-scheme: light; }
body { background: #0b0c10; }
.container { height: 100vh; display:flex; flex-direction:column; align-items:center; justify-content:flex-start; gap:18px; padding-top:8vh; }
.avatar-wrap { width:280px; height:280px; border-radius:22px; background:rgba(255,255,255,0.04); display:flex; align-items:center; justify-content:center; overflow:hidden; box-shadow:0 8px 24px rgba(0,0,0,0.35); }
.avatar { width:85%; height:85%; object-fit:contain; animation:breathe 4s ease-in-out infinite; }
@keyframes breathe { 0%{transform:scale(1.00);} 50%{transform:scale(1.02);} 100%{transform:scale(1.00);} }
.caption { font-size:26px; line-height:1.35; color:#e8eef2; text-align:center; max-width:70ch; }
.status { display:flex; align-items:center; gap:10px; color:#93a1a1; font-size:14px; letter-spacing:.2px; }
.dot { width:12px; height:12px; border-radius:50%; background:#3498db; box-shadow:0 0 10px rgba(52,152,219,0.85); }
.dot.talking { background:#e74c3c; box-shadow:0 0 10px rgba(231,76,60,0.95); }
.dot.thinking { background:#f1c40f; box-shadow:0 0 10px rgba(241,196,15,0.95); }
'''

_css_done = False


def build_ui() -> tuple[Callable[[str], None], Callable[[str], None]]:
    """
    UI를 구성하고, 두 가지 콜백을 반환한다.
    - update_caption(text): 자막 갱신
    - set_speaking(is_on): 상태 도트/문구 갱신
    """
    global _css_done
    if not _css_done:
        ui.add_css(_UI_CSS)
        _css_done = True

    # ✅ kiosk_ui.py 파일 위치 기준으로 static 디렉터리 고정
    base_dir = Path(__file__).resolve().parent
    static_dir = base_dir / 'static'  # 여기에 cashier.webp 존재해야 함
    mount_url = '/static'

    if static_dir.is_dir():
        # 이미 마운트했는지 중복 방지(옵션) — NiceGUI는 중복 마운트에 예민할 수 있음
        try:
            app.add_static_files(mount_url, str(static_dir))
        except Exception:
            pass  # 이미 마운트되어 있다면 무시

        img_src = f'{mount_url}/cashier.webp'
    else:
        print(f'[UI] static 폴더를 찾을 수 없습니다: {static_dir}')
        img_src = None

    with ui.element('div').classes('container'):
        wrapper = ui.element('div').classes('avatar-wrap').style('position:relative;')
        with wrapper:
            if img_src:
                ui.image(img_src).classes('avatar').props('draggable=false')
            else:
                ui.label('이미지를 찾을 수 없습니다').style('color:#ccc')

        ui.element('div').style('height:8px')

        status_row = ui.row().classes('status')
        with status_row:
            status_dot = ui.element('div').classes('dot')  # 기본 파랑
            status_text = ui.html('<span>말씀해주세요</span>')

        caption = ui.label('어서 오십시오. 무엇을 도와드릴까요?').classes('caption')

    def update_caption(text: str) -> None:
        caption.set_text(text)

    def set_status(mode: str) -> None:
        # mode in {'listening','thinking','speaking'}
        status_row.clear()
        with status_row:
            cls = 'dot'
            label = '말씀해주세요'
            if mode == 'speaking':
                cls = 'dot talking'; label = '답변중'
            if mode == 'thinking':
                cls = 'dot thinking'; label = '생각중'
            ui.element('div').classes(cls)
            ui.html(f'<span>{label}</span>')

    # ✅ 기존 호환용 (불린을 speaking으로 해석)
    def set_speaking(is_on: bool) -> None:
        set_status('speaking' if is_on else 'listening')

    # 반환 시 새로운 시그니처 우선: (update_caption, set_status)
    return update_caption, set_status


def run_ui(native: bool = True, reload: bool = False) -> None:
    ui.run(native=native, reload=reload)
