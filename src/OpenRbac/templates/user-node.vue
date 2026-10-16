<template>
  <li :class="dept.depth_class">
    <span class="user-switch"></span><a :href="dept.href" :class="dept.link_class"><span class="user-node-icon"></span>{{ dept.dept_name }}</a>
    <ul>
      <user-node v-for="dept in dept.children"></user-node>
    </ul>
  </li>
</template>
