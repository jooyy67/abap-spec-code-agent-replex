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
            # FS 탭은 내부에서 좌/우 패널 타이틀을 이미 표시하므로, 상단 파란 섹션 타이틀은 숨김
            rx.cond(
                State.expanded_sidebar_group == "fs",
                rx.fragment(),
                rx.heading(title, size="5", color="#2b6cb0", margin_top="0.25em"),
            ),
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
                rx.cond(
                    State.expanded_sidebar_group != "fs",
                    rx.button(
                        "상세 분석 및 FS 생성 시작",
                        on_click=State.handle_submit,
                        color_scheme="blue",
                        width="100%",
                        margin_top="2em",
                    ),
                    rx.fragment(),
                ),
                spacing="4",
                width="100%",
                align_items="start",
                # FS 탭에서 하단 빈 공간이 생기지 않도록 flex로 꽉 채움
                style={"height": "100%", "minHeight": "0"},
            ),
            # FS 탭(2열)은 화면을 더 꽉 차게 사용
            width=rx.cond(State.expanded_sidebar_group == "fs", "100%", "min(1100px, 100%)"),
            max_width=rx.cond(
                State.expanded_sidebar_group == "fs",
                rx.cond(State.sidebar_collapsed, "calc(100vw - 2rem)", "calc(100vw - 360px - 2rem)"),
                "1100px",
            ),
            height="100%",
            padding=rx.cond(State.expanded_sidebar_group == "fs", "1.1em", "2.5em"),
            background_color="white",
            overflow_y="auto",
            border_radius="16px",
            box_shadow="0 20px 45px -18px rgba(0, 0, 0, 0.18)",
            border="1px solid #e2e8f0",
            box_sizing="border-box",
        ),
        width="100%",
        height="100vh",
        padding=rx.cond(State.expanded_sidebar_group == "fs", "0.75rem", "2rem"),
        background_color="#f8fafc",
        display="flex",
        justify_content=rx.cond(State.expanded_sidebar_group == "fs", "stretch", "center"),
        align_items="stretch",
        overflow="hidden",
        box_sizing="border-box",
    )

def index():
    return rx.box(
        # 전역(바깥) 스크롤 제거: body/html/root를 고정
        rx.el.style(
            """
            html, body {
              height: 100%;
              overflow: hidden;
              margin: 0;
            }
            #__next {
              height: 100%;
              overflow: hidden;
            }

            /* Markdown table: allow horizontal scroll without squishing */
            .md-scroll {
              overflow-x: auto;
              max-width: 100%;
            }
            .md-scroll table {
              width: max-content;
              min-width: 100%;
              border-collapse: collapse;
            }

            /* Markdown rendering polish */
            .md-render {
              color: #1f2937;
              line-height: 1.55;
              font-size: 0.95rem;
            }
            .md-render h1, .md-render h2, .md-render h3 {
              margin: 0.4rem 0 0.35rem 0;
              line-height: 1.25;
              color: #1f2937;
            }
            .md-render h2 { font-size: 1.15rem; }
            .md-render h3 { font-size: 1.05rem; }
            .md-render p { margin: 0.35rem 0; }
            .md-render ul, .md-render ol { margin: 0.35rem 0 0.35rem 1.2rem; }
            .md-render li { margin: 0.15rem 0; }
            .md-render hr {
              border: 0;
              border-top: 1px solid #eef2f7;
              margin: 0.75rem 0;
            }

            .md-render table {
              /* In md-render, prefer fitting container over max-content */
              width: 100% !important;
              table-layout: fixed;
              border: 1px solid #eef2f7;
              border-radius: 12px;
              overflow: hidden;
              background: white;
              box-shadow: 0 1px 0 rgba(15, 23, 42, 0.03);
            }
            .md-render th, .md-render td {
              border-bottom: 1px solid #f1f5f9;
              padding: 0.4rem 0.55rem;
              vertical-align: top;
              text-align: center;
              white-space: normal;
              word-break: keep-all;
              overflow-wrap: anywhere;
              font-size: 0.9rem;
            }
            .md-render th {
              background: #fafcff;
              font-weight: 700;
              color: #111827;
            }
            .md-render tr:last-child td { border-bottom: none; }

            .md-render code {
              background: #f1f5f9;
              padding: 0.12rem 0.25rem;
              border-radius: 6px;
              font-size: 0.9em;
            }
            """.strip()
        ),
        rx.hstack(
            # 왼쪽 사이드바
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            rx.cond(
                                State.sidebar_collapsed,
                                rx.icon("panel-left-open", size=18, color="#4a5568"),
                                rx.icon("panel-left-close", size=18, color="#4a5568"),
                            ),
                            on_click=State.toggle_sidebar,
                            cursor="pointer",
                            padding="0.35em",
                            border_radius="10px",
                            _hover={"background_color": "#edf2f7"},
                        ),
                        rx.cond(
                            State.sidebar_collapsed,
                            rx.fragment(),
                            rx.heading("ABAP AGENT", size="7"),
                        ),
                        align_items="center",
                        width="100%",
                        justify="start",
                        spacing="3",
                    ),
                    rx.cond(
                        State.sidebar_collapsed,
                        rx.fragment(),
                        rx.fragment(
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
                        ),
                    ),
                    width="100%",
                    height="100%",
                    padding=rx.cond(State.sidebar_collapsed, "1.25em 0.75em", "2.25em 1.5em"),
                    align_items="start",
                    overflow="hidden",
                ),
                width=rx.cond(State.sidebar_collapsed, "72px", "360px"),
                height="100%",
                border_right="1px solid #e2e8f0",
                position="sticky",
                top="0",
                align_self="stretch",
                box_sizing="border-box",
                background_color="white",
            ),
            # 오른쪽 메인 모니터
            main_monitor(),
            width="100%",
            spacing="0",
            height="100%",
            overflow="hidden",
        ),
        position="fixed",
        inset="0",
        height="100vh",
        width="100%",
        overflow="hidden",
        box_sizing="border-box",
    )

app = rx.App(theme=rx.theme(appearance="light", accent_color="blue"))
app.add_page(index)