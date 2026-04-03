import reflex as rx
from typing import List
from pydantic import BaseModel # 추가


class SelectionField(BaseModel):
    order: str = ""
    section: str = ""
    label: str = ""
    field_id: str = ""
    input_type: str = "단일"
    is_required: bool = False
    has_f4: bool = False
    ui_rule: str = ""


class ALVField(BaseModel):
    order: str = ""
    label: str = ""
    field_id: str = ""
    is_key: bool = False
    is_sum: bool = False
    is_edit: bool = False
    action: str = ""


# --- 메인 상태 (내비게이션 관리) ---
class StateMain(rx.State):
    sections: List[str] = [
        "1. 프로그램 기본 정보",
        "2. 프로그램 유형 & 상세 기능",
        "3. 화면 구조 및 동작",
        "4. 조회 조건 (Selection Screen)",
        "5. 조회 결과 리스트 (ALV Grid)",
        "6. 업무 처리 및 데이터 규칙",
    ]
    current_section: str = sections[0]
    hovered_section: str = ""

    def set_current_section(self, section: str):
        self.current_section = section

    def set_hovered_section(self, section: str):
        self.hovered_section = section


# --- 데이터 상태 (입력값 관리) ---
class State(StateMain):  # StateMain을 상속받아 하나로 합침 (중복 방지)
    # 섹션 1
    prog_name: str = ""
    req_dept_user: str = ""
    work_category: str = ""
    ref_tcode: str = ""
    auth_range: List[str] = []
    work_options: List[str] = [
        "구매(MM)",
        "영업(SD)",
        "생산(PP)",
        "회계(FI)",
        "인사(HR)",
        "원가(CO)",
        "자산(AA)",
        "기타",
    ]

    # 섹션 2
    prog_type: str = "조회 전용"
    selected_features: List[str] = []

    # 섹션 3
    ui_layout: str = "단일 화면"
    layout_detail: str = ""
    ui_features: List[str] = []
    edit_auth: str = "조회 전용"
    other_ui_notes: str = ""

    # 섹션 4
    selection_fields: List[SelectionField] = [
        SelectionField(
            order="1",
            section="기본",
            label="회사 코드",
            field_id="BUKRS",
            input_type="단일",
            is_required=True,
            has_f4=True,
            ui_rule="1000 고정",
        )
    ]

    # 섹션 5
    alv_fields_a: List[ALVField] = [
        ALVField(
            order="1",
            label="전표 번호",
            field_id="BELNR",
            is_key=True,
            action="클릭 시 상세 조회",
        ),
        ALVField(order="2", label="처리 상태", field_id="STATUS", action="아이콘 표시"),
    ]
    alv_fields_b: List[ALVField] = [
        ALVField(order="1", label="품목 번호", field_id="BUZEI", is_key=True),
        ALVField(
            order="2",
            label="수량",
            field_id="MENGE",
            is_sum=True,
            is_edit=True,
            action="값 변경 시 재계산",
        ),
    ]

    # 섹션 6
    logic_flow: str = ""
    validation_rule: str = ""
    auto_calc_rule: str = ""
    data_target: List[str] = []
    delete_method: str = ""
    dup_check: str = ""

    # --- 핸들러 함수들 ---
    def update_auth_range(self, value: str, checked: bool):
        if checked:
            self.auth_range.append(value)
        else:
            self.auth_range.remove(value)

    def add_selection_row(self):
        self.selection_fields.append(
            SelectionField(order=str(len(self.selection_fields) + 1))
        )

    def update_field(self, index: int, key: str, value: any):
        setattr(self.selection_fields[index], key, value)

    def delete_selection_row(self, index: int):
        self.selection_fields.pop(index)

    def update_list(self, attr_name: str, value: str, checked: bool):
        curr = getattr(self, attr_name).copy()
        if checked:
            curr.append(value)
        else:
            curr.remove(value)
        setattr(self, attr_name, curr)

    def add_alv_row(self, area: str):
        target = self.alv_fields_a if area == "A" else self.alv_fields_b
        target.append(ALVField(order=str(len(target) + 1)))

    def update_alv_field(self, area: str, index: int, key: str, value: any):
        target = self.alv_fields_a if area == "A" else self.alv_fields_b
        setattr(target[index], key, value)

    def handle_submit(self):
        if not self.prog_name:
            return rx.window_alert("프로그램 이름을 입력해주세요!")
        return rx.window_alert("✅ 저장 완료! AI 분석을 시작합니다.")

    # state.py 에 이 함수가 있는지 확인이 필요합니다

    def update_data_target(self, value: str, checked: bool):
        if checked:
            self.data_target.append(value)
        else:
            self.data_target = [i for i in self.data_target if i != value]
