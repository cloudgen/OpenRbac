<template>
  <div class="wrapper">
    <aside class="main-sidebar sidebar-dark-primary">
      <ui-menu></ui-menu>
    </aside>
    <div class="content-wrapper">
      <header class="main-header">
        <el-breadcrumb>
          <el-breadcrumb-item>Home</el-breadcrumb-item>
          <el-breadcrumb-item>{{ title }}</el-breadcrumb-item>
        </el-breadcrumb>
        <el-dropdown>
          <span class="nav-link">{{ user_name }}</span>
          <el-dropdown-menu>
            <el-dropdown-item>
              <form method="post" action="/logout">
                <input type="hidden" name="csrf" :value="csrf">
                <el-button type="primary">Sign out</el-button>
              </form>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </header>
      <main class="content">
        <slot></slot>
      </main>
    </div>
  </div>
</template>
