<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="toolbar">Operation log</div>
    <el-table :data="rows">
      <el-table-column prop="oper_id" label="oper_id" />
      <el-table-column prop="title" label="title" />
      <el-table-column prop="business_type" label="business_type" />
      <el-table-column prop="oper_name" label="oper_name" />
      <el-table-column prop="status" label="status" />
      <el-table-column prop="oper_time" label="oper_time" />
    </el-table>
    <el-pagination :total="total" />
  </shell>
</template>
