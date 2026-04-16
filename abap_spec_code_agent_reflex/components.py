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
        options,
        value=value,
        on_change=on_change_fn,
        variant="ghost",
        width="100%",
        height="100%",
        text_align="center",
        background_color="transparent",
        border="none",
        style={
            "box-shadow": "none",
            "text-align": "center",
        },
        _focus={"background_color": "white", "border": "1px solid #4dabf7"},
    )

def feature_item(label: str, desc: str | None = None):
    """2번 섹션 체크박스(+ 선택 설명)"""
    children = [
        rx.checkbox(
            label,
            checked=State.selected_features.contains(label),
            on_change=lambda b: State.update_list("selected_features", label, b),
        )
    ]
    if desc:
        children.append(
            rx.text(desc, color="#718096", font_size="0.9em", margin_left="1.85em")
        )

    return rx.vstack(*children, spacing="1", width="100%", align_items="start")

def auth_item(label: str):
    """1번 섹션 권한 체크박스"""
    return rx.checkbox(
        label,
        checked=State.auth_range.contains(label),
        on_change=lambda b: State.update_auth_range(label, b),
    )

# --- 2. 섹션별 가변 뷰 (오른쪽 모니터 화면용) ---

def view_section_1():
    return rx.vstack(
        rx.text("1.1 프로그램 이름", font_weight="bold"),
        rx.input(
            value=State.prog_name,
            placeholder="예: 채권잔액프로그램",
            on_change=State.set_prog_name,
            width="100%",
        ),
        rx.text("1.2 요청 부서/자", font_weight="bold"),
        rx.input(
            value=State.req_dept_user,
            placeholder="예: 회계팀 홍길동",
            on_change=State.set_req_dept_user,
            width="100%",
        ),
        rx.text("1.3 업무 구분", font_weight="bold"),
        rx.select(
            State.work_options,
            value=State.work_category,
            on_change=State.set_work_category,
            width="100%",
        ),
        rx.text("1.4 참조 T-Code", font_weight="bold"),
        rx.input(
            value=State.ref_tcode,
            placeholder="예: MM03, VA05",
            on_change=State.set_ref_tcode,
            width="100%",
        ),
        rx.text("1.5 사용 권한 범위", font_weight="bold"),
        rx.vstack(
            auth_item("모든 사용자"),
            auth_item("특정 부서만"),
            auth_item("특정 사업장만"),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        spacing="3",
        width="100%",
        align_items="start",
    )

def view_section_2():
    def prog_type_option(value: str, label: str, desc: str):
        is_selected = State.prog_type == value
        return rx.box(
            rx.hstack(
                rx.box(
                    width="16px",
                    height="16px",
                    border_radius="4px",
                    border=rx.cond(is_selected, "5px solid #2b6cb0", "2px solid #a0aec0"),
                    background_color="white",
                    flex_shrink="0",
                    margin_top="0.2em",
                ),
                rx.vstack(
                    rx.text(label, font_weight="600"),
                    rx.text(desc, color="#718096"),
                    spacing="1",
                    align_items="start",
                ),
                spacing="3",
                align_items="start",
                width="100%",
            ),
            width="100%",
            padding="0.75em 0.9em",
            border_radius="12px",
            border=rx.cond(is_selected, "1px solid #90cdf4", "1px solid #e2e8f0"),
            background_color=rx.cond(is_selected, "#ebf8ff", "transparent"),
            cursor="pointer",
            on_click=lambda: State.set_prog_type(value),
        )

    return rx.vstack(
        rx.text("2.1 기본 유형 (필수 - 1개만 선택)", font_weight="bold"),
        rx.vstack(
            # NOTE: 내부 로직은 기존 State.prog_type 값을 그대로 사용 (로직 변경 없음)
            prog_type_option("조회 전용", "조회형", "데이터 확인 중심 (3.4-A 작성 / 3.4-B 작성 안 함)"),
            prog_type_option("조회 + 저장", "CRUD형", "입력/수정/삭제 포함 (3.4-B 필수 작성)"),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        rx.divider(margin_y="0.75em"),
        rx.text("2.2 조회 조건 설정", font_weight="bold"),
        rx.vstack(
            feature_item("사용", "필터 입력창 생성 (4번 섹션 작성)"),
            feature_item("미사용", "실행 시 즉시 조회 (4번 섹션 건너뜀)"),
            rx.cond(
                State.prog_type != "조회 전용",
                rx.vstack(
                    feature_item("양식 다운로드", "업로드 템플릿 버튼 생성"),
                    spacing="2",
                    width="100%",
                    align_items="start",
                ),
                rx.fragment(),
            ),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        spacing="4",
        width="100%",
        align_items="start",
    )

def view_section_3():
    is_crud = State.prog_type != "조회 전용"
    is_multi = State.grid_count == "다중 Grid"
    has_create = State.detail_b_scope.contains("신규 추가")

    return rx.vstack(
        rx.text("3.1 Grid 개수 (필수 - 1개만 선택)", font_weight="bold"),
        rx.radio_group(
            ["단일 Grid", "다중 Grid"],
            value=State.grid_count,
            on_change=State.set_grid_count,
            direction="row",
            spacing="4",
        ),
        rx.text("분할 방식:", font_weight="bold"),
        rx.radio_group(
            ["상하", "좌우", "탭"],
            value=State.split_mode,
            on_change=State.set_split_mode,
            direction="row",
            spacing="4",
        ),
        rx.divider(margin_y="0.75em"),
        rx.text("3.2 클릭 시 동작 (중복 가능)", font_weight="bold"),
        rx.vstack(
            rx.checkbox(
                "없음",
                on_change=lambda b: State.update_list("click_actions", "없음", b),
            ),
            rx.checkbox(
                "화면 이동",
                on_change=lambda b: State.update_list("click_actions", "화면 이동", b),
            ),
            rx.checkbox(
                "팝업",
                on_change=lambda b: State.update_list("click_actions", "팝업", b),
            ),
            rx.cond(
                is_multi,
                rx.vstack(
                    rx.checkbox(
                        "내부연동 (Drill-Down)",
                        on_change=lambda b: State.update_list("click_actions", "내부연동 (Drill-Down)", b),
                    ),
                    spacing="1",
                    width="100%",
                    align_items="start",
                ),
                rx.fragment(),
            ),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        rx.divider(margin_y="0.75em"),
        rx.text("3.3 실행 방식", font_weight="bold"),
        rx.vstack(
            rx.checkbox("Hotspot (필드 클릭)", on_change=lambda b: State.update_list("exec_methods", "Hotspot", b)),
            rx.checkbox("Double Click (행 클릭)", on_change=lambda b: State.update_list("exec_methods", "Double Click", b)),
            rx.checkbox("버튼", on_change=lambda b: State.update_list("exec_methods", "버튼", b)),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        rx.divider(margin_y="0.75em"),
        rx.text("3.4 상세 기능 (유형별 필수 작성)", font_weight="bold", color="#2b6cb0"),
        rx.cond(
            is_crud,
            rx.vstack(
                rx.text("3.4-B [CRUD형 전용]", font_weight="bold"),
                rx.text("3.4-B-1. 처리 범위", font_weight="bold"),
                rx.vstack(
                    rx.checkbox(
                        "신규 추가",
                        checked=State.detail_b_scope.contains("신규 추가"),
                        on_change=lambda b: State.toggle_detail_b_scope("신규 추가", b),
                    ),
                    rx.checkbox(
                        "수정 가능",
                        checked=State.detail_b_scope.contains("수정 가능"),
                        on_change=lambda b: State.toggle_detail_b_scope("수정 가능", b),
                    ),
                    rx.checkbox(
                        "삭제 가능",
                        checked=State.detail_b_scope.contains("삭제 가능"),
                        on_change=lambda b: State.toggle_detail_b_scope("삭제 가능", b),
                    ),
                    spacing="2",
                    width="100%",
                    align_items="start",
                ),
                rx.divider(margin_y="0.5em"),
                rx.cond(
                    has_create,
                    rx.vstack(
                        rx.text("3.4-B-2. 입력 방식", font_weight="bold"),
                        rx.checkbox("엑셀 업로드", on_change=lambda b: State.update_list("detail_b_input_methods", "엑셀 업로드", b)),
                        rx.checkbox("직접 입력", on_change=lambda b: State.update_list("detail_b_input_methods", "직접 입력", b)),
                        rx.checkbox("팝업", on_change=lambda b: State.update_list("detail_b_input_methods", "팝업", b)),
                        rx.checkbox("화면이동", on_change=lambda b: State.update_list("detail_b_input_methods", "화면이동", b)),
                        spacing="2",
                        width="100%",
                        align_items="start",
                    ),
                    rx.fragment(),
                ),
                rx.divider(margin_y="0.5em"),
                rx.text("3.4-B-3. Grid 제어 (3.1 선택에 따라 작성)", font_weight="bold"),
                rx.cond(
                    is_multi,
                    rx.vstack(
                        rx.text("상단 Grid", font_weight="bold"),
                        rx.vstack(
                            rx.checkbox("조회 전용", on_change=lambda b: State.update_list("detail_b_multi_top", "조회 전용", b)),
                            rx.checkbox("편집 가능(추가/삭제/모드전환)", on_change=lambda b: State.update_list("detail_b_multi_top", "편집 가능(추가/삭제/모드전환)", b)),
                            spacing="2",
                            width="100%",
                            align_items="start",
                        ),
                        rx.text("하단 Grid", font_weight="bold", margin_top="0.25em"),
                        rx.vstack(
                            rx.checkbox("조회 전용", on_change=lambda b: State.update_list("detail_b_multi_bottom", "조회 전용", b)),
                            rx.checkbox(
                                "편집 가능(추가/삭제/모드전환/다건처리)",
                                on_change=lambda b: State.update_list("detail_b_multi_bottom", "편집 가능(추가/삭제/모드전환/다건처리)", b),
                            ),
                            spacing="2",
                            width="100%",
                            align_items="start",
                        ),
                        spacing="2",
                        width="100%",
                        align_items="start",
                    ),
                    rx.vstack(
                        rx.vstack(
                            rx.checkbox("행 추가", on_change=lambda b: State.update_list("detail_b_single_grid_controls", "행 추가", b)),
                            rx.checkbox("행 삭제", on_change=lambda b: State.update_list("detail_b_single_grid_controls", "행 삭제", b)),
                            rx.checkbox("모드 전환", on_change=lambda b: State.update_list("detail_b_single_grid_controls", "모드 전환", b)),
                            rx.checkbox("다건 처리", on_change=lambda b: State.update_list("detail_b_single_grid_controls", "다건 처리", b)),
                            spacing="2",
                            width="100%",
                            align_items="start",
                        ),
                        spacing="2",
                        width="100%",
                        align_items="start",
                    ),
                ),
                spacing="3",
                width="100%",
                align_items="start",
            ),
            rx.vstack(
                rx.text("3.4-A [조회형 전용]", font_weight="bold"),
                rx.vstack(
                    rx.checkbox("단순 조회", on_change=lambda b: State.update_list("detail_a", "단순 조회", b)),
                    rx.checkbox("상세 조회 사용", on_change=lambda b: State.update_list("detail_a", "상세 조회 사용", b)),
                    spacing="2",
                    width="100%",
                    align_items="start",
                ),
                spacing="2",
                width="100%",
                align_items="start",
            ),
        ),
        spacing="4",
        width="100%",
        align_items="start",
    )

def view_section_4():
    return rx.vstack(
        rx.text("조회 시 입력받는 조건 정의", color="#718096"),
        rx.text("섹션: 비슷한 항목끼리 박스로 묶음 (예: [기본 정보])", color="#718096"),
        rx.text("입력방식:", font_weight="bold"),
        rx.unordered_list(
            rx.list_item(rx.text("단일: 값 1개 입력")),
            rx.list_item(rx.text("범위: 시작~종료")),
            rx.list_item(rx.text("라디오: 선택형")),
            rx.list_item(rx.text("리스트: 드롭다운")),
            rx.list_item(rx.text("체크박스: Y/N")),
            spacing="1",
            padding_left="1.2em",
            color="#4a5568",
        ),
        rx.text("화면제어규칙: 특정 상황에서 칸을 잠그거나 숨겨야 할 내용", color="#718096"),
        rx.divider(margin_y="0.75em"),
        rx.text("자동 입력 (추가 기능)", font_weight="bold", color="#2b6cb0"),
        rx.text("엑셀 업로드로 아래 테이블을 자동 채울 수 있습니다. 업로드 후에도 직접 수정 가능합니다.", color="#718096"),
        rx.hstack(
            rx.button(
                "조회조건 업로드 템플릿 다운로드",
                on_click=rx.download(url="/templates/selection_template.xlsx", filename="조회조건_업로드_템플릿.xlsx"),
                variant="soft",
            ),
            rx.text("(.xlsx)", color="#718096"),
            spacing="2",
            width="100%",
            align_items="center",
            flex_wrap="wrap",
        ),
        rx.hstack(
            rx.upload(
                rx.button("엑셀 선택", variant="soft"),
                id="excel_upload",
                accept={"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"]},
                multiple=False,
                border="none",
                padding="0",
                background_color="transparent",
                width="auto",
                height="auto",
                style={
                    "border": "none",
                    "outline": "none",
                    "boxShadow": "none",
                    "display": "inline-flex",
                },
            ),
            rx.button(
                "업로드 후 자동 반영",
                on_click=State.handle_excel_upload_selection(rx.upload_files(upload_id="excel_upload")),
                color_scheme="blue",
                variant="solid",
            ),
            rx.button(
                "선택 취소",
                on_click=[
                    rx.clear_selected_files("excel_upload"),
                    State.clear_selection_upload_and_table,
                ],
                variant="ghost",
            ),
            spacing="3",
            width="100%",
            align_items="center",
            flex_wrap="wrap",
        ),
        rx.cond(
            rx.selected_files("excel_upload").length() > 0,
            rx.text(
                rx.selected_files("excel_upload")[0],
                color="#718096",
                font_size="0.9em",
                width="100%",
                overflow="hidden",
                text_overflow="ellipsis",
                white_space="nowrap",
            ),
            rx.fragment(),
        ),
        rx.cond(
            State.selection_upload_error != "",
            rx.text(State.selection_upload_error, color="#c53030", white_space="pre-wrap"),
            rx.fragment(),
        ),
        rx.cond(
            State.selection_upload_info != "",
            rx.text(State.selection_upload_info, color="#2f855a", white_space="pre-wrap"),
            rx.fragment(),
        ),
        rx.cond(
            State.selection_upload_debug != "",
            rx.hstack(
                rx.checkbox(
                    "디버그 보기",
                    checked=State.show_selection_upload_debug,
                    on_change=State.set_show_selection_upload_debug,
                ),
                rx.spacer(),
                width="100%",
                align_items="center",
            ),
            rx.fragment(),
        ),
        rx.cond(
            (State.selection_upload_debug != "") & State.show_selection_upload_debug,
            rx.box(
                rx.text("업로드 파싱 디버그 (상위 3행)", font_weight="bold", color="#4a5568"),
                rx.code_block(State.selection_upload_debug, width="100%"),
                width="100%",
                padding="0.75em",
                border="1px solid #e2e8f0",
                background_color="#f8fafc",
                border_radius="12px",
            ),
            rx.fragment(),
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    table_header_cell("순서"),
                    table_header_cell("섹션명"),
                    table_header_cell("항목명"),
                    table_header_cell("필드ID"),
                    table_header_cell("입력방식"),
                    table_header_cell("필수"),
                    table_header_cell("F4"),
                    table_header_cell("화면 제어 규칙"),
                    table_header_cell("삭제"),
                )
            ),
            rx.table.body(
                rx.foreach(State.selection_fields, lambda field, idx: rx.table.row(
                    table_body_cell(cell_input(field.order, lambda v: State.update_field(idx, "order", v))),
                    table_body_cell(cell_input(field.section, lambda v: State.update_field(idx, "section", v))),
                    table_body_cell(cell_input(field.label, lambda v: State.update_field(idx, "label", v))),
                    table_body_cell(cell_input(field.field_id, lambda v: State.update_field(idx, "field_id", v))),
                    table_body_cell(
                        rx.center(
                            cell_select(
                                ["단일", "범위", "라디오", "리스트", "체크박스"],
                                field.input_type,
                                lambda v: State.update_field(idx, "input_type", v),
                            )
                        )
                    ),
                    table_body_cell(rx.center(rx.checkbox(checked=field.is_required, on_change=lambda b: State.update_field(idx, "is_required", b)))),
                    table_body_cell(rx.center(rx.checkbox(checked=field.has_f4, on_change=lambda b: State.update_field(idx, "has_f4", b)))),
                    table_body_cell(cell_input(field.ui_rule, lambda v: State.update_field(idx, "ui_rule", v))),
                    table_body_cell(
                        rx.center(
                            rx.button(
                                rx.icon("trash-2"),
                                color_scheme="red",
                                variant="ghost",
                                on_click=lambda: State.delete_selection_row(idx),
                                size="1",
                            )
                        )
                    ),
                ))
            ), width="100%"
        ),
        rx.button(rx.icon("plus"), "행 추가", on_click=State.add_selection_row, variant="soft"),
        width="100%"
    )

def view_section_5():
    def alv_pick_summary(area: str):
        # 업로드된 모든 테이블에서 체크한 행을 합산하여 표시
        pick_data = State.alv_picked_preview_all_a if area == "A" else State.alv_picked_preview_all_b
        return rx.vstack(
            rx.text(f"선택한 필드 요약 (영역 {area})", font_weight="bold", color="#4a5568", margin_top="0.85em"),
            rx.cond(
                pick_data.length() > 0,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            table_header_cell("테이블"),
                            table_header_cell("순서"),
                            table_header_cell("항목명"),
                            table_header_cell("필드ID"),
                            table_header_cell("중요키(K)"),
                            table_header_cell("합계"),
                            table_header_cell("수정"),
                            table_header_cell("동작"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            pick_data,
                            lambda field, idx: rx.table.row(
                                table_body_cell(rx.text(field.table_label, white_space="pre-wrap")),
                                table_body_cell(rx.text(field.order, text_align="center")),
                                table_body_cell(rx.text(field.label, white_space="pre-wrap")),
                                table_body_cell(rx.text(field.field_id, text_align="center")),
                                table_body_cell(rx.center(rx.text(rx.cond(field.is_key, "Y", "")))),
                                table_body_cell(rx.center(rx.text(rx.cond(field.is_sum, "Y", "")))),
                                table_body_cell(rx.center(rx.text(rx.cond(field.is_edit, "Y", "")))),
                                table_body_cell(rx.text(field.action, white_space="pre-wrap")),
                                key=field.table_label + "-" + idx.to_string() + "-" + field.field_id,
                            ),
                        )
                    ),
                    width="100%",
                    border="1px solid #e2e8f0",
                    border_radius="10px",
                    overflow="hidden",
                ),
                rx.text("왼쪽 체크박스로 요약에 넣을 행을 선택하세요.", color="#a0aec0", font_size="0.9em"),
            ),
            spacing="1",
            width="100%",
            align_items="start",
        )

    def alv_table(area: str, title: str, data):
        pick_key = "preview_pick_a" if area == "A" else "preview_pick_b"
        bind_id = State.area_bind_id_a if area == "A" else State.area_bind_id_b
        return rx.vstack(
            rx.text(title, font_weight="bold", color="#2b6cb0"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        table_header_cell("선택"),
                        table_header_cell("순서"),
                        table_header_cell("항목명"),
                        table_header_cell("필드ID"),
                        table_header_cell("중요키(K)"),
                        table_header_cell("합계"),
                        table_header_cell("수정"),
                        table_header_cell("동작"),
                        table_header_cell("삭제"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        data,
                        lambda field, idx: rx.table.row(
                            table_body_cell(
                                rx.center(
                                    rx.checkbox(
                                        checked=rx.cond(area == "A", field.preview_pick_a, field.preview_pick_b),
                                        on_change=lambda b: State.update_alv_field(area, idx, pick_key, b),
                                    )
                                )
                            ),
                            table_body_cell(
                                cell_input(field.order, lambda v: State.update_alv_field(area, idx, "order", v))
                            ),
                            table_body_cell(
                                cell_input(field.label, lambda v: State.update_alv_field(area, idx, "label", v))
                            ),
                            table_body_cell(
                                cell_input(field.field_id, lambda v: State.update_alv_field(area, idx, "field_id", v))
                            ),
                            table_body_cell(
                                rx.center(
                                    rx.checkbox(
                                        checked=field.is_key,
                                        on_change=lambda b: State.update_alv_field(area, idx, "is_key", b),
                                    )
                                )
                            ),
                            table_body_cell(
                                rx.center(
                                    rx.checkbox(
                                        checked=field.is_sum,
                                        on_change=lambda b: State.update_alv_field(area, idx, "is_sum", b),
                                    )
                                )
                            ),
                            table_body_cell(
                                rx.center(
                                    rx.checkbox(
                                        checked=field.is_edit,
                                        on_change=lambda b: State.update_alv_field(area, idx, "is_edit", b),
                                    )
                                )
                            ),
                            table_body_cell(
                                cell_input(field.action, lambda v: State.update_alv_field(area, idx, "action", v))
                            ),
                            table_body_cell(
                                rx.center(
                                    rx.button(
                                        rx.icon("trash-2"),
                                        color_scheme="red",
                                        variant="ghost",
                                        on_click=lambda: State.delete_alv_row(area, idx),
                                        size="1",
                                    )
                                )
                            ),
                            key=bind_id + "-" + idx.to_string() + "-" + field.field_id,
                        ),
                    )
                ),
                width="100%",
            ),
            rx.button(rx.icon("plus"), "행 추가", on_click=lambda: State.add_alv_row(area), variant="soft"),
            spacing="3",
            width="100%",
            align_items="start",
        )

    return rx.vstack(
        rx.text("화면에 표시될 데이터 정의", color="#718096"),
        rx.text("화면 영역(상단/하단/팝업)별로 구분하여 작성", color="#718096"),
        rx.unordered_list(
            rx.list_item(rx.text("중요키: 데이터의 기준이 되는 번호 (예: 전표번호)")),
            rx.list_item(rx.text("시각효과: 색상, 아이콘")),
            rx.list_item(rx.text("동작: 더블클릭, 값 변경 시 이벤트 등")),
            spacing="1",
            padding_left="1.2em",
            color="#4a5568",
        ),
        rx.divider(margin_y="0.75em"),
        rx.text("자동 입력 (추가 기능)", font_weight="bold", color="#2b6cb0"),
        rx.text("엑셀 업로드로 ALV 테이블을 자동 채울 수 있습니다. (기본: 영역 A, area 컬럼으로 A/B 분리 가능)", color="#718096"),
        rx.hstack(
            rx.button(
                "ALV 업로드 템플릿 다운로드",
                on_click=rx.download(url="/templates/alv_template.xlsx", filename="ALV_업로드_템플릿.xlsx"),
                variant="soft",
            ),
            rx.text("(.xlsx)", color="#718096"),
            spacing="2",
            width="100%",
            align_items="center",
            flex_wrap="wrap",
        ),
        rx.hstack(
            rx.upload(
                rx.button("엑셀 선택", variant="soft"),
                id="excel_upload_alv",
                accept={"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"]},
                multiple=False,
                border="none",
                padding="0",
                background_color="transparent",
                width="auto",
                height="auto",
                style={
                    "border": "none",
                    "outline": "none",
                    "boxShadow": "none",
                    "display": "inline-flex",
                },
            ),
            rx.button(
                "업로드 후 자동 반영",
                on_click=State.handle_excel_upload_alv(rx.upload_files(upload_id="excel_upload_alv")),
                color_scheme="blue",
                variant="solid",
            ),
            rx.button(
                "선택 취소",
                on_click=[
                    rx.clear_selected_files("excel_upload_alv"),
                    State.clear_alv_upload_and_tables,
                ],
                variant="ghost",
            ),
            spacing="3",
            width="100%",
            align_items="center",
            flex_wrap="wrap",
        ),
        rx.cond(
            rx.selected_files("excel_upload_alv").length() > 0,
            rx.text(
                rx.selected_files("excel_upload_alv")[0],
                color="#718096",
                font_size="0.9em",
                width="100%",
                overflow="hidden",
                text_overflow="ellipsis",
                white_space="nowrap",
            ),
            rx.fragment(),
        ),
        rx.text(
            "SE11 캡처는 「이미지 1장 = 추출 테이블 1개」이며 결과는 합치지 않습니다. 클립보드 붙여넣기만 지원합니다.",
            color="#718096",
        ),
        rx.clipboard(
            rx.box(
                rx.text(
                    "아래 영역을 클릭한 뒤 Ctrl+V로 캡처를 붙여넣고, 「테이블 생성」으로 추출하세요.",
                    font_weight="500",
                    color="#4a5568",
                    margin_bottom="0.5em",
                ),
                rx.cond(
                    State.se11_paste_queue_uris.length() > 0,
                    rx.hstack(
                        rx.foreach(
                            State.se11_paste_queue_uris,
                            lambda uri, idx: rx.box(
                                rx.image(
                                    src=uri,
                                    max_height="160px",
                                    width="auto",
                                    border_radius="10px",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.button(
                                    rx.icon("x", size=16),
                                    size="1",
                                    variant="solid",
                                    color_scheme="red",
                                    on_click=lambda: State.remove_se11_paste_queue_item(idx),
                                    style={"position": "absolute", "top": "6px", "right": "6px"},
                                ),
                                style={"position": "relative", "display": "inline-block"},
                                key=idx,
                            ),
                        ),
                        spacing="3",
                        flex_wrap="wrap",
                        width="100%",
                        align_items="start",
                    ),
                    rx.text("붙여넣은 이미지 미리보기가 여기에 표시됩니다.", color="#a0aec0", font_size="0.9em"),
                ),
                padding="1em",
                border="2px dashed #cbd5e0",
                border_radius="12px",
                width="100%",
                background_color="#fafafa",
                tab_index=0,
                _focus_within={"border_color": "#3182ce", "background_color": "#f7fafc"},
            ),
            on_paste=State.on_se11_image_paste.stop_propagation,
        ),
        rx.text("생성된 업로드 테이블 목록", font_weight="bold", color="#2b6cb0", margin_top="0.5em"),
        rx.text("추출 후 아래에서 항목을 확인하고, 영역 A/B 드롭다운에서 바인딩하세요.", color="#718096", font_size="0.85em"),
        rx.cond(
            State.uploaded_alv_tables.length() > 0,
            rx.vstack(
                rx.foreach(
                    State.uploaded_alv_tables,
                    lambda t: rx.hstack(
                        rx.badge(t.label, color_scheme="blue", variant="soft"),
                        rx.text(" 필드 목록 추출됨", color="#718096", font_size="0.9em"),
                        rx.spacer(),
                        rx.button(
                            rx.icon("trash-2", size=16),
                            size="1",
                            variant="ghost",
                            color_scheme="red",
                            on_click=lambda: State.delete_uploaded_alv_table(t.id),
                        ),
                        spacing="2",
                        align_items="center",
                        width="100%",
                    ),
                ),
                spacing="2",
                width="100%",
                padding="0.75em",
                border="1px solid #e2e8f0",
                border_radius="12px",
                background_color="#f8fafc",
            ),
            rx.fragment(),
        ),
        rx.hstack(
            rx.button(
                "테이블 생성",
                on_click=State.handle_se11_create_tables,
                color_scheme="blue",
                variant="solid",
            ),
            rx.button(
                "바인딩 초기화",
                on_click=State.reset_se11_tables_and_bindings,
                variant="ghost",
            ),
            spacing="3",
            width="100%",
            align_items="center",
            flex_wrap="wrap",
        ),
        rx.cond(
            (State.alv_upload_error != "") | (State.image_upload_error != ""),
            rx.vstack(
                rx.cond(State.alv_upload_error != "", rx.text(State.alv_upload_error, color="#c53030", white_space="pre-wrap"), rx.fragment()),
                rx.cond(State.image_upload_error != "", rx.text(State.image_upload_error, color="#c53030", white_space="pre-wrap"), rx.fragment()),
                spacing="1",
                width="100%",
            ),
            rx.fragment(),
        ),
        rx.cond(
            (State.alv_upload_info != "") | (State.image_upload_info != ""),
            rx.vstack(
                rx.cond(State.alv_upload_info != "", rx.text(State.alv_upload_info, color="#2f855a", white_space="pre-wrap"), rx.fragment()),
                rx.cond(State.image_upload_info != "", rx.text(State.image_upload_info, color="#2f855a", white_space="pre-wrap"), rx.fragment()),
                spacing="1",
                width="100%",
            ),
            rx.fragment(),
        ),
        rx.cond(
            State.alv_upload_debug != "",
            rx.hstack(
                rx.checkbox(
                    "디버그 보기",
                    checked=State.show_alv_upload_debug,
                    on_change=State.set_show_alv_upload_debug,
                ),
                rx.spacer(),
                width="100%",
                align_items="center",
            ),
            rx.fragment(),
        ),
        rx.cond(
            (State.alv_upload_debug != "") & State.show_alv_upload_debug,
            rx.box(
                rx.text("업로드 파싱 디버그 (상위 3행)", font_weight="bold", color="#4a5568"),
                rx.code_block(State.alv_upload_debug, width="100%"),
                width="100%",
                padding="0.75em",
                border="1px solid #e2e8f0",
                background_color="#f8fafc",
                border_radius="12px",
            ),
            rx.fragment(),
        ),
        rx.divider(margin_y="0.75em"),
        rx.text("영역 바인딩", font_weight="bold", color="#2b6cb0"),
        rx.text(
            "업로드 테이블 목록에서 영역 A·B에 반영할 표를 각각 선택합니다. 선택을 바꾸면 해당 영역 표가 즉시 갱신됩니다.",
            color="#718096",
            font_size="0.85em",
        ),
        rx.vstack(
            rx.text("[영역 A: 메인 목록]", font_weight="bold", color="#2b6cb0"),
            rx.hstack(
                rx.text("바인딩", font_weight="500", color="#4a5568"),
                rx.select(
                    State.se11_select_options,
                    value=State.area_bind_value_a,
                    on_change=State.set_area_bind_a,
                    width="100%",
                    max_width="440px",
                ),
                spacing="3",
                width="100%",
                align_items="center",
                flex_wrap="wrap",
            ),
            alv_table("A", "선택된 테이블 (영역 A)", State.alv_fields_a),
            alv_pick_summary("A"),
            spacing="3",
            width="100%",
            align_items="start",
        ),
        rx.divider(margin_y="0.75em"),
        rx.vstack(
            rx.text("[영역 B: 상세 / 팝업 / 탭]", font_weight="bold", color="#2b6cb0"),
            rx.hstack(
                rx.text("바인딩", font_weight="500", color="#4a5568"),
                rx.select(
                    State.se11_select_options,
                    value=State.area_bind_value_b,
                    on_change=State.set_area_bind_b,
                    width="100%",
                    max_width="440px",
                ),
                spacing="3",
                width="100%",
                align_items="center",
                flex_wrap="wrap",
            ),
            alv_table("B", "선택된 테이블 (영역 B)", State.alv_fields_b),
            alv_pick_summary("B"),
            spacing="3",
            width="100%",
            align_items="start",
        ),
        spacing="4",
        width="100%",
        align_items="start",
    )

