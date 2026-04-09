import reflex as rx
from .state import State # State가 StateMain의 모든 기능을 포함함
from .components import *

def sidebar_item(text: str, href: str, indent: bool = True):
    # 호버/클릭 여부에 따른 디자인 변경
    is_active = (State.current_section == text) | (State.hovered_section == text)
    
    return rx.link(
        rx.box(
            rx.hstack(
                rx.text(
                    text,
                    color=rx.cond(is_active, "#2b6cb0", "#4a5568"),
                    font_weight=rx.cond(is_active, "600", "400"),
                ),
                rx.cond(
                    State.hovered_section == text,
                    rx.icon("arrow-right", size=18, color="#2b6cb0"),
                    rx.fragment(),
                ),
                justify="between",
                width="100%",
                align="center",
            ),
            padding=rx.cond(indent, "0.65em 0.9em 0.65em 1.3em", "0.65em 0.9em"),
            border_radius="10px",
            background_color=rx.cond(State.hovered_section == text, "#edf2f7", "transparent"),
            cursor="pointer",
            on_click=lambda: State.set_current_section(text),
            on_mouse_enter=lambda: State.set_hovered_section(text),
            on_mouse_leave=lambda: State.set_hovered_section(""),
            width="100%",
            transition="all 0.2s ease",
        ),
        href=href,
        underline="none",
    )


def sidebar_group_title(text: str, group_key: str, on_click):
    is_open = State.expanded_sidebar_group == group_key
    return rx.box(
        rx.hstack(
            rx.text(
                text,
                font_weight="700",
                color="#2d3748",
                font_size="0.95em",
            ),
            rx.icon(
                rx.cond(is_open, "chevron-down", "chevron-right"),
                size=16,
                color="#4a5568",
            ),
            justify="between",
            width="100%",
            align="center",
        ),
        width="100%",
        padding="0.55em 0.65em",
        border_radius="10px",
        background_color=rx.cond(is_open, "#f1f5f9", "transparent"),
        cursor="pointer",
        on_click=on_click,
        transition="all 0.2s ease",
    )

