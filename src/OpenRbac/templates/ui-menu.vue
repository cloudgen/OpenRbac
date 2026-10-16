<template>
  <el-menu router :default-active="path" mode="vertical">
    <el-sub-menu v-for="group in nav_groups" :index="group.label">
      <template #title>{{ group.label }}</template>
      <el-menu-item v-for="item in group.items" :index="item.href">
        {{ item.label }}
      </el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>
