<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="role-page">
      <form class="role-search" method="get" action="/roles">
        <label>Role name <input type="text" name="role_name" :value="query_role_name"></label>
        <label>Permission key <input type="text" name="role_key" :value="query_role_key"></label>
        <label>Status
          <select v-if="state_all" name="state">
            <option value="" selected>All</option>
            <option value="0">Enabled</option>
            <option value="1">Disabled</option>
          </select>
          <select v-if="state_on" name="state">
            <option value="">All</option>
            <option value="0" selected>Enabled</option>
            <option value="1">Disabled</option>
          </select>
          <select v-if="state_off" name="state">
            <option value="">All</option>
            <option value="0">Enabled</option>
            <option value="1" selected>Disabled</option>
          </select>
        </label>
        <date-range>Created </date-range>
        <button class="user-btn user-btn-search" type="submit">Search</button>
        <a class="user-btn user-btn-reset" href="/roles">Reset</a>
      </form>
      <form class="role-work" method="get" action="/roles">
        <input type="hidden" name="role_name" :value="query_role_name">
        <input type="hidden" name="role_key" :value="query_role_key">
        <input type="hidden" name="state" :value="query_state">
        <input type="hidden" name="begin" :value="query_begin">
        <input type="hidden" name="end" :value="query_end">
        <div class="user-toolbar">
          <a v-if="can_add" class="user-btn user-btn-add" :href="add_href">Add</a>
          <button v-if="can_edit" class="user-btn user-btn-edit" type="submit" name="form" value="edit">Edit</button>
          <button v-if="can_remove" class="user-btn user-btn-remove" type="submit" name="form" value="remove">Remove</button>
          <a v-if="can_export" class="user-btn user-btn-export" :href="export_href">Export</a>
        </div>
        <el-table :data="rows">
          <el-table-column v-if="can_choose">
            <template #header>
              <input class="table-check" type="checkbox" aria-label="check all">
            </template>
            <input class="table-check" type="checkbox" name="role_id" aria-label="Select row" :value="row.role_id">
          </el-table-column>
          <el-table-column prop="role_id" label="Role id" />
          <el-table-column label="Role name">
            <a v-if="edit_action" class="role-name" :href="row.edit_href">{{ row.role_name }}</a>
            <span v-if="not edit_action">{{ row.role_name }}</span>
          </el-table-column>
          <el-table-column prop="role_key" label="Permission key" />
          <el-table-column label="Data scope">
            <el-tag :type="row.scope_type">{{ row.scope_label }}</el-tag>
          </el-table-column>
          <el-table-column prop="role_sort" label="Display order" />
          <el-table-column label="Status">
            <el-switch :value="row.status" :label="row.status_label" :form="row.status_form" :post="row.status_post"></el-switch>
          </el-table-column>
          <el-table-column prop="created" label="Created" />
          <el-table-column label="Action">
            <a v-if="edit_action" class="user-btn user-btn-edit" :href="row.edit_href">Edit</a>
            <a v-if="remove_action" class="user-btn user-btn-remove" :href="row.remove_href">Remove</a>
            <details v-if="scope_action" class="role-more">
              <summary class="user-btn user-btn-more">More</summary>
              <a class="user-btn user-btn-edit" :href="row.scope_href">Data scope</a>
            </details>
          </el-table-column>
        </el-table>
        <p class="role-count">{{ count_line }}</p>
      </form>
      <form v-if="can_edit" v-for="row in rows" method="post" action="/roles/status" :id="row.status_form">
        <input type="hidden" name="csrf" :value="csrf">
        <input type="hidden" name="role_id" :value="row.role_id">
        <input type="hidden" name="status" :value="row.status_next">
        <input type="hidden" name="role_name" :value="query_role_name">
        <input type="hidden" name="role_key" :value="query_role_key">
        <input type="hidden" name="state" :value="query_state">
        <input type="hidden" name="begin" :value="query_begin">
        <input type="hidden" name="end" :value="query_end">
      </form>
      <el-dialog v-if="show_add" title="Add a role">
        <el-form method="post" action="/roles/add">
          <input type="hidden" name="csrf" :value="csrf">
          <el-form-item label="Role name">
            <el-input name="role_name" />
          </el-form-item>
          <el-form-item label="Permission key">
            <el-input name="role_key" />
          </el-form-item>
          <el-form-item label="Display order">
            <el-input name="role_sort" value="0" />
          </el-form-item>
          <el-form-item label="Status">
            <el-switch name="status" value="0"></el-switch>
          </el-form-item>
          <el-form-item label="Remark">
            <el-input name="remark" />
          </el-form-item>
          <el-form-item label="Menus">
            <el-tree :data="menus" show-checkbox name="menu_id" node-key="menu_id" label-key="menu_name" />
          </el-form-item>
          <el-button type="primary" class="user-btn user-btn-add">Add</el-button>
        </el-form>
      </el-dialog>
      <el-dialog v-if="show_edit" title="Edit a role">
        <el-form method="post" action="/roles/edit">
          <input type="hidden" name="csrf" :value="csrf">
          <input type="hidden" name="role_id" :value="edit_role_id">
          <el-form-item label="Role name">
            <el-input name="role_name" :value="edit_name" />
          </el-form-item>
          <el-form-item label="Permission key">
            <el-input name="role_key" :value="edit_key" />
          </el-form-item>
          <el-form-item label="Display order">
            <el-input name="role_sort" :value="edit_sort" />
          </el-form-item>
          <el-form-item label="Status">
            <el-switch name="status" :value="edit_status"></el-switch>
          </el-form-item>
          <el-form-item label="Remark">
            <el-input name="remark" :value="edit_remark" />
          </el-form-item>
          <el-form-item label="Menus">
            <el-tree :data="menus" show-checkbox name="menu_id" node-key="menu_id" label-key="menu_name" />
          </el-form-item>
          <el-button type="primary" class="user-btn user-btn-edit">Save</el-button>
        </el-form>
      </el-dialog>
      <el-dialog v-if="show_remove" title="Remove a role">
        <el-form method="post" action="/roles/remove">
          <input type="hidden" name="csrf" :value="csrf">
          <input type="hidden" name="role_id" :value="remove_role_id">
          <p>{{ remove_name }}</p>
          <el-button type="primary" class="user-btn user-btn-remove">Remove</el-button>
        </el-form>
      </el-dialog>
      <el-dialog v-if="show_scope" title="Data scope">
        <el-form method="post" action="/roles/grant">
          <input type="hidden" name="csrf" :value="csrf">
          <input type="hidden" name="role_id" :value="scope_role_id">
          <input v-for="menu in scope_menus" type="hidden" name="menu_id" :value="menu.menu_id">
          <el-form-item label="Role name">
            <span>{{ scope_name }}</span>
          </el-form-item>
          <el-form-item label="Permission key">
            <span>{{ scope_key }}</span>
          </el-form-item>
          <el-form-item label="Data scope">
            <select v-if="scope_1" name="data_scope">
              <option value="1" selected>All data</option>
              <option value="2">Custom data</option>
              <option value="3">This department</option>
              <option value="4">Department and children</option>
            </select>
            <select v-if="scope_2" name="data_scope">
              <option value="1">All data</option>
              <option value="2" selected>Custom data</option>
              <option value="3">This department</option>
              <option value="4">Department and children</option>
            </select>
            <select v-if="scope_3" name="data_scope">
              <option value="1">All data</option>
              <option value="2">Custom data</option>
              <option value="3" selected>This department</option>
              <option value="4">Department and children</option>
            </select>
            <select v-if="scope_4" name="data_scope">
              <option value="1">All data</option>
              <option value="2">Custom data</option>
              <option value="3">This department</option>
              <option value="4" selected>Department and children</option>
            </select>
          </el-form-item>
          <el-form-item label="Department id">
            <el-input name="dept_id" :value="scope_dept" />
          </el-form-item>
          <el-button type="primary">Grant</el-button>
        </el-form>
      </el-dialog>
    </div>
  </shell>
</template>
