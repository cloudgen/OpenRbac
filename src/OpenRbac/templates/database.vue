<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="toolbar">Database</div>
    <p>{{ sentence }} The next sign-in uses the saved engine. Changing it signs this browser out, because the session row stays in the previous database.</p>
    <el-form method="post" action="/database">
      <input type="hidden" name="csrf" :value="csrf">
      <fieldset>
        <legend>Database</legend>
        <el-radio-group v-model="engine">
          <el-radio value="sqlite3">{{ sqlite_label }}</el-radio>
          <el-radio value="mysql">{{ mysql_label }}</el-radio>
        </el-radio-group>
      </fieldset>
      <el-button type="primary">Save</el-button>
    </el-form>
  </shell>
</template>