def view_section_6():
    return rx.vstack(
        rx.text("업무 흐름 (자유 기술)", font_weight="bold"),
        rx.text(
            "예: 회사코드·전기일 등으로 전표 조회, 선택한 데이터만 저장, 전표 클릭 시 상세 조회, 수량 변경 시 금액 자동 계산",
            color="#718096",
            font_size="0.85em",
        ),
        rx.text_area(
            value=State.logic_flow,
            placeholder="업무 단계·분기·화면 전환 등을 자유롭게 기술합니다.",
            on_change=State.set_logic_flow,
            width="100%",
            height="140px",
        ),
        rx.text("공통 체크 (Validation)", font_weight="bold"),
        rx.text('예: "수량 0이면 저장 불가"', color="#718096", font_size="0.85em"),
        rx.text_area(
            value=State.validation_rule,
            placeholder="저장/변경 전 공통 검증 규칙을 적습니다.",
            on_change=State.set_validation_rule,
            width="100%",
            height="88px",
        ),
        rx.text("자동 계산 / 변경", font_weight="bold"),
        rx.text('예: 수량 변경 시 금액 자동 계산', color="#718096", font_size="0.85em"),
        rx.text_area(
            value=State.auto_calc_rule,
            placeholder="자동 계산·연동 필드·디폴트값 등을 적습니다.",
            on_change=State.set_auto_calc_rule,
            width="100%",
            height="88px",
        ),
        rx.text("데이터 처리 기준", font_weight="bold", color="#2b6cb0", margin_top="0.25em"),
        rx.text("반영 위치", font_weight="bold"),
        rx.hstack(
            rx.checkbox(
                "Z-Table 저장",
                checked=State.data_target.contains("Z-Table 저장"),
                on_change=lambda b: State.update_data_target("Z-Table 저장", b),
            ),
            rx.checkbox(
                "SAP 표준 문서",
                checked=State.data_target.contains("SAP 표준 문서"),
                on_change=lambda b: State.update_data_target("SAP 표준 문서", b),
            ),
            rx.checkbox(
                "파일 생성",
                checked=State.data_target.contains("파일 생성"),
                on_change=lambda b: State.update_data_target("파일 생성", b),
            ),
            spacing="4",
            flex_wrap="wrap",
            width="100%",
        ),
        rx.text("삭제 방식", font_weight="bold"),
        rx.select(
            ["미지정", "완전 삭제", "삭제 마킹"],
            value=State.delete_method,
            on_change=State.set_delete_method,
            width="100%",
            max_width="320px",
        ),
        rx.text("중복 체크", font_weight="bold"),
        rx.select(
            ["미지정", "필요", "불필요"],
            value=State.dup_check,
            on_change=State.set_dup_check,
            width="100%",
            max_width="320px",
        ),
        spacing="3",
        width="100%",
        align_items="start",
    )


