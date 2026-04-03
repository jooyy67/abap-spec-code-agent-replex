import reflex as rx
from .state import State

# --- 1. 공통 디자인 함수 (테두리 없는 Ghost 스타일 유지) ---

def section_title(title: str):
    return rx.heading(
        title, size="5", margin_top="1.5em", color="#2b6cb0", 
        border_bottom="2px solid #e2e8f0", width="100%", padding_bottom="0.3em"
    )

def table_header_cell(label: str):
    return rx.table.column_header_cell(
        label, background_color="#f8f9fa", border="1px solid #dee2e6",
        font_weight="bold", text_align="center", padding_y="0.8em", color="#495057"
    )

def table_body_cell(content):
    return rx.table.cell(content, border="1px solid #dee2e6", padding="0", vertical_align="middle")

def cell_input(value: str, on_change_fn, width="100%"):
    return rx.input(
        value=value, on_change=on_change_fn, variant="soft", width=width,
        height="100%", text_align="center", background_color="transparent",
        border="none", style={"box-shadow": "none"},
        _focus={"background_color": "white", "border": "1px solid #4dabf7"},
    )

def cell_select(options, value, on_change_fn):
    return rx.select(
        options, value=value, on_change=on_change_fn, variant="soft",
        width="100%", background_color="transparent", style={"box-shadow": "none"}
    )

def feature_item(label: str):
    """2번 섹션 체크박스"""
    return rx.checkbox(label, on_change=lambda b: State.update_list("selected_features", label, b))

def auth_item(label: str):
    """1번 섹션 권한 체크박스"""
    return rx.checkbox(label, on_change=lambda b: State.update_auth_range(label, b))

# --- 2. 섹션별 가변 뷰 (오른쪽 모니터 화면용) ---

def view_section_1():
    return rx.vstack(
        rx.text("프로그램 이름", font_weight="bold"),
        rx.input(placeholder="예: 구매 현황 조회", on_change=State.set_prog_name, width="100%"),
        rx.text("요청 부서/자", font_weight="bold"),
        rx.input(placeholder="예: 회계팀 홍길동", on_change=State.set_req_dept_user, width="100%"),
        rx.text("업무 구분", font_weight="bold"),
        rx.select(State.work_options, on_change=State.set_work_category, width="100%"),
        rx.text("사용 권한 범위", font_weight="bold"),
        rx.hstack(auth_item("모든 사용자"), auth_item("특정 부서"), auth_item("특정 플랜트"), spacing="4"),
        spacing="3", width="100%"
    )

def view_section_2():
    return rx.vstack(
        rx.text("메인 유형", font_weight="bold"),
        rx.radio_group(["조회 전용", "저장 전용", "조회 + 저장"], on_change=State.set_prog_type, direction="row", spacing="4"),
        rx.text("상세 기능", font_weight="bold"),
        rx.grid(
            feature_item("행 추가"), feature_item("행 삭제"), feature_item("엑셀 업로드"), feature_item("엑셀 다운로드"),
            feature_item("합계 표시"), feature_item("메일 알림"), columns="2", spacing="2", width="100%"
        ),
        spacing="4", width="100%"
    )

def view_section_3():
    return rx.vstack(
        rx.text("기본 구조", font_weight="bold"),
        rx.radio_group(["단일 화면", "2분할 (위/아래)", "2분할 (좌/우)"], value=State.ui_layout, on_change=State.set_ui_layout),
        rx.cond(
            State.ui_layout.contains("2분할"),
            rx.vstack(
                rx.text("└ 상세 동작 정의", color="#2b6cb0", font_weight="bold"),
                rx.radio_group(["연동형", "병렬형"], on_change=State.set_layout_detail, direction="row", spacing="4"),
                padding_left="1em", border_left="2px solid #cbd5e0"
            ),
            rx.fragment() # 에러 방지를 위해 rx.none() 대신 사용
        ),
        rx.text("편집 권한", font_weight="bold"),
        rx.radio_group(["조회 전용", "수정 가능"], on_change=State.set_edit_auth, direction="row", spacing="4"),
        spacing="4", width="100%"
    )

def view_section_4():
    return rx.vstack(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    table_header_cell("순서"), table_header_cell("항목명"), table_header_cell("필드ID"),
                    table_header_cell("입력방식"), table_header_cell("필수"), table_header_cell("삭제")
                )
            ),
            rx.table.body(
                rx.foreach(State.selection_fields, lambda field, idx: rx.table.row(
                    table_body_cell(cell_input(field.order, lambda v: State.update_field(idx, "order", v))),
                    table_body_cell(cell_input(field.label, lambda v: State.update_field(idx, "label", v))),
                    table_body_cell(cell_input(field.field_id, lambda v: State.update_field(idx, "field_id", v))),
                    table_body_cell(rx.center(cell_select(["단일", "범위", "리스트"], field.input_type, lambda v: State.update_field(idx, "input_type", v)))),
                    table_body_cell(rx.center(rx.checkbox(is_checked=field.is_required, on_change=lambda b: State.update_field(idx, "is_required", b)))),
                    table_body_cell(rx.center(rx.button(rx.icon("trash-2"), color_scheme="red", variant="ghost", on_click=lambda: State.delete_selection_row(idx), size="1")))
                ))
            ), width="100%"
        ),
        rx.button(rx.icon("plus"), "행 추가", on_click=State.add_selection_row, variant="soft"),
        width="100%"
    )

def view_section_5():
    return rx.vstack(
        rx.text("[영역 A: 메인 목록]", font_weight="bold", color="#2b6cb0"),
        rx.table.root(
            rx.table.header(rx.table.row(table_header_cell("항목명"), table_header_cell("필드ID"), table_header_cell("수정"))),
            rx.table.body(
                rx.foreach(State.alv_fields_a, lambda field, idx: rx.table.row(
                    table_body_cell(cell_input(field.label, lambda v: State.update_alv_field("A", idx, "label", v))),
                    table_body_cell(cell_input(field.field_id, lambda v: State.update_alv_field("A", idx, "field_id", v))),
                    table_body_cell(rx.center(rx.checkbox(is_checked=field.is_edit, on_change=lambda b: State.update_alv_field("A", idx, "is_edit", b))))
                ))
            ), width="100%"
        ),
        rx.button(rx.icon("plus"), "행 추가", on_click=lambda: State.add_alv_row("A"), variant="soft"),
        width="100%"
    )

def view_section_6():
    return rx.vstack(
        rx.text("업무 흐름", font_weight="bold"),
        rx.text_area(placeholder="상세 로직 입력...", on_change=State.set_logic_flow, width="100%", height="150px"),
        rx.text("반영 위치", font_weight="bold"),
        rx.hstack(
            rx.checkbox("Z-Table", on_change=lambda b: State.update_data_target("Z-Table", b)),
            rx.checkbox("BAPI", on_change=lambda b: State.update_data_target("BAPI", b)),
            spacing="4"
        ),
        spacing="4", width="100%"
    )