---

database-plugin: basic

---

```yaml:dbfolder
name: DB_テーマ
description: new description
columns:
  __file__:
    key: __file__
    id: __file__
    input: markdown
    label: File
    accessorKey: __file__
    isMetadata: true
    skipPersist: false
    isDragDisabled: false
    csvCandidate: true
    position: 1
    isHidden: false
    sortIndex: -1
    width: 100
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: true
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      content_alignment: text-align-left
      wrap_content: true
  __modified__:
    key: __modified__
    id: __modified__
    input: metadata_time
    label: Modified
    accessorKey: __modified__
    isMetadata: true
    isDragDisabled: false
    skipPersist: false
    csvCandidate: true
    position: 3
    isHidden: false
    sortIndex: -1
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  記入:
    input: checkbox
    accessorKey: 記入
    key: 記入
    id: 記入
    label: 記入
    position: 2
    skipPersist: false
    isHidden: false
    sortIndex: -1
    width: 337
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
config:
  remove_field_when_delete_column: false
  cell_size: compact
  sticky_first_column: false
  group_folder_column: 
  remove_empty_folders: false
  automatically_group_files: false
  hoist_files_with_empty_attributes: true
  show_metadata_created: false
  show_metadata_modified: true
  show_metadata_tasks: false
  show_metadata_inlinks: false
  show_metadata_outlinks: false
  show_metadata_tags: false
  source_data: current_folder
  source_form_result: 
  source_destination_path: /
  row_templates_folder: /
  current_row_template: 
  pagination_size: 200
  font_size: 14
  enable_js_formulas: true
  formula_folder_path: /
  inline_default: false
  inline_new_position: last_field
  date_format: yyyy-MM-dd
  datetime_format: yyyy-MM-dd
  metadata_date_format: yyyy-MM-dd
  enable_footer: false
  implementation: default
filters:
  enabled: true
  conditions:
      - condition: AND
        disabled: true
        label: "未記入"
        color: "hsl(6,91%,71%)"
        filters:
        - field: 記入
          operator: IS_EMPTY
          value: "true"
          type: checkbox
        - field: 記入
          operator: NOT_CONTAINS
          value: "true"
          type: checkbox
      - condition: AND
        disabled: true
        label: "完了"
        color: "hsl(119,99%,69%)"
        filters:
        - field: 記入
          operator: CONTAINS
          value: "true"
          type: checkbox
```