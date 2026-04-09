import reflex as rx
from typing import List
from pydantic import BaseModel # 추가
import os
import google.generativeai as genai


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
    input_sections: List[str] = [
        "1. 프로그램 기본 정보",
        "2. 프로그램 유형 & 상세 기능",
        "3. 화면 구조 및 동작",
        "4. 조회 조건 (Selection Screen)",
        "5. 조회 결과 리스트 (ALV Grid)",
        "6. 업무 처리 및 데이터 규칙",
    ]
    input_section_ids: List[str] = [
        "input-1",
        "input-2",
        "input-3",
        "input-4",
        "input-5",
        "input-6",
    ]

    fs_sections: List[str] = [
        "1. 프로그램 기본 정보",
        "2. Include 구성",
        "3. 기능 매핑",
        "4. FORM 정의",
        "5. 조회 DB 매핑",
        "6. 저장 DB 매핑",
        "7. ALV 매핑",
        "8. 이벤트 매핑",
        "9. 저장 흐름",
        "10. 메시지",
    ]
    fs_section_ids: List[str] = [
        "fs-1",
        "fs-2",
        "fs-3",
        "fs-4",
        "fs-5",
        "fs-6",
        "fs-7",
        "fs-8",
        "fs-9",
        "fs-10",
    ]

    code_sections: List[str] = ["Code 생성"]
    code_section_ids: List[str] = ["code-1"]

    sections: List[str] = input_sections + fs_sections + code_sections

    current_section: str = sections[0]
    hovered_section: str = ""
    expanded_sidebar_group: str = "input"

    def set_current_section(self, section: str):
        self.current_section = section

    def set_hovered_section(self, section: str):
        self.hovered_section = section

    def toggle_sidebar_group(self, group: str):
        self.expanded_sidebar_group = "" if self.expanded_sidebar_group == group else group

    def toggle_input_group(self):
        was_open = self.expanded_sidebar_group == "input"
        self.toggle_sidebar_group("input")
        if not was_open:
            self.current_section = self.input_sections[0]

    def toggle_fs_group(self):
        was_open = self.expanded_sidebar_group == "fs"
        self.toggle_sidebar_group("fs")
        if not was_open:
            self.current_section = self.fs_sections[0]

    def toggle_code_group(self):
        was_open = self.expanded_sidebar_group == "code"
        self.toggle_sidebar_group("code")
        if not was_open:
            self.current_section = self.code_sections[0]


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

    generated_fs: str = ""
    fs_error: str = ""
    is_generating_fs: bool = False

    # --- 핸들러 함수들 ---
    def set_prog_name(self, value: str):
        self.prog_name = value

    def set_req_dept_user(self, value: str):
        self.req_dept_user = value

    def set_work_category(self, value: str):
        self.work_category = value

    def set_prog_type(self, value: str):
        self.prog_type = value

    def set_ui_layout(self, value: str):
        self.ui_layout = value

    def set_layout_detail(self, value: str):
        self.layout_detail = value

    def set_edit_auth(self, value: str):
        self.edit_auth = value

    def set_other_ui_notes(self, value: str):
        self.other_ui_notes = value

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

    def delete_alv_row(self, area: str, index: int):
        target = self.alv_fields_a if area == "A" else self.alv_fields_b
        target.pop(index)

    def handle_submit(self):
        if not self.prog_name:
            return rx.window_alert("프로그램 이름을 입력해주세요!")
        return self.generate_fs()

    def _read_fs_template(self) -> str:
        template_path = os.path.join("templates", "FS_Functional_Spec.md")
        if not os.path.exists(template_path):
            raise FileNotFoundError(
                f"FS 템플릿 파일을 찾을 수 없습니다: {template_path}"
            )
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def _build_fs_prompt(self, template: str) -> str:
        selection_rows = [
            {
                "order": f.order,
                "section": f.section,
                "label": f.label,
                "field_id": f.field_id,
                "input_type": f.input_type,
                "is_required": f.is_required,
                "has_f4": f.has_f4,
                "ui_rule": f.ui_rule,
            }
            for f in self.selection_fields
        ]
        alv_a = [
            {
                "order": f.order,
                "label": f.label,
                "field_id": f.field_id,
                "is_key": f.is_key,
                "is_sum": f.is_sum,
                "is_edit": f.is_edit,
                "action": f.action,
            }
            for f in self.alv_fields_a
        ]
        alv_b = [
            {
                "order": f.order,
                "label": f.label,
                "field_id": f.field_id,
                "is_key": f.is_key,
                "is_sum": f.is_sum,
                "is_edit": f.is_edit,
                "action": f.action,
            }
            for f in self.alv_fields_b
        ]

        # 템플릿 구조를 유지하면서, 아래 입력값으로 빈 칸을 채우도록 유도
        return f"""
당신은 SAP ABAP Functional Spec 작성자입니다.
아래 "템플릿"의 구조(헤더/섹션/표/번호)를 최대한 유지하면서, "입력 데이터"를 사용해 내용을 채워서
완성된 Functional Spec 문서를 한국어로 작성하세요.

규칙:
- 출력은 마크다운만 반환
- 템플릿의 섹션 순서/형식을 유지 (추가 섹션이 필요하면 맨 아래에 최소로)
- 값이 비어있는 항목은 "TBD"로 표기
- 표 형태가 있는 템플릿은 표를 유지

템플릿:
```md
{template}
```

입력 데이터(JSON):
```json
{{
  "program_basic": {{
    "prog_name": "{self.prog_name}",
    "req_dept_user": "{self.req_dept_user}",
    "work_category": "{self.work_category}",
    "ref_tcode": "{self.ref_tcode}",
    "auth_range": {self.auth_range}
  }},
  "program_type": {{
    "prog_type": "{self.prog_type}",
    "selected_features": {self.selected_features}
  }},
  "ui_layout": {{
    "ui_layout": "{self.ui_layout}",
    "layout_detail": "{self.layout_detail}",
    "ui_features": {self.ui_features},
    "edit_auth": "{self.edit_auth}",
    "other_ui_notes": "{self.other_ui_notes}"
  }},
  "selection_screen": {selection_rows},
  "alv_area_a": {alv_a},
  "alv_area_b": {alv_b},
  "business_rules": {{
    "logic_flow": "{self.logic_flow}",
    "data_target": {self.data_target}
  }}
}}
```
""".strip()

    def generate_fs(self):
        self.is_generating_fs = True
        self.fs_error = ""
        self.generated_fs = ""

        try:
            api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise RuntimeError("환경변수 GEMINI_API_KEY(또는 GOOGLE_API_KEY)가 설정되어 있지 않습니다.")

            template = self._read_fs_template()
            prompt = self._build_fs_prompt(template)

            genai.configure(api_key=api_key)
            # Model selection:
            # - Prefer explicit env override
            # - Otherwise try common stable aliases
            # - If those fail (404 / unsupported), pick the first model that supports generateContent.
            preferred = (os.environ.get("GEMINI_MODEL") or "").strip()
            candidates = [m for m in [preferred, "gemini-1.5-pro-latest", "gemini-2.0-flash", "gemini-1.5-flash-latest"] if m]

            last_err: Exception | None = None
            resp = None
            for name in candidates:
                try:
                    resp = genai.GenerativeModel(name).generate_content(prompt)
                    last_err = None
                    break
                except Exception as e:
                    last_err = e

            if resp is None:
                try:
                    # Fallback: discover an available model supporting generateContent.
                    for m in genai.list_models():
                        methods = getattr(m, "supported_generation_methods", []) or []
                        if "generateContent" in methods or "generate_content" in methods:
                            model_name = getattr(m, "name", "")
                            if model_name.startswith("models/"):
                                model_name = model_name.replace("models/", "", 1)
                            resp = genai.GenerativeModel(model_name).generate_content(prompt)
                            last_err = None
                            break
                except Exception as e:
                    last_err = e

            if resp is None:
                raise RuntimeError(f"사용 가능한 Gemini 모델을 찾지 못했습니다. 마지막 오류: {last_err}")

            self.generated_fs = (resp.text or "").strip()

            # 생성 후 FS 그룹으로 열어두기
            self.expanded_sidebar_group = "fs"
            self.current_section = self.fs_sections[0]

            if not self.generated_fs:
                raise RuntimeError("FS 생성 결과가 비어 있습니다. (Gemini 응답이 empty)")
            return rx.window_alert("✅ FS 생성 완료! (FS 탭에서 확인하세요)")
        except Exception as e:
            self.fs_error = str(e)
            return rx.window_alert(f"❌ FS 생성 실패: {e}")
        finally:
            self.is_generating_fs = False

    # state.py 에 이 함수가 있는지 확인이 필요합니다

    def set_ref_tcode(self, value: str):
        self.ref_tcode = value

    def update_data_target(self, value: str, checked: bool):
        if checked:
            self.data_target.append(value)
        else:
            self.data_target = [i for i in self.data_target if i != value]
