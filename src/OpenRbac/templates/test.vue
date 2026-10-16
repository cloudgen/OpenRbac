<template>
  <div class="content">
  <div class="card">
  <div class="card-body table-responsive p-0">
  <table class="table table-bordered table-striped">
  <thead>
  <tr>
    <th class="table-check-col"><input class="table-check h-4 w-4 rounded border-input" type="checkbox" aria-label="check all"></th>
    <th>User</th>
    <th data-prop="dept_name">Department</th>
    <th data-prop="phone">Phone</th>
    <th>Status</th>
    <th data-prop="created">JOINED</th>
    <th>Action</th>
  </tr>
  </thead>
  <tbody>
  <tr v-for="row in rows">
    <td class="table-check-col"><input type="checkbox" aria-label="Select row" class="table-check h-4 w-4 rounded border-input" :value="row.user_id"></td>
    <td>
      <div class="user-person">
        <span class="user-person-mark">{{ row.initials }}</span>
        <div class="min-w-0">
          <a v-if="can_edit" class="font-medium truncate hover:text-primary block" :href="row.edit_href">{{ row.nick_name }}</a>
          <span v-else class="font-medium truncate block">{{ row.nick_name }}</span>
          <div class="text-xs text-muted-foreground truncate">@{{ row.user_name }}</div>
        </div>
      </div>
    </td>
    <td>{{ row.dept_name }}</td>
    <td>{{ row.phone }}</td>
    <td>
      <el-switch :value="row.status" :label="row.status_label" :form="row.status_form" :post="row.status_post"></el-switch>
    </td>
    <td>{{ row.created }}</td>
    <td>
      <a v-if="can_edit" class="user-btn user-btn-edit" :href="row.edit_href">Edit</a>
      <a v-if="can_remove" class="user-btn user-btn-remove" :href="row.remove_href">Remove</a>
      <a v-if="can_reset" class="user-btn user-btn-resetpwd" :href="row.reset_href">Reset</a>
    </td>
  </tr>
  </tbody>
  </table>
  </div>
  </div>
  <form v-if="can_edit" v-for="row in rows" method="post" action="/users/status" :id="row.status_form">
    <input type="hidden" name="csrf" :value="csrf">
    <input type="hidden" name="user_id" :value="row.user_id">
    <input type="hidden" name="status" :value="row.status_next">
  </form>
  </div>
</template>
