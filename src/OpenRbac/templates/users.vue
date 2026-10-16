<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="note" class="user-note">{{ note }}</p>
    <div class="user-page">
      <aside class="user-org">
        <div class="user-org-head">
          <span>Organization</span>
          <a v-if="can_depts" class="user-org-manage" href="/depts">Departments</a>
        </div>
        <ul class="user-tree">
          <user-node v-for="dept in departments"></user-node>
        </ul>
      </aside>
      <div class="user-main">
        <div class="user-head">
          <h1>Users</h1>
          <p>Manage accounts, departments, and access.</p>
        </div>
        <form class="user-search" method="get" action="/users">
          <input type="hidden" name="state" :value="query_state">
          <div class="user-status" role="group" aria-label="Status">
            <a v-if="state_all" class="user-status-item is-current" :href="state_all_href">All</a>
            <a v-if="state_on" class="user-status-item" :href="state_all_href">All</a>
            <a v-if="state_off" class="user-status-item" :href="state_all_href">All</a>
            <a v-if="state_on" class="user-status-item is-current" :href="state_on_href">Enabled</a>
            <a v-if="state_all" class="user-status-item" :href="state_on_href">Enabled</a>
            <a v-if="state_off" class="user-status-item" :href="state_on_href">Enabled</a>
            <a v-if="state_off" class="user-status-item is-current" :href="state_off_href">Disabled</a>
            <a v-if="state_all" class="user-status-item" :href="state_off_href">Disabled</a>
            <a v-if="state_on" class="user-status-item" :href="state_off_href">Disabled</a>
          </div>
          <label>Login name <input type="text" name="user_name" :value="query_user_name"></label>
          <label>Phone <input type="text" name="phone" :value="query_phone"></label>
          <date-range>Created </date-range>
          <input v-if="query_dept" type="hidden" name="dept" :value="query_dept">
          <span class="user-search-actions">
            <button class="user-btn user-btn-search" type="submit">Search</button>
            <a class="user-btn user-btn-reset" href="/users">Reset</a>
          </span>
        </form>
        <form class="user-work" method="get" action="/users">
          <input type="hidden" name="user_name" :value="query_user_name">
          <input type="hidden" name="phone" :value="query_phone">
          <input type="hidden" name="state" :value="query_state">
          <input type="hidden" name="begin" :value="query_begin">
          <input type="hidden" name="end" :value="query_end">
          <input type="hidden" name="dept" :value="query_dept">
          <div class="user-toolbar">
            <p class="user-result">{{ total }} results</p>
            <div class="user-toolbar-actions">
            <a v-if="can_add" class="user-btn user-btn-add" :href="add_href">Add</a>
            <button v-if="can_edit" class="user-btn user-btn-edit" type="submit" name="form" value="edit">Edit</button>
            <button v-if="can_remove" class="user-btn user-btn-remove" type="submit" name="form" value="remove">Remove</button>
            <a v-if="can_import" class="user-btn user-btn-import" :href="import_href">Import</a>
            <a v-if="can_export" class="user-btn user-btn-export" :href="export_href">Export</a>
            </div>
          </div>
          <el-table :data="rows">
            <el-table-column v-if="can_choose" label="Choose">
              <input type="radio" name="user_id" :value="row.user_id">
            </el-table-column>
            <el-table-column label="User">
              <div class="user-person">
                <span class="user-person-mark">{{ row.initials }}</span>
                <div class="min-w-0">
                  <a v-if="can_edit" class="font-medium truncate hover:text-primary block" :href="row.edit_href">{{ row.nick_name }}</a>
                  <span v-else class="font-medium truncate block">{{ row.nick_name }}</span>
                  <div class="text-xs text-muted-foreground truncate">@{{ row.user_name }}</div>
                </div>
              </div>
            </el-table-column>
            <el-table-column prop="dept_name" label="Department" />
            <el-table-column prop="phone" label="Phone" />
            <el-table-column label="Status">
              <el-switch :value="row.status" :label="row.status_label" :form="row.status_form" :post="row.status_post"></el-switch>
            </el-table-column>
            <el-table-column prop="created" label="Created" />
            <el-table-column label="Action">
              <a v-if="can_edit" class="user-btn user-btn-edit" :href="row.edit_href">Edit</a>
              <a v-if="can_remove" class="user-btn user-btn-remove" :href="row.remove_href">Remove</a>
              <a v-if="can_reset" class="user-btn user-btn-resetpwd" :href="row.reset_href">Reset</a>
            </el-table-column>
          </el-table>
        </form>
        <form v-if="can_edit" v-for="row in rows" method="post" action="/users/status" :id="row.status_form">
          <input type="hidden" name="csrf" :value="csrf">
          <input type="hidden" name="user_id" :value="row.user_id">
          <input type="hidden" name="status" :value="row.status_next">
          <input type="hidden" name="user_name" :value="query_user_name">
          <input type="hidden" name="phone" :value="query_phone">
          <input type="hidden" name="state" :value="query_state">
          <input type="hidden" name="begin" :value="query_begin">
          <input type="hidden" name="end" :value="query_end">
          <input type="hidden" name="dept" :value="query_dept">
        </form>
        <el-pagination :total="total" :limit="limit" />
        <el-dialog v-if="show_add" title="Add a user">
          <el-form method="post" action="/users/add">
            <input type="hidden" name="csrf" :value="csrf">
            <el-form-item label="Account">
              <el-input name="user_name" />
            </el-form-item>
            <el-form-item label="Name">
              <el-input name="nick_name" />
            </el-form-item>
            <el-form-item label="Department id">
              <el-input-number name="dept_id" />
            </el-form-item>
            <el-form-item label="Role id">
              <el-input-number name="role_id" />
            </el-form-item>
            <el-form-item label="Password">
              <el-input name="password" type="password" />
            </el-form-item>
            <el-button type="primary" class="user-btn user-btn-add">Add</el-button>
          </el-form>
        </el-dialog>
        <div v-if="show_edit" class="user-edit-float">
          <el-dialog title="Edit a user">
            <el-form method="post" action="/users/edit">
              <input type="hidden" name="csrf" :value="csrf">
              <input type="hidden" name="user_id" :value="edit_user_id">
              <input type="hidden" name="form" value="edit">
              <input type="hidden" name="user_name" :value="query_user_name">
              <input type="hidden" name="phone" :value="query_phone">
              <input type="hidden" name="state" :value="query_state">
              <input type="hidden" name="begin" :value="query_begin">
              <input type="hidden" name="end" :value="query_end">
              <input type="hidden" name="dept" :value="query_dept">
              <div class="user-edit-actions">
                <el-button type="primary" class="user-btn user-btn-edit">Save</el-button>
                <a class="user-btn user-btn-close" :href="edit_close_href">Close</a>
              </div>
              <h2 class="user-edit-head">Account</h2>
              <div class="user-edit-grid">
                <el-form-item label="Name">
                  <el-input name="nick_name" :value="edit_nick" />
                </el-form-item>
                <el-form-item label="Department">
                  <div class="dept-field">
                    <input type="text" class="user-readonly" readonly :value="edit_dept_name">
                    <label class="user-btn user-btn-search" for="dept-open" title="Choose a department"></label>
                  </div>
                </el-form-item>
                <el-form-item label="Phone">
                  <el-input name="phonenumber" :value="edit_phone" />
                </el-form-item>
                <el-form-item label="Email">
                  <el-input name="email" :value="edit_email" />
                </el-form-item>
                <el-form-item label="Login name">
                  <input type="text" class="user-readonly" readonly :value="edit_login">
                </el-form-item>
                <el-form-item label="Status">
                  <el-switch name="status" :value="edit_status"></el-switch>
                </el-form-item>
                <el-form-item label="Job title">
                  <div class="job-select">
                    <input type="hidden" name="job_title_id" value="">
                    <input class="job-open" id="job-open" type="checkbox">
                    <label class="job-caret" for="job-open"></label>
                    <div class="job-menu">
                      <label v-for="job in job_titles" class="job-row">
                        <input class="job-check" type="checkbox" name="job_title_id" :value="job.job_title_id" :checked="job.checked">
                        <span class="job-tag">{{ job.job_title }}</span>
                      </label>
                    </div>
                  </div>
                </el-form-item>
                <el-form-item label="Sex">
                  <select name="sex">
                    <option value="0" :selected="sex_male">Male</option>
                    <option value="1" :selected="sex_female">Female</option>
                    <option value="2" :selected="sex_unknown">Unknown</option>
                  </select>
                </el-form-item>
                <div class="user-edit-span">
                  <el-form-item label="Role">
                    <input type="hidden" name="role_id" value="">
                    <label v-for="role in edit_roles" class="user-check">
                      <input type="checkbox" name="role_id" :value="role.role_id" :checked="role.checked" :disabled="role.locked">
                      {{ role.role_name }}
                    </label>
                  </el-form-item>
                </div>
              </div>
              <div class="user-edit-wide">
                <el-form-item label="Remark">
                  <textarea name="remark">{{ edit_remark }}</textarea>
                </el-form-item>
              </div>
              <input class="dept-open" id="dept-open" type="checkbox" :checked="picker_dept">
              <div class="dept-float">
                <div class="dept-sheet">
                  <p>Choose a department</p>
                  <label>Keyword <input type="text" name="dept_q" :value="dept_q"></label>
                  <button type="submit" class="user-btn user-btn-search" name="picker" value="dept" formmethod="get" formaction="/users">Search</button>
                  <ul class="user-tree">
                    <dept-choice v-for="dept in edit_departments"></dept-choice>
                  </ul>
                  <label class="user-btn" for="dept-open">Confirm</label>
                  <label class="dept-clear"><input type="radio" name="dept_id" value="" :checked="dept_cleared">Clear</label>
                  <label class="user-btn user-btn-close" for="dept-open">Close</label>
                </div>
              </div>
            </el-form>
          </el-dialog>
        </div>
        <el-dialog v-if="show_reset" title="Reset a password">
          <el-form method="post" action="/users/reset">
            <input type="hidden" name="csrf" :value="csrf">
            <input type="hidden" name="user_id" :value="reset_user_id">
            <el-form-item label="Password">
              <el-input name="password" type="password" />
            </el-form-item>
            <el-button type="primary" class="user-btn user-btn-resetpwd">Reset</el-button>
          </el-form>
        </el-dialog>
        <el-dialog v-if="show_remove" title="Remove a user">
          <el-form method="post" action="/users/remove">
            <input type="hidden" name="csrf" :value="csrf">
            <input type="hidden" name="user_id" :value="remove_user_id">
            <p>{{ remove_name }}</p>
            <el-button type="primary" class="user-btn user-btn-remove">Remove</el-button>
          </el-form>
        </el-dialog>
        <el-dialog v-if="show_import" title="Import users">
          <el-form method="post" action="/users/import" enctype="multipart/form-data">
            <input type="hidden" name="csrf" :value="csrf">
            <el-form-item label="File">
              <input type="file" name="file" accept=".csv">
            </el-form-item>
            <label class="user-check">
              <input type="checkbox" name="update_support" value="1">
              Update accounts that already exist
            </label>
            <p>Columns: user_name, nick_name, dept_id, role_id. Optional: password, phonenumber, status.</p>
            <a v-if="can_export" class="user-btn user-btn-export" :href="export_href">Export</a>
            <el-button type="primary" class="user-btn user-btn-import">Import</el-button>
          </el-form>
        </el-dialog>
      </div>
    </div>
  </shell>
</template>
