<template>
  <li :class="dept.depth_class">
    <span class="user-switch"></span><label :class="dept.link_class"><input type="radio" name="dept_id" :value="dept.dept_id" :checked="dept.checked"><span class="user-node-icon"></span>{{ dept.dept_name }}</label>
    <ul>
      <dept-choice v-for="dept in dept.children"></dept-choice>
    </ul>
  </li>
</template>
