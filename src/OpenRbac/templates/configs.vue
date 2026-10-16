<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="config-page">
      <form class="config-search" method="get" action="/configs">
        <label>Parameter name <input type="text" name="config_name" :value="query_config_name"></label>
        <label>Parameter key <input type="text" name="config_key" :value="query_config_key"></label>
        <label>Built-in
          <select v-if="type_all" name="config_type">
            <option value="" selected>All</option>
            <option value="Y">Yes</option>
            <option value="N">No</option>
          </select>
          <select v-if="type_yes" name="config_type">
            <option value="">All</option>
            <option value="Y" selected>Yes</option>
            <option value="N">No</option>
          </select>
          <select v-if="type_no" name="config_type">
            <option value="">All</option>
            <option value="Y">Yes</option>
            <option value="N" selected>No</option>
          </select>
        </label>
        <date-range>Created </date-range>
        <button class="user-btn user-btn-search" type="submit">Search</button>
        <a class="user-btn user-btn-reset" href="/configs">Reset</a>
      </form>
      <form class="config-work" method="get" action="/configs">
        <input type="hidden" name="config_name" :value="query_config_name">
        <input type="hidden" name="config_key" :value="query_config_key">
        <input type="hidden" name="config_type" :value="query_config_type">
        <input type="hidden" name="begin" :value="query_begin">
        <input type="hidden" name="end" :value="query_end">
        <div class="config-toolbar">
          <button v-if="can_edit" class="user-btn user-btn-edit" type="submit" name="form" value="edit">Change</button>
        </div>
        <el-table :data="rows">
          <el-table-column v-if="can_edit">
            <template #header>
              <input class="table-check" type="checkbox" aria-label="check all">
            </template>
            <input class="table-check" type="checkbox" name="config_id" aria-label="Select row" :value="row.config_id">
          </el-table-column>
          <el-table-column prop="config_id" label="Parameter id" />
          <el-table-column prop="config_name" label="Parameter name" />
          <el-table-column prop="config_key" label="Parameter key" />
          <el-table-column prop="config_value" label="Parameter value" />
          <el-table-column label="Built-in">
            <span :class="row.built_class">{{ row.built_label }}</span>
          </el-table-column>
          <el-table-column prop="remark" label="Remark" />
          <el-table-column prop="created" label="Created" />
          <el-table-column label="Action">
            <a v-if="can_edit" class="user-btn user-btn-edit" :href="row.change_href">Change</a>
          </el-table-column>
        </el-table>
      </form>
      <p>{{ count_line }}</p>
      <el-dialog v-if="show_edit" title="Change a parameter">
        <el-form method="post" action="/configs/set">
          <input type="hidden" name="csrf" :value="csrf">
          <input type="hidden" name="config_key" :value="edit_key">
          <p>{{ edit_name }}</p>
          <p>{{ edit_key }}</p>
          <label>Parameter value <textarea name="config_value">{{ edit_value }}</textarea></label>
          <button class="user-btn user-btn-edit" type="submit">Change</button>
          <a :href="close_href">Close</a>
        </el-form>
      </el-dialog>
    </div>
  </shell>
</template>
