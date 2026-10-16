<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="login-page">
      <form class="user-search" method="get" action="/login-log">
        <label>Login address <input type="text" name="ipaddr" :value="query_ipaddr"></label>
        <label>Login name <input type="text" name="user_name" :value="query_user_name"></label>
        <label>Login status
          <select v-if="status_all" name="status">
            <option value="" selected>All</option>
            <option value="0">Success</option>
            <option value="1">Failed</option>
          </select>
          <select v-if="status_ok" name="status">
            <option value="">All</option>
            <option value="0" selected>Success</option>
            <option value="1">Failed</option>
          </select>
          <select v-if="status_bad" name="status">
            <option value="">All</option>
            <option value="0">Success</option>
            <option value="1" selected>Failed</option>
          </select>
        </label>
        <date-range>Login time </date-range>
        <button class="user-btn user-btn-search" type="submit">Search</button>
        <a class="user-btn user-btn-reset" href="/login-log">Reset</a>
      </form>
      <el-table :data="rows">
        <el-table-column prop="info_id" label="Access id" />
        <el-table-column prop="user_name" label="Login name" />
        <el-table-column prop="ipaddr" label="Login address" />
        <el-table-column prop="login_location" label="Login location" />
        <el-table-column prop="browser" label="Browser" />
        <el-table-column prop="os" label="Operating system" />
        <el-table-column label="Login status">
          <el-tag :type="row.tag_type">{{ row.status_label }}</el-tag>
        </el-table-column>
        <el-table-column prop="msg" label="Message" />
        <el-table-column prop="login_time" label="Login time" />
      </el-table>
      <p class="login-count">{{ count_line }}</p>
    </div>
  </shell>
</template>
