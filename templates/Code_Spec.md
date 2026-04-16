# Code Template Specification

---

## 템플릿 운영 원칙

- TEMPLATE_ID는 BLOCK_ID 기준으로 TPL_ 접두어를 붙여 생성한다.
- 템플릿은 공통 코드 틀만 포함한다.
- 실제 값은 {placeholder} 형태로 AI가 치환한다.
- 하나의 BLOCK_ID는 기본적으로 하나의 TEMPLATE_ID를 가진다.
- 필요 시 세부 유형으로 확장 가능하다.

예:
- TPL_F01_SAVE_DB_DATA_MODIFY
- TPL_F01_SAVE_DB_DATA_INSERT
- TPL_F01_SELECT_JOIN

---

## TOP

### TPL_TOP_PROGRAM

    REPORT {program_id} MESSAGE-ID {message_class}.

### TPL_TOP_LOCAL_CLASS

    CLASS {local_class_name} DEFINITION DEFERRED.

### TPL_TOP_TABLES_CONTROLS

    TABLES: {tables_list}.
    CONTROLS: {control_name} TYPE TABSTRIP.

### TPL_TOP_GLOBAL_OBJECT

    DATA: go_container TYPE REF TO cl_gui_custom_container,
          go_alv_grid TYPE REF TO cl_gui_alv_grid,
          go_event TYPE REF TO {local_class_name}.

### TPL_TOP_ALV_ATTR

    DATA: gt_fcat TYPE lvc_t_fcat,
          gs_fcat TYPE lvc_s_fcat,
          gs_layout TYPE lvc_s_layo,
          gt_sort TYPE lvc_t_sort,
          gs_sort TYPE lvc_s_sort,
          gt_uifunctions TYPE ui_functions,
          gs_variant TYPE disvariant.

### TPL_TOP_DATA_ITAB

    TYPES: BEGIN OF {ty_data},
    {field_lines}
    END OF {ty_data}.

    DATA: gt_data TYPE TABLE OF {ty_data},
          gs_data TYPE {ty_data}.

    DATA: gt_save TYPE TABLE OF {save_type},
          gs_save TYPE {save_type}.

### TPL_TOP_GLOBAL_VAR

    DATA: gv_okcode TYPE sy-ucomm,
          gv_mode TYPE c LENGTH 1,
          gv_tabix TYPE sy-tabix.

### TPL_TOP_MACRO

    DEFINE _init.
      REFRESH &1.
      CLEAR &2.
    END-OF-DEFINITION.

---

## S01

### TPL_S01_BASE

    SELECTION-SCREEN BEGIN OF BLOCK {block_name} WITH FRAME TITLE text-{title_no}.
    SELECTION-SCREEN END OF BLOCK {block_name}.

### TPL_S01_PARAMETERS

    PARAMETERS: p_{field_id} TYPE {ddic_type} {obligatory}.

### TPL_S01_SELECT_OPTIONS

    SELECT-OPTIONS: s_{field_id} FOR {ref_field}.

### TPL_S01_SELECTION_UI

    PARAMETERS: p_{radio1} RADIOBUTTON GROUP {group},
                p_{radio2} RADIOBUTTON GROUP {group},
                p_{check} AS CHECKBOX.

### TPL_S01_SEARCH_HELP

    AT SELECTION-SCREEN ON VALUE-REQUEST FOR {field_name}.
    PERFORM {f4_form}.

### TPL_S01_LAYOUT

    SELECTION-SCREEN SKIP.
    SELECTION-SCREEN ULINE.

### TPL_S01_MODIF

    LOOP AT SCREEN.
      IF screen-group1 = '{modif_id}'.
        screen-input = 0.
        MODIFY SCREEN.
      ENDIF.
    ENDLOOP.

---

## C01

### TPL_C01_CLASS_DEF

    CLASS {local_class_name} DEFINITION.
      PUBLIC SECTION.
        CLASS-METHODS:
          hotspot_click FOR EVENT hotspot_click OF cl_gui_alv_grid
            IMPORTING e_row_id e_column_id.
    ENDCLASS.

### TPL_C01_CLASS_IMPL

    CLASS {local_class_name} IMPLEMENTATION.
      METHOD hotspot_click.
        PERFORM {delegate_form} USING e_row_id e_column_id.
      ENDMETHOD.
    ENDCLASS.

---

## O01

### TPL_O01_BASE

    MODULE status_0100 OUTPUT.
      PERFORM set_status.
      PERFORM init_screen.
    ENDMODULE.

---

## I01

### TPL_I01_BASE

    MODULE user_command_0100 INPUT.
      gv_okcode = sy-ucomm.
      CLEAR sy-ucomm.
      PERFORM user_command USING gv_okcode.
    ENDMODULE.

---

## F01_03 조회

### TPL_F01_SELECT

    FORM {form_name}.
      CLEAR gt_data.
      SELECT {select_fields}
        INTO CORRESPONDING FIELDS OF TABLE @gt_data
        FROM {from_table}
        WHERE {where_clause}
        {order_by_clause}.
    ENDFORM.

---

## F01_04 데이터 처리

### TPL_F01_LOOP

    FORM {form_name}.
      LOOP AT gt_data INTO gs_data.
        {process_logic}
        MODIFY gt_data FROM gs_data INDEX sy-tabix TRANSPORTING {transport_fields}.
      ENDLOOP.
    ENDFORM.

---

## F01_05 ALV

### TPL_F01_ALV_DISPLAY

    FORM display_alv.
      CALL METHOD go_alv_grid->set_table_for_first_display
        EXPORTING
          is_layout = gs_layout
          is_variant = gs_variant
          i_save = 'A'
        CHANGING
          it_outtab = gt_data
          it_fieldcatalog = gt_fcat
          it_sort = gt_sort.
    ENDFORM.

---

## F01_06 저장

### TPL_F01_SAVE_FLOW

    FORM save_data.
      CALL METHOD go_alv_grid->check_changed_data.
      PERFORM check_data.
      PERFORM make_save_data.
      PERFORM save_db_data.
      PERFORM after_save.
    ENDFORM.

### TPL_F01_SAVE_DB_DATA

    FORM save_db_data.
      MODIFY {save_table} FROM TABLE gt_save.
      IF sy-subrc = 0.
        COMMIT WORK.
      ELSE.
        ROLLBACK WORK.
        MESSAGE s000 WITH '저장 중 오류가 발생했습니다.' DISPLAY LIKE 'E'.
        RETURN.
      ENDIF.
    ENDFORM.