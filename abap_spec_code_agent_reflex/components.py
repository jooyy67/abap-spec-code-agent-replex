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
            is_checked=State.selected_features.contains(label),
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
        is_checked=State.auth_range.contains(label),
        on_change=lambda b: State.update_auth_range(label, b),
    )

# --- 2. 섹션별 가변 뷰 (오른쪽 모니터 화면용) ---

def view_section_1():
    return rx.vstack(
        rx.text("프로그램 이름", font_weight="bold"),
        rx.input(
            value=State.prog_name,
            placeholder="예: 구매 현황 조회",
            on_change=State.set_prog_name,
            width="100%",
        ),
        rx.text("요청 부서/자", font_weight="bold"),
        rx.input(
            value=State.req_dept_user,
            placeholder="예: 회계팀 홍길동",
            on_change=State.set_req_dept_user,
            width="100%",
        ),
        rx.text("업무 구분", font_weight="bold"),
        rx.select(
            State.work_options,
            value=State.work_category,
            on_change=State.set_work_category,
            width="100%",
        ),
        rx.text("참조 T-Code", font_weight="bold"),
        rx.input(
            value=State.ref_tcode,
            placeholder="예: MM03, VA05",
            on_change=State.set_ref_tcode,
            width="100%",
        ),
        rx.text("사용 권한 범위", font_weight="bold"),
        rx.hstack(auth_item("모든 사용자"), auth_item("특정 부서"), auth_item("특정 플랜트"), spacing="4"),
        spacing="3", width="100%"
    )

