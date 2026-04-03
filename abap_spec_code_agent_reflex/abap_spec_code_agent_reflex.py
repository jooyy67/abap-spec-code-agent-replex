import reflex as rx
from .state import State # State가 StateMain의 모든 기능을 포함함
from .components import *

def sidebar_item(text: str):
    # 호버/클릭 여부에 따른 디자인 변경
    is_active = (State.current_section == text) | (State.hovered_section == text)
    
    return rx.box(
        rx.hstack(
            rx.text(text, color=rx.cond(is_active, "#2b6cb0", "#4a5568"), font_weight=rx.cond(is_active, "600", "400")),
            rx.cond(State.hovered_section == text, rx.icon("arrow-right", size=18, color="#2b6cb0"), rx.fragment()),
            justify="between", width="100%", align="center",
        ),
        padding="0.8em 1em", border_radius="10px",
        background_color=rx.cond(State.hovered_section == text, "#edf2f7", "transparent"),
        cursor="pointer",
        on_click=lambda: State.set_current_section(text),
        on_mouse_enter=lambda: State.set_hovered_section(text),
        on_mouse_leave=lambda: State.set_hovered_section(""),
        width="100%", transition="all 0.2s ease",
    )

def main_monitor():
    return rx.center(
        rx.box(
            # 모니터 스탠드
            rx.box(width="150px", height="15px", background_color="#cbd5e0", position="absolute", bottom="-15px", left="50%", transform="translateX(-50%)", border_radius="0 0 8px 8px"),
            # 내부 화면
            rx.box(
                rx.vstack(
                    rx.heading(State.current_section, size="6", color="#2b6cb0", margin_bottom="1em"),
                    # 섹션별 뷰 전환
                    rx.cond(State.current_section == State.sections[0], view_section_1()),
                    rx.cond(State.current_section == State.sections[1], view_section_2()),
                    rx.cond(State.current_section == State.sections[2], view_section_3()),
                    rx.cond(State.current_section == State.sections[3], view_section_4()),
                    rx.cond(State.current_section == State.sections[4], view_section_5()),
                    rx.cond(State.current_section == State.sections[5], view_section_6()),
                    rx.button("상세 분석 및 FS 생성 시작", on_click=State.handle_submit, color_scheme="blue", width="100%", margin_top="2em"),
                    spacing="4", width="100%", align_items="start"
                ),
                padding="2.5em", background_color="white", height="100%", overflow_y="auto", border_radius="15px",
            ),
            border="12px solid #1a202c", border_radius="25px", width="850px", height="650px", position="relative",
            box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        ),
        width="100%", height="100vh", background_color="#f8fafc"
    )

def index():
    return rx.hstack(
        # 왼쪽 사이드바
        rx.vstack(
            rx.heading("ABAP Spec Agent", size="7", margin_bottom="1em"),
            rx.foreach(State.sections, sidebar_item),
            width="320px", height="100vh", padding="3em 2em", border_right="1px solid #e2e8f0", align_items="start",
        ),
        # 오른쪽 메인 모니터
        main_monitor(),
        width="100%", spacing="0"
    )

app = rx.App(theme=rx.theme(appearance="light", accent_color="blue"))
app.add_page(index)