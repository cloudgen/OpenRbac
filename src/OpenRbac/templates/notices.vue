<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="toolbar">Notices</div>
    <el-table :data="rows">
      <el-table-column prop="notice_id" label="notice_id" />
      <el-table-column prop="notice_title" label="notice_title" />
      <el-table-column prop="notice_type" label="notice_type" />
      <el-table-column prop="status" label="status" />
    </el-table>
    <el-pagination :total="total" />
    <el-dialog v-if="can_add" title="Publish a notice">
      <el-form method="post" action="/notices/add">
        <input type="hidden" name="csrf" :value="csrf">
        <el-form-item label="Title">
          <el-input name="title" />
        </el-form-item>
        <el-form-item label="Type">
          <el-radio-group name="notice_type">
            <el-radio value="1">Notice</el-radio>
            <el-radio value="2">Announcement</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Content">
          <el-input name="content" />
        </el-form-item>
        <el-button type="primary">Publish</el-button>
      </el-form>
    </el-dialog>
  </shell>
</template>
