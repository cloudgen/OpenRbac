<template>
  <div class="login">
    <h1>Sign in</h1>
    <p v-if="error" class="error">{{ error }}</p>
    <el-form method="post" action="/login">
      <fieldset>
        <legend>Database</legend>
        <el-radio-group v-model="engine">
          <el-radio value="sqlite3">{{ sqlite_label }}</el-radio>
          <el-radio value="mysql">{{ mysql_label }}</el-radio>
        </el-radio-group>
      </fieldset>
      <el-form-item label="Account">
        <el-input name="user_name" autocomplete="username" />
      </el-form-item>
      <el-form-item label="Password">
        <el-input name="password" type="password" autocomplete="current-password" />
      </el-form-item>
      <el-button type="primary" size="large">Sign in</el-button>
    </el-form>
    <p>Seeded accounts and initial passwords are in the product README. Change them after the first sign-in. This site listens on this computer only unless remote bind was explicitly allowed. sqlite3 and the default file are already selected. Change that only when you want mysql. mysql needs OPENRBAC_DB_PASSWORD.</p>
  </div>
</template>