def view_section_2():
    def prog_type_option(value: str, desc: str):
        is_selected = State.prog_type == value
        return rx.box(
            rx.hstack(
                rx.box(
                    width="16px",
                    height="16px",
                    border_radius="999px",
                    border=rx.cond(is_selected, "5px solid #2b6cb0", "2px solid #a0aec0"),
                    background_color="white",
                    flex_shrink="0",
                    margin_top="0.2em",
                ),
                rx.vstack(
                    rx.text(value, font_weight="600"),
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
        rx.text("메인 유형 (택 1)", font_weight="bold"),
        rx.vstack(
            prog_type_option("조회 전용", "데이터 조회 및 리포트 출력"),
            prog_type_option("저장 전용", "신규 입력 및 등록 (엑셀 업로드 포함 가능)"),
            prog_type_option("조회 + 저장", "조회 후 수정, 저장, 삭제, 승인까지 포함"),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        rx.divider(margin_y="0.75em"),
        rx.text("상세 기능 (중복 선택)", font_weight="bold"),
        rx.text("데이터 처리", font_weight="bold", color="#2b6cb0"),
        rx.vstack(
            feature_item("행 추가", "신규 데이터 입력"),
            feature_item("행 삭제", "데이터 제거"),
            feature_item("선택 행 처리", "체크된 데이터만 처리"),
            feature_item("일괄 처리", "전체 데이터 처리"),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        rx.text("파일 기능", font_weight="bold", color="#2b6cb0", margin_top="0.5em"),
        rx.vstack(
            feature_item("엑셀 업로드", "파일로 데이터 입력"),
            feature_item("엑셀 다운로드", "조회 결과 다운로드"),
            feature_item("템플릿 제공", "업로드용 양식 다운로드"),
            feature_item("파일 첨부", "문서 첨부 기능"),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        rx.text("출력 / 기타", font_weight="bold", color="#2b6cb0", margin_top="0.5em"),
        rx.vstack(
            feature_item("합계 / 소계 표시", "금액/수량 합계"),
            feature_item("변경 로그 기록", "이력 관리"),
            feature_item("승인 / 결재 연동", ""),
            feature_item("메일 알림", ""),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        spacing="4",
        width="100%",
    )

def view_section_3():
    return rx.vstack(
        rx.text("기본 구조 (택 1)", font_weight="bold"),
        rx.radio_group(
            ["단일 화면", "2분할 (위/아래)", "2분할 (좌/우)"],
            value=State.ui_layout,
            on_change=State.set_ui_layout,
            direction="row",
            spacing="4",
        ),
        rx.cond(
            State.ui_layout.contains("2분할"),
            rx.vstack(
                rx.text("└ 상세 동작 정의", color="#2b6cb0", font_weight="bold"),
                rx.radio_group(
                    ["연동형", "병렬형"],
                    value=State.layout_detail,
                    on_change=State.set_layout_detail,
                    direction="row",
                    spacing="4",
                ),
                rx.text("  • 연동형 (선택 시 상세 조회)", color="#718096"),
                rx.text("  • 병렬형 (독립 화면)", color="#718096"),
                padding_left="1em",
                border_left="2px solid #cbd5e0",
                spacing="2",
                width="100%",
                align_items="start",
            ),
            rx.fragment(),  # 에러 방지를 위해 rx.none() 대신 사용
        ),
        rx.divider(margin_y="0.5em"),
        rx.text("추가 구조 / 기능", font_weight="bold"),
        rx.vstack(
            rx.checkbox("탭(Tab) 사용", on_change=lambda b: State.update_list("ui_features", "탭(Tab) 사용", b)),
            rx.checkbox(
                "팝업창 사용 (조회 / 입력)",
                on_change=lambda b: State.update_list("ui_features", "팝업창 사용 (조회 / 입력)", b),
            ),
            spacing="2",
            width="100%",
            align_items="start",
        ),
        rx.divider(margin_y="0.5em"),
        rx.text("편집 권한", font_weight="bold"),
        rx.radio_group(
            ["조회 전용", "수정 / 입력 / 삭제 가능"],
            value=State.edit_auth,
            on_change=State.set_edit_auth,
            direction="row",
            spacing="4",
        ),
        rx.divider(margin_y="0.5em"),
        rx.text("기타 사항", font_weight="bold"),
        rx.text_area(
            placeholder="예: 자동 새로고침 필요 등",
            value=State.other_ui_notes,
            on_change=State.set_other_ui_notes,
            width="100%",
            height="120px",
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
                    is_checked=State.show_selection_upload_debug,
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
                    table_body_cell(rx.center(rx.checkbox(is_checked=field.is_required, on_change=lambda b: State.update_field(idx, "is_required", b)))),
                    table_body_cell(rx.center(rx.checkbox(is_checked=field.has_f4, on_change=lambda b: State.update_field(idx, "has_f4", b)))),
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
    def alv_table(area: str, title: str, data):
        return rx.vstack(
            rx.text(title, font_weight="bold", color="#2b6cb0"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
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
                                        is_checked=field.is_key,
                                        on_change=lambda b: State.update_alv_field(area, idx, "is_key", b),
                                    )
                                )
                            ),
                            table_body_cell(
                                rx.center(
                                    rx.checkbox(
                                        is_checked=field.is_sum,
                                        on_change=lambda b: State.update_alv_field(area, idx, "is_sum", b),
                                    )
                                )
                            ),
                            table_body_cell(
                                rx.center(
                                    rx.checkbox(
                                        is_checked=field.is_edit,
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
        rx.text("SE11 캡처 이미지 업로드로 필드 목록을 추출해 지정한 테이블에 자동 반영할 수 있습니다.", color="#718096"),
        rx.hstack(
            rx.select(
                ["조회조건", "조회결과(영역 A)", "조회결과(영역 B)"],
                value=State.image_target,
                on_change=State.set_image_target,
                width="260px",
            ),
            rx.upload(
                rx.button("이미지 선택", variant="soft"),
                id="se11_image_upload",
                accept={"image/*": [".png", ".jpg", ".jpeg", ".webp"]},
                multiple=False,
            ),
            rx.button(
                "업로드 후 자동 반영",
                on_click=State.handle_image_upload(rx.upload_files(upload_id="se11_image_upload")),
                color_scheme="blue",
                variant="solid",
            ),
            rx.button(
                "선택 취소",
                on_click=rx.clear_selected_files("se11_image_upload"),
                variant="ghost",
            ),
            spacing="3",
            width="100%",
            align_items="center",
            flex_wrap="wrap",
        ),
        rx.cond(
            rx.selected_files("se11_image_upload").length() > 0,
            rx.hstack(
                rx.text("선택된 파일:", font_weight="bold", color="#4a5568"),
                rx.foreach(rx.selected_files("se11_image_upload"), rx.badge),
                spacing="2",
                flex_wrap="wrap",
                width="100%",
            ),
            rx.fragment(),
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
                    is_checked=State.show_alv_upload_debug,
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
        alv_table("A", "[영역 A: 메인 목록]", State.alv_fields_a),
        rx.divider(margin_y="0.75em"),
        alv_table("B", "[영역 B: 상세 / 팝업 / 탭]", State.alv_fields_b),
        spacing="4",
        width="100%",
        align_items="start",
    )

def view_section_6():
    return rx.vstack(
        rx.text("업무 흐름", font_weight="bold"),
        rx.text_area(
            value=State.logic_flow,
            placeholder="상세 로직 입력...",
            on_change=State.set_logic_flow,
            width="100%",
            height="150px",
        ),
        rx.text("반영 위치", font_weight="bold"),
        rx.hstack(
            rx.checkbox(
                "Z-Table",
                is_checked=State.data_target.contains("Z-Table"),
                on_change=lambda b: State.update_data_target("Z-Table", b),
            ),
            rx.checkbox(
                "BAPI",
                is_checked=State.data_target.contains("BAPI"),
                on_change=lambda b: State.update_data_target("BAPI", b),
            ),
            spacing="4"
        ),
        spacing="4", width="100%"
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
        return rx.vstack(
            rx.hstack(
                rx.text("개발 매핑 입력서 (편집 가능)", font_weight="bold"),
                rx.spacer(),
                rx.button(
                    "원본 입력값 수정 (TBD 보완)",
                    variant="soft",
                    on_click=State.open_edit_modal,
                ),
                rx.button(
                    "FS 기준으로 매핑 재생성",
                    variant="solid",
                    color_scheme="blue",
                    on_click=State.generate_mapping_sections,
                ),
                spacing="2",
                width="100%",
                align_items="center",
                flex_wrap="wrap",
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
            rx.hstack(
                rx.select(
                    mapping_sections,
                    value=State.mapping_active_section,
                    on_change=State.set_mapping_active_section,
                    width="280px",
                ),
                rx.cond(
                    (State.mapping_updated_at != ""),
                    rx.text(f"마지막 업데이트: {State.mapping_updated_at}", color="#718096", font_size="0.85em"),
                    rx.fragment(),
                ),
                spacing="3",
                width="100%",
                align_items="center",
                flex_wrap="wrap",
            ),
            rx.text_area(
                value=State.mapping_sections[State.mapping_active_section],
                placeholder="아직 생성된 개발 매핑 입력서가 없습니다. FS 생성 후 자동 생성되며, 여기서 직접 수정할 수 있습니다.",
                on_change=lambda v: State.update_mapping_section(State.mapping_active_section, v),
                width="100%",
                height="540px",
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
                            ],
                            value=State.edit_field_key,
                            on_change=State.set_edit_field_key,
                            width="100%",
                        ),
                        rx.text("값", font_weight="bold"),
                        rx.cond(
                            (State.edit_field_key == "other_ui_notes") | (State.edit_field_key == "logic_flow"),
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
            spacing="3",
            width="100%",
            align_items="start",
        )

    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text("Functional Spec (읽기 전용)", font_weight="bold"),
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
                rx.text_area(
                    value=State.generated_fs,
                    placeholder="아직 생성된 FS가 없습니다. 아래 버튼(상세 분석 및 FS 생성 시작)을 눌러 생성하세요.",
                    width="100%",
                    height="640px",
                    is_read_only=True,
                ),
                spacing="3",
                width="100%",
                align_items="start",
            ),
            mapping_editor(),
            spacing="4",
            width="100%",
            align_items="start",
            flex_wrap="wrap",
        ),
        spacing="3",
        width="100%",
        align_items="start",
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