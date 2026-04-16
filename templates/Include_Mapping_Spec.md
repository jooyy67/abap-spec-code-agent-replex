# Include Mapping Specification

---

## 1. 문서 개요

### 1.1 목적
본 문서는 프로그램 생성 시 표준 BLOCK_ID를 어떤 Include에 배치할지,  
각 Include 내에서 어떤 FORM / CLASS / 선언 형태로 구현할지 정의한다.

---

### 1.2 적용 범위

- TOP Include  
- S01 Include  
- C01 Include  
- O01 Include  
- I01 Include  
- F01 Include  

---

### 1.3 생성 기준

- 사용자 요구사항 입력서  
- Functional Spec  
- 세부 기능 리스트  
- 개발 매핑 입력서  
- 표준 BLOCK 목록  
- 코드 템플릿(TPL)  

---

## 2. 프로그램 기본 정보

- Program ID  
- Program Name  
- Message Class  
- Main Screen No : 0100  

---

## 3. Include 구성

| Include ID | Include 명 | 역할 | 생성 여부 |
|------------|-----------|------|-----------|
| TOP | 전역 선언 | 프로그램 선언 | Y |
| S01 | Selection Screen | 조회조건 | Y/N |
| C01 | 이벤트 클래스 | 이벤트 처리 | Y/N |
| O01 | PBO 처리 | 화면 출력 | Y/N |
| I01 | PAI 처리 | 사용자 입력 처리 | Y/N |
| F01_01 | 구조 | FORM 규칙 | Y/N |
| F01_02 | 제어 | 흐름 제어 | Y/N |
| F01_03 | 조회 | DB 조회 | Y/N |
| F01_04 | 데이터 처리 | 가공 처리 | Y/N |
| F01_05 | ALV 출력 | 출력 처리 | Y/N |
| F01_06 | 저장/메시지 | 저장 처리 | Y/N |

---

## 4. TOP Include 매핑

| BLOCK_ID | Include | 선언 대상 | 생성 항목 | TEMPLATE_ID |
|----------|---------|----------|----------|-------------|
| TOP_PROGRAM | TOP | 프로그램 선언 | REPORT / MESSAGE-ID | TPL_TOP_PROGRAM |

---

## 5. S01 Include 매핑

| BLOCK_ID | Include | 대상 | 생성 항목 | TEMPLATE_ID |
|----------|---------|------|----------|-------------|
| S01_BASE | S01 | Selection Screen | SELECTION-SCREEN BEGIN/END | TPL_S01_BASE |
| S01_BLOCK | S01 | 화면 블록 | BLOCK 단위 구성 | TPL_S01_BLOCK |
| S01_PARAMETERS | S01 | 단일 입력 | PARAMETERS | TPL_S01_PARAMETERS |
| S01_SELECT_OPTIONS | S01 | 범위 입력 | SELECT-OPTIONS | TPL_S01_SELECT_OPTIONS |
| S01_SELECTION_UI | S01 | 선택형 입력 | RADIO / CHECKBOX / LISTBOX | TPL_S01_SELECTION_UI |
| S01_SEARCH_HELP | S01 | F4 도움말 | SEARCH HELP | TPL_S01_SEARCH_HELP |
| S01_LAYOUT | S01 | 화면 정리 | SKIP / ULINE | TPL_S01_LAYOUT |
| S01_MODIF | S01 | 동적 제어 | MODIF ID / SCREEN | TPL_S01_MODIF |

---

## 6. C01 Include 매핑

| BLOCK_ID | Include | 대상 | 생성 항목 | TEMPLATE_ID |
|----------|---------|------|----------|-------------|
| C01_BASE | C01 | 클래스 기본 | Local Class 구조 | TPL_C01_BASE |
| C01_METHOD_NAMING | C01 | 메서드 규칙 | 이벤트 명명 | TPL_C01_METHOD_NAMING |
| C01_CLASS_DEF | C01 | 클래스 정의 | CLASS DEFINITION | TPL_C01_CLASS_DEF |
| C01_CLASS_IMPL | C01 | 클래스 구현 | CLASS IMPLEMENTATION | TPL_C01_CLASS_IMPL |
| C01_DELEGATION | C01 | 위임 처리 | METHOD → PERFORM | TPL_C01_DELEGATION |

