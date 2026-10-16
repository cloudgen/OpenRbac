<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="toolbar">Departments</div>
    <el-table :data="rows">
      <el-table-column prop="dept_id" label="dept_id" />
      <el-table-column prop="parent_id" label="parent_id" />
      <el-table-column prop="dept_name" label="dept_name" />
      <el-table-column prop="ancestors" label="ancestors" />
      <el-table-column prop="status" label="status" />
    </el-table>
    <el-pagination :total="total" />
    <el-dialog v-if="can_add" title="Add a department">
      <el-form method="post" action="/depts/add">
        <input type="hidden" name="csrf" :value="csrf">
        <el-form-item label="Name">
          <el-input name="dept_name" />
        </el-form-item>
        <el-form-item label="Parent">
          <el-tree-select name="parent_id" :data="parents" node-key="dept_id" label-key="dept_name" />
        </el-form-item>
        <el-button type="primary">Add</el-button>
      </el-form>
    </el-dialog>
  </shell>
</template>
