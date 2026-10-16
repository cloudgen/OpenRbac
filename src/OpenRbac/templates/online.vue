<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="online-page">
      <form class="user-search" method="get" action="/online">
        <label>Login address <input type="text" name="ipaddr" :value="query_ipaddr"></label>
        <label>Login name <input type="text" name="user_name" :value="query_user_name"></label>
        <button class="user-btn user-btn-search" type="submit">Search</button>
        <a class="user-btn user-btn-reset" href="/online">Reset</a>
      </form>
      <el-table :data="rows">
        <el-table-column prop="number" label="Number" />
        <el-table-column prop="token_prefix" label="Session" />
        <el-table-column prop="user_name" label="Login name" />
        <el-table-column prop="ipaddr" label="Host" />
        <el-table-column label="Session status">
          <el-tag type="success">Online</el-tag>
        </el-table-column>
        <el-table-column prop="login_time" label="Login time" />
        <el-table-column prop="last_access" label="Last access" />
        <el-table-column v-if="can_logout" label="Action">
          <form method="post" action="/online/logout">
            <input type="hidden" name="csrf" :value="csrf">
            <input type="hidden" name="token" :value="row.token">
            <el-button type="danger">Force logout {{ row.token_prefix }}</el-button>
          </form>
        </el-table-column>
      </el-table>
      <p class="online-count">{{ count_line }}</p>
    </div>
  </shell>
</template>