def main_monitor():
    def section_block(section_id: str, title: str, content):
        return rx.box(
            rx.heading(title, size="5", color="#2b6cb0", margin_top="0.25em"),
            content,
            id=section_id,
            width="100%",
            padding_top="0.75em",
            scroll_margin_top="1.25em",
        )

    return rx.box(
        rx.box(
            rx.vstack(
                rx.cond(
                    State.expanded_sidebar_group == "input",
                    rx.fragment(
                        section_block(State.input_section_ids[0], State.input_sections[0], view_section_1()),
                        section_block(State.input_section_ids[1], State.input_sections[1], view_section_2()),
                        section_block(State.input_section_ids[2], State.input_sections[2], view_section_3()),
                        section_block(State.input_section_ids[3], State.input_sections[3], view_section_4()),
                        section_block(State.input_section_ids[4], State.input_sections[4], view_section_5()),
                        section_block(State.input_section_ids[5], State.input_sections[5], view_section_6()),
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    State.expanded_sidebar_group == "fs",
                    rx.fragment(
                        section_block(State.fs_section_ids[0], State.fs_sections[0], view_fs_section_1()),
                        section_block(State.fs_section_ids[1], State.fs_sections[1], view_fs_section_2()),
                        section_block(State.fs_section_ids[2], State.fs_sections[2], view_fs_section_3()),
                        section_block(State.fs_section_ids[3], State.fs_sections[3], view_fs_section_4()),
                        section_block(State.fs_section_ids[4], State.fs_sections[4], view_fs_section_5()),
                        section_block(State.fs_section_ids[5], State.fs_sections[5], view_fs_section_6()),
                        section_block(State.fs_section_ids[6], State.fs_sections[6], view_fs_section_7()),
                        section_block(State.fs_section_ids[7], State.fs_sections[7], view_fs_section_8()),
                        section_block(State.fs_section_ids[8], State.fs_sections[8], view_fs_section_9()),
                        section_block(State.fs_section_ids[9], State.fs_sections[9], view_fs_section_10()),
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    State.expanded_sidebar_group == "code",
                    rx.fragment(
                        section_block(State.code_section_ids[0], State.code_sections[0], view_code_gen()),
                    ),
                    rx.fragment(),
                ),
                rx.button(
                    "상세 분석 및 FS 생성 시작",
                    on_click=State.handle_submit,
                    color_scheme="blue",
                    width="100%",
                    margin_top="2em",
                ),
                spacing="4",
                width="100%",
                align_items="start",
            ),
            width="min(1100px, 100%)",
            height="calc(100vh - 4rem)",
            padding="2.5em",
            background_color="white",
            overflow_y="auto",
            border_radius="16px",
            box_shadow="0 20px 45px -18px rgba(0, 0, 0, 0.18)",
            border="1px solid #e2e8f0",
        ),
        width="100%",
        height="100vh",
        padding="2rem",
        background_color="#f8fafc",
        display="flex",
        justify_content="center",
        align_items="flex-start",
    )

def index():
    return rx.hstack(
        # 왼쪽 사이드바
        rx.vstack(
            rx.heading("ABAP Spec Agent", size="7", margin_bottom="1em"),
            sidebar_group_title("사용자 입력 방식", "input", State.toggle_input_group),
            rx.cond(
                State.expanded_sidebar_group == "input",
                rx.vstack(
                    sidebar_item(State.input_sections[0], href="#input-1", indent=True),
                    sidebar_item(State.input_sections[1], href="#input-2", indent=True),
                    sidebar_item(State.input_sections[2], href="#input-3", indent=True),
                    sidebar_item(State.input_sections[3], href="#input-4", indent=True),
                    sidebar_item(State.input_sections[4], href="#input-5", indent=True),
                    sidebar_item(State.input_sections[5], href="#input-6", indent=True),
                    spacing="0",
                    width="100%",
                    align_items="start",
                ),
                rx.fragment(),
            ),
            sidebar_group_title("Functional Spec & 개발매핑 입력서", "fs", State.toggle_fs_group),
            rx.cond(
                State.expanded_sidebar_group == "fs",
                rx.vstack(
                    sidebar_item(State.fs_sections[0], href="#fs-1", indent=True),
                    sidebar_item(State.fs_sections[1], href="#fs-2", indent=True),
                    sidebar_item(State.fs_sections[2], href="#fs-3", indent=True),
                    sidebar_item(State.fs_sections[3], href="#fs-4", indent=True),
                    sidebar_item(State.fs_sections[4], href="#fs-5", indent=True),
                    sidebar_item(State.fs_sections[5], href="#fs-6", indent=True),
                    sidebar_item(State.fs_sections[6], href="#fs-7", indent=True),
                    sidebar_item(State.fs_sections[7], href="#fs-8", indent=True),
                    sidebar_item(State.fs_sections[8], href="#fs-9", indent=True),
                    sidebar_item(State.fs_sections[9], href="#fs-10", indent=True),
                    spacing="0",
                    width="100%",
                    align_items="start",
                ),
                rx.fragment(),
            ),
            sidebar_group_title("Code 생성", "code", State.toggle_code_group),
            rx.cond(
                State.expanded_sidebar_group == "code",
                rx.vstack(
                    sidebar_item(State.code_sections[0], href="#code-1", indent=True),
                    spacing="0",
                    width="100%",
                    align_items="start",
                ),
                rx.fragment(),
            ),
            width="360px",
            height="100vh",
            padding="2.25em 1.5em",
            border_right="1px solid #e2e8f0",
            align_items="start",
            overflow_y="auto",
            position="sticky",
            top="0",
            align_self="flex-start",
        ),
        # 오른쪽 메인 모니터
        main_monitor(),
        width="100%", spacing="0"
    )

app = rx.App(theme=rx.theme(appearance="light", accent_color="blue"))
app.add_page(index)