def _placeholder(title: str):
    return rx.vstack(
        rx.text(f"{title} (준비중)", font_weight="bold"),
        rx.text("이 섹션은 사이드바 구조만 먼저 연결해두었습니다.", color="#718096"),
        spacing="2",
        width="100%",
        align_items="start",
    )


def view_fs_section_1():
    # 뷰포트에 맞춰 좌/우 패널이 꽉 차도록 (헤더/패딩/여백 고려)
    panel_height = "calc(100vh - 220px)"
    mapping_sections = [
        "프로그램 기본 정보",
        "Include 구성",
        "기능 매핑",
        "FORM 정의",
        "조회 DB 매핑",
        "저장 DB 매핑",
        "ALV 매핑",
        "이벤트 매핑",
        "저장 흐름",
        "메시지",
    ]

    def mapping_editor():
        return rx.box(
            rx.hstack(
                rx.text(
                    "2. 개발 매핑 입력서 (편집 가능)",
                    font_weight="bold",
                    style={"overflow": "hidden", "textOverflow": "ellipsis", "whiteSpace": "nowrap"},
                ),
                rx.spacer(),
                rx.button(
                    "원본 입력값 수정 (TBD 보완)",
                    variant="soft",
                    on_click=State.open_edit_modal,
                    size="2",
                    style={"flexShrink": "0"},
                ),
                rx.button(
                    "FS 기준으로 매핑 재생성",
                    variant="solid",
                    color_scheme="blue",
                    on_click=State.generate_mapping_sections,
                    size="2",
                    style={"flexShrink": "0"},
                ),
                spacing="1",
                width="100%",
                align_items="center",
                flex_wrap="nowrap",
                overflow="hidden",
            ),
            rx.cond(
                State.mapping_error != "",
                rx.box(
                    rx.text(State.mapping_error, color="#c53030", white_space="pre-wrap"),
                    width="100%",
                    padding="0.75em",
                    border="1px solid #fed7d7",
                    background_color="#fff5f5",
                    border_radius="12px",
                ),
                rx.fragment(),
            ),
            rx.cond(
                State.mapping_updated_at != "",
                rx.text(f"마지막 업데이트: {State.mapping_updated_at}", color="#718096", font_size="0.85em"),
                rx.fragment(),
            ),
            rx.cond(
                (State.generated_fs == "") | (State.mapping_sections.length() == 0),
                rx.box(
                    rx.text(
                        "아직 생성된 개발 매핑 입력서가 없습니다. FS 생성 후 자동 생성되며, FS를 바탕으로 `FS_Mapping_Spec.md` 템플릿 구조에 맞춰 채워집니다.",
                        color="#718096",
                        white_space="pre-wrap",
                    ),
                    width="100%",
                    padding="1em",
                    border="1px solid #e2e8f0",
                    background_color="#f8fafc",
                    border_radius="12px",
                ),
                rx.scroll_area(
                    rx.vstack(
                        rx.foreach(
                            mapping_sections,
                            lambda sec, idx: rx.box(
                                # 헤더 라인에 버튼을 고정 배치(작은 화면에서도 항상 보이게)
                                rx.hstack(
                                    rx.heading(
                                        (idx + 1).to_string() + ". " + sec,
                                        size="4",
                                        color="#2b6cb0",
                                    ),
                                    rx.spacer(),
                                    rx.cond(
                                        State.mapping_edit_section == sec,
                                        rx.button(
                                            "완료",
                                            variant="soft",
                                            on_click=lambda: State.set_mapping_edit_section(""),
                                            style={"flexShrink": "0"},
                                        ),
                                        rx.button(
                                            "수정",
                                            variant="soft",
                                            on_click=lambda: State.set_mapping_edit_section(sec),
                                            style={"flexShrink": "0"},
                                        ),
                                    ),
                                    width="100%",
                                    align_items="center",
                                    flex_wrap="wrap",
                                ),
                                rx.divider(margin_y="0.5em"),
                                rx.cond(
                                    State.mapping_edit_section == sec,
                                    rx.box(
                                        rx.text_area(
                                            value=State.mapping_sections[sec],
                                            on_change=lambda v: State.update_mapping_section(sec, v),
                                            width="100%",
                                            height="360px",
                                        ),
                                        width="100%",
                                        style={"overflowX": "auto"},
                                    ),
                                    rx.box(
                                        rx.markdown(
                                            State.mapping_sections[sec],
                                            width="100%",
                                            style={"fontSize": "0.92em"},
                                        ),
                                        width="100%",
                                        class_name="md-scroll md-render",
                                        style={"overflowX": "auto", "maxWidth": "100%"},
                                    ),
                                ),
                                width="100%",
                                padding="0.9em",
                                border="1px solid #e2e8f0",
                                border_radius="12px",
                                background_color="white",
                                key=sec,
                                style={"minWidth": "0"},
                            ),
                        ),
                        spacing="3",
                        width="100%",
                        align_items="start",
                    ),
                    type="always",
                    scrollbars="vertical",
                    style={"flex": "1", "minHeight": "0", "width": "100%"},
                ),
            ),
            # Edit modal
            rx.dialog.root(
                rx.dialog.content(
                    rx.dialog.title("원본 입력값 수정"),
                    rx.dialog.description(
                        "이 값은 원본 데이터(Single Source of Truth)이며, 저장하면 FS/매핑이 재생성됩니다.",
                        color="#718096",
                    ),
                    rx.vstack(
                        rx.text("수정 대상", font_weight="bold"),
                        rx.select(
                            [
                                "prog_name",
                                "req_dept_user",
                                "work_category",
                                "ref_tcode",
                                "prog_type",
                                "ui_layout",
                                "layout_detail",
                                "edit_auth",
                                "other_ui_notes",
                                "logic_flow",
                                "validation_rule",
                                "auto_calc_rule",
                                "delete_method",
                                "dup_check",
                            ],
                            value=State.edit_field_key,
                            on_change=State.set_edit_field_key,
                            width="100%",
                        ),
                        rx.text("값", font_weight="bold"),
                        rx.cond(
                            (
                                (State.edit_field_key == "other_ui_notes")
                                | (State.edit_field_key == "logic_flow")
                                | (State.edit_field_key == "validation_rule")
                                | (State.edit_field_key == "auto_calc_rule")
                            ),
                            rx.text_area(
                                value=State.edit_field_value,
                                on_change=State.set_edit_field_value,
                                width="100%",
                                height="140px",
                            ),
                            rx.input(
                                value=State.edit_field_value,
                                on_change=State.set_edit_field_value,
                                width="100%",
                            ),
                        ),
                        rx.cond(
                            State.edit_modal_error != "",
                            rx.text(State.edit_modal_error, color="#c53030", white_space="pre-wrap"),
                            rx.fragment(),
                        ),
                        rx.hstack(
                            rx.button("취소", variant="ghost", on_click=State.close_edit_modal),
                            rx.button(
                                "저장 후 재생성",
                                color_scheme="blue",
                                variant="solid",
                                on_click=State.apply_edit_and_regenerate,
                            ),
                            spacing="2",
                            justify="end",
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    max_width="720px",
                ),
                open=State.edit_modal_open,
            ),
            width="100%",
            style={"display": "flex", "flexDirection": "column", "gap": "0.75rem", "height": panel_height, "minWidth": "0"},
        )

    def fs_viewer():
        return rx.box(
            rx.hstack(
                rx.text("1. Functional Spec (읽기 전용)", font_weight="bold"),
                rx.spacer(),
                spacing="2",
                width="100%",
                align_items="center",
            ),
            rx.cond(
                State.fs_error != "",
                rx.box(
                    rx.text(State.fs_error, color="#c53030", white_space="pre-wrap"),
                    width="100%",
                    padding="0.75em",
                    border="1px solid #fed7d7",
                    background_color="#fff5f5",
                    border_radius="12px",
                ),
                rx.fragment(),
            ),
            rx.cond(
                (State.generated_fs == "") | (State.fs_blocks.length() == 0),
                rx.box(
                    rx.text(
                        "아직 생성된 FS가 없습니다. 아래 버튼(상세 분석 및 FS 생성 시작)을 눌러 생성하세요.",
                        color="#718096",
                        white_space="pre-wrap",
                    ),
                    width="100%",
                    padding="1em",
                    border="1px solid #e2e8f0",
                    background_color="#f8fafc",
                    border_radius="12px",
                ),
                rx.scroll_area(
                    rx.vstack(
                        rx.foreach(
                            State.fs_blocks,
                            lambda b: rx.box(
                                rx.heading(b.title, size="4", color="#2b6cb0"),
                                rx.divider(margin_y="0.5em"),
                                rx.markdown(
                                    b.content_md,
                                    width="100%",
                                    style={"fontSize": "0.92em"},
                                ),
                                width="100%",
                                padding="1em",
                                border="1px solid #e2e8f0",
                                border_radius="12px",
                                background_color="white",
                                class_name="md-scroll md-render",
                            ),
                        ),
                        spacing="3",
                        width="100%",
                        align_items="start",
                    ),
                    type="always",
                    scrollbars="vertical",
                    style={"flex": "1", "minHeight": "0", "width": "100%"},
                ),
            ),
            width="100%",
            style={"display": "flex", "flexDirection": "column", "gap": "0.75rem", "height": panel_height, "minWidth": "0"},
        )

    return rx.box(
            rx.hstack(
            rx.box(
                fs_viewer(),
                style={"flex": "1 1 520px", "minWidth": "320px"},
                width="100%",
            ),
            rx.box(
                mapping_editor(),
                style={"flex": "1 1 520px", "minWidth": "320px"},
                width="100%",
            ),
            spacing="4",
            width="100%",
            align_items="stretch",
            flex_wrap="wrap",
        ),
        width="100%",
        height="100%",
        style={"minHeight": "0"},
    )


def view_fs_section_2():
    return _placeholder("FS 2. Include 구성")


def view_fs_section_3():
    return _placeholder("FS 3. 기능 매핑")


def view_fs_section_4():
    return _placeholder("FS 4. FORM 정의")


def view_fs_section_5():
    return _placeholder("FS 5. 조회 DB 매핑")


def view_fs_section_6():
    return _placeholder("FS 6. 저장 DB 매핑")


def view_fs_section_7():
    return _placeholder("FS 7. ALV 매핑")


def view_fs_section_8():
    return _placeholder("FS 8. 이벤트 매핑")


def view_fs_section_9():
    return _placeholder("FS 9. 저장 흐름")


def view_fs_section_10():
    return _placeholder("FS 10. 메시지")


def view_code_gen():
    return _placeholder("Code 생성")