<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="dict-page">
      <form class="user-search" method="get" action="/dicts">
        <label>Dictionary name <input type="text" name="dict_name" :value="query_dict_name"></label>
        <label>Dictionary type <input type="text" name="dict_type" :value="query_dict_type"></label>
        <label>Status
          <select v-if="status_all" name="status">
            <option value="" selected>All</option>
            <option value="0">Normal</option>
            <option value="1">Disabled</option>
          </select>
          <select v-if="status_on" name="status">
            <option value="">All</option>
            <option value="0" selected>Normal</option>
            <option value="1">Disabled</option>
          </select>
          <select v-if="status_off" name="status">
            <option value="">All</option>
            <option value="0">Normal</option>
            <option value="1" selected>Disabled</option>
          </select>
        </label>
        <date-range>Created </date-range>
        <button class="user-btn user-btn-search" type="submit">Search</button>
        <a class="user-btn user-btn-reset" href="/dicts">Reset</a>
      </form>
      <div class="user-toolbar">
        <a v-if="can_add" class="user-btn user-btn-add" :href="add_href">Add a dictionary value</a>
      </div>
      <el-table :data="rows">
        <el-table-column prop="dict_id" label="Dictionary id" />
        <el-table-column prop="dict_name" label="Dictionary name" />
        <el-table-column prop="dict_type" label="Dictionary type" />
        <el-table-column label="Status">
          <el-tag :type="row.status_kind">{{ row.status_label }}</el-tag>
        </el-table-column>
        <el-table-column prop="remark" label="Remark" />
        <el-table-column prop="created" label="Created" />
      </el-table>
      <p class="dict-count">{{ count_line }}</p>
      <el-dialog v-if="show_add" title="Add a dictionary value">
        <el-form method="post" action="/dicts/add">
          <input type="hidden" name="csrf" :value="csrf">
          <el-form-item label="Type">
            <el-input name="dict_type" />
          </el-form-item>
          <el-form-item label="Label">
            <el-input name="dict_label" />
          </el-form-item>
          <el-form-item label="Value">
            <el-input name="dict_value" />
          </el-form-item>
          <el-button type="primary" class="user-btn user-btn-add">Add</el-button>
        </el-form>
      </el-dialog>
    </div>
  </shell>
</template>