---

## 7. O01 Include 매핑

| BLOCK_ID | Include | FORM 명 | 생성 항목 | TEMPLATE_ID |
|----------|---------|--------|----------|-------------|
| O01_BASE | O01 | STATUS_0100 / PBO_0100 | PBO 기본 구조 | TPL_O01_BASE |
| O01_STATUS | O01 | SET_STATUS | PF-STATUS / TITLEBAR | TPL_O01_STATUS |
| O01_EXCLUDING | O01 | EXCLUDE_BUTTON | 버튼 제외 처리 | TPL_O01_EXCLUDING |

---

## 8. I01 Include 매핑

| BLOCK_ID | Include | FORM 명 | 생성 항목 | TEMPLATE_ID |
|----------|---------|--------|----------|-------------|
| I01_BASE | I01 | USER_COMMAND_0100 | PAI 기본 구조 | TPL_I01_BASE |
| I01_EXIT | I01 | EXIT_0100 | 종료 처리 | TPL_I01_EXIT |
| I01_COMMAND | I01 | USER_COMMAND_0100 | OK_CODE CASE 분기 | TPL_I01_COMMAND |
| I01_TAB | I01 | TAB_CONTROL | 탭 처리 | TPL_I01_TAB |

---

## 9. F01 Include 매핑

### 9.1 F01_01 구조

| BLOCK_ID | Include | 생성 항목 | TEMPLATE_ID |
|----------|---------|----------|-------------|
| F01_FORM_PERFORM | F01_01 | FORM / PERFORM 구조 | TPL_F01_FORM_PERFORM |

---

### 9.2 F01_02 제어

- SET_INIT_VALUE
- BRANCH_LOGIC (IF / CASE)
- FLOW_CONTROL (CHECK / EXIT / RETURN)
- STOP_PROCESS
- LEAVE_LIST

---

### 9.3 F01_03 조회

- SELECT_DATA
- SELECT_SINGLE_DATA
- ORDER BY 처리

---

### 9.4 F01_04 데이터 처리

- LOOP 가공
- SORT 처리
- MODIFY / APPEND / DELETE

---

### 9.5 F01_05 ALV

- CREATE_OBJECT
- DISPLAY_ALV
- SET_FIELDCATALOG
- SET_LAYOUT
- SET_SORT / SUBTOTAL
- EVENT 처리

---

### 9.6 F01_06 저장/메시지

- CHECK_DATA
- SAVE_DATA
- SAVE_DB_DATA
- AFTER_SAVE
- MESSAGE 처리

---

## 10. 기능 ID → BLOCK 매핑

| 기능 ID | 필수 BLOCK |
|--------|-----------|
| SCR_01 | S01_MODIF |
| ALV_01 | F01_EVENT |
| EVT_01 | F01_DATA_CHANGED |
| SAV_01 | F01_SAVE_FLOW |
| SAV_03 | F01_SAVE_DB_DATA |
| ALV_02 | F01_SORT_SUBTOTAL |
| ALV_03 | F01_COLOR_ICON |
| EXT_01 | F01_DOWNLOAD / F01_UPLOAD |

---

## 11. 코드 생성 순서

1. TOP  
2. S01  
3. C01  
4. O01  
5. I01  
6. F01_01  
7. F01_02  
8. F01_03  
9. F01_04  
10. F01_05  
11. F01_06  

---

## 12. 생성 조건 / 비고

- 조회 전용 프로그램은 저장 관련 BLOCK 생성하지 않음  
- ALV 미사용 시 ALV 관련 BLOCK 생성하지 않음  
- 이벤트 미사용 시 클래스 생성하지 않음  
- 팝업/탭 구조 사용 시 O01 / I01 추가 생성  
- 업로드 기능 사용 시 검증 BLOCK 함께 생성  