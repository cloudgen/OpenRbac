<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="toolbar">Job Titles</div>
    <el-table :data="rows">
      <el-table-column prop="job_title_id" label="job_title_id" />
      <el-table-column prop="job_title_code" label="job_title_code" />
      <el-table-column prop="job_title" label="job_title" />
      <el-table-column prop="job_title_sort" label="job_title_sort" />
      <el-table-column prop="status" label="status" />
    </el-table>
    <el-pagination :total="total" />
    <el-dialog v-if="can_add" title="add a job titles">
      <el-form method="post" action="/job-titles/add">
        <input type="hidden" name="csrf" :value="csrf">
        <el-form-item label="Code">
          <el-input name="job_title_code" />
        </el-form-item>
        <el-form-item label="Name">
          <el-input name="job_title" />
        </el-form-item>
        <el-button type="primary">Add</el-button>
      </el-form>
    </el-dialog>
  </shell>
</template>
