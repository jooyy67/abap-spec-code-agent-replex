# 개발 매핑 입력서

## 1. 프로그램 기본 정보
FS 1, 2, 3, 5, 6, 8 기반 자동 생성

| 항목 | 값 | 생성 규칙 |
|------|----|-----------|
| Program ID |  | FS 1. 프로그램 기본정보 |
| Program Name |  | FS 1. 프로그램 기본정보 |
| Program Type | 조회 / 저장 / 조회+저장 | FS 2 |
| Main Screen | 0100 | FS 3 |
| ALV 사용 여부 | Y / N | FS 5 |
| Event Class 사용 여부 | Y / N | FS 8 |
| Save 기능 사용 여부 | Y / N | FS 6 |

---

## 2. Include 구성

### FS 전체 구조 기반 자동 결정

| Include ID | 설명 | 생성 여부 | 생성 규칙 |
|------------|------|-----------|-----------|
| TOP | 전역 선언 | Y | 항상 |
| S01 | Selection Screen |  | 조회조건 존재시 |
| C01 | 이벤트 클래스 |  | Event 기능 존재 시 |
| O01 | PBO |  | Dynpro 화면 사용 시 |
| I01 | PAI |  | Dynpro 화면 사용 시 |

### F01 블록 구성

| Block ID | 설명 | 생성 여부 | 생성 규칙 |
|----------|------|-----------|-----------|
| F01_01 | 구조 | Y | 항상 |
| F01_02 | 제어 |  | 분기/제어 존재 시 |
| F01_03 | 조회 |  | DB 조회 존재 시 |
| F01_04 | 데이터 처리 |  | 가공/계산 존재 시 |
| F01_05 | ALV |  | ALV 존재 시 |
| F01_06 | 저장 |  | Save 기능 존재 시 |

---

## 3. 기능 매핑
FS 8. 세부 기능 리스트 기반 자동 생성  
BLOCK / Include / TEMPLATE 연결 관리

| 기능 ID | 기능명 | 상세 정의 | 입력 연결 | 중요도 | BLOCK_ID | Include | TEMPLATE_ID | 생성 여부 | 비고 |
|--------|--------|-----------|-----------|--------|----------|---------|-------------|-----------|------|
| SCR_01 | 조회조건 제어 | 회사코드 고정 및 필드 제어 | Selection | 상 | S01_MODIF | S01 | TPL_S01_MODIF | Y | SCREEN_CONTROL |
| ALV_01 | 마스터/상세 연동 | 클릭 시 상세 조회 | ALV | 상 | F01_EVENT | F01_05 | TPL_F01_EVENT | Y | CLASS_IMPL |
| EVT_01 | 실시간 계산 | 수량 변경 시 금액 계산 | ALV | 중 | F01_DATA_CHANGED | F01_05 | TPL_F01_DATA_CHANGED | Y | REFRESH |
| VAL_01 | 저장 검증 | 필수값 및 선택 체크 | Rule | 상 | F01_CHECK_DATA | F01_06 | TPL_F01_CHECK_DATA | Y | MESSAGE |
| SAV_01 | 저장 처리 | 데이터 저장 처리 | Save | 상 | F01_SAVE_FLOW | F01_06 | TPL_F01_SAVE_FLOW | Y | 저장 흐름 |
| SAV_03 | DB 반영 | Z Table / 표준 반영 | Save | 상 | F01_SAVE_DB_DATA | F01_06 | TPL_F01_SAVE_DB_DATA | Y | MODIFY/BAPI |
| EXT_01 | 엑셀 다운로드 | 다운로드 처리 | File | 중 | F01_DOWNLOAD | F01_05 | TPL_F01_DOWNLOAD | 조건부 | 선택 시 |
| EXT_02 | 엑셀 업로드 | 업로드 처리 | File | 중 | F01_UPLOAD | F01_06 | TPL_F01_UPLOAD | 조건부 | 선택 시 |
| ALV_02 | 합계 처리 | 금액/수량 합계 표시 | ALV | 중 | F01_SORT_SUBTOTAL | F01_05 | TPL_F01_SORT | Y | LAYOUT |
| ALV_03 | 시각 효과 | 색상 / 아이콘 표시 | ALV | 중 | F01_COLOR_ICON | F01_05 | TPL_F01_COLOR_ICON | Y | FCAT_OPTION |

---

## 4. FORM 정의
기능 매핑 및 규칙 기반 생성

| FORM_NAME | BLOCK_ID | Include | TEMPLATE_ID | 순서 | 설명 |
|-----------|----------|---------|-------------|------|------|
| select_data | F01_SELECT | F01_03 | TPL_F01_SELECT | 1 | 조회 |
| process_data | F01_LOOP | F01_04 | TPL_F01_LOOP | 2 | 가공 |
| display_alv | F01_ALV_DISPLAY | F01_05 | TPL_F01_ALV_DISPLAY | 3 | 출력 |
| save_data | F01_SAVE_FLOW | F01_06 | TPL_F01_SAVE_FLOW | 4 | 저장 |

---

## 5. 조회 DB 매핑
FS 9.1 기반

| FORM | 테이블 | JOIN | WHERE 조건 | ORDER BY | 대상 ITAB |
|------|--------|------|------------|----------|-----------|
| select_data |  |  |  |  | GT_DATA |

---

## 6. 저장 DB 매핑
FS 9.2 기반

| FORM | 테이블 | 방식 | KEY 기준 | 대상 ITAB |
|------|--------|------|----------|-----------|
| save_db_data |  | MODIFY / INSERT / UPDATE / DELETE / BAPI |  | GT_SAVE |

---

## 7. ALV 매핑
FS 5 기반

| 영역 | 필드ID | 속성 | BLOCK_ID | 비고 |
|------|--------|------|----------|------|
| MAIN | BELNR | key | F01_FIELDCATALOG |  |
| MAIN | WRBTR | sum | F01_SORT_SUBTOTAL |  |
| DETAIL | MENGE | edit | F01_EDIT_MODE |  |
| MAIN | BELNR | hotspot | F01_EVENT |  |
| MAIN | STATUS | icon | F01_COLOR_ICON |  |

---

## 8. 이벤트 매핑
자동 생성 영역

| 이벤트 | BLOCK_ID | 클래스 | FORM | 후처리 FORM |
|--------|----------|--------|------|-------------|
| hotspot_click | F01_EVENT | LCL_EVENT_HANDLER | handle_event | select_detail |
| data_changed | F01_DATA_CHANGED | LCL_EVENT_HANDLER | handle_data_changed | process_data |

---

## 9. 저장 흐름
자동 생성 영역

| 단계 | FORM | BLOCK_ID |
|------|------|----------|
| CHECK | check_data | F01_CHECK_DATA |
| MAKE | make_save_data | F01_MAKE_SAVE_DATA |
| SAVE | save_db_data | F01_SAVE_DB_DATA |
| AFTER | after_save | F01_AFTER_SAVE |

---

## 10. 메시지
FS 10 기반

| MSG_ID | TYPE | TEXT | FORM |
|--------|------|------|------|
| MSG_001 | E |  | check_data |
| MSG_002 | S |  | after_save |

---

## 11. 비고
FS 11 기반  

| 항목 | 내용 |
|------|------|
| 참고 화면 |  |
| 참고 파일 |  |

---

## 특이사항