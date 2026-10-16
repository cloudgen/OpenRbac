<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="menu-page">
      <form class="menu-search" method="get" action="/menus">
        <label>Menu name <input type="text" name="menu_name" :value="query_menu_name"></label>
        <label>Status
          <select v-if="state_all" name="state">
            <option value="" selected>All</option>
            <option value="0">Show</option>
            <option value="1">Hide</option>
          </select>
          <select v-if="state_show" name="state">
            <option value="">All</option>
            <option value="0" selected>Show</option>
            <option value="1">Hide</option>
          </select>
          <select v-if="state_hide" name="state">
            <option value="">All</option>
            <option value="0">Show</option>
            <option value="1" selected>Hide</option>
          </select>
        </label>
        <input v-if="has_closed" type="hidden" name="closed" :value="query_closed">
        <button class="user-btn user-btn-search" type="submit">Search</button>
        <a class="user-btn user-btn-reset" href="/menus">Reset</a>
      </form>
      <form class="menu-work" method="get" action="/menus">
        <input type="hidden" name="menu_name" :value="query_menu_name">
        <input type="hidden" name="state" :value="query_state">
        <input v-if="has_closed" type="hidden" name="closed" :value="query_closed">
        <div class="menu-toolbar">
          <a v-if="can_add" class="user-btn menu-btn-add" :href="add_href">Add</a>
          <button v-if="can_edit" class="user-btn menu-btn-edit" type="submit" name="form" value="edit">Edit</button>
          <button v-if="can_edit" class="user-btn menu-btn-sort" type="submit" form="menu-sort">Save sort</button>
          <a class="user-btn menu-btn-fold" :href="fold_href">Expand/Collapse</a>
        </div>
        <el-table :data="rows">
          <el-table-column v-if="can_choose">
            <template #header>
              <input class="table-check" type="checkbox" aria-label="check all">
            </template>
            <input class="table-check" type="checkbox" name="menu_id" aria-label="Select row" :value="row.menu_id">
          </el-table-column>
          <el-table-column label="Menu name">
            <span :class="row.name_class"><a :class="row.twist_class" :href="row.toggle_href"></a><span :class="row.icon_class"></span>{{ row.menu_name }}</span>
          </el-table-column>
          <el-table-column label="Sort">
            <input v-if="can_edit" class="menu-sort" type="text" name="order_num" form="menu-sort" :value="row.order_num">
            <input v-else class="menu-sort" type="text" readonly :value="row.order_num">
            <input v-if="can_edit" type="hidden" name="menu_id" form="menu-sort" :value="row.menu_id">
          </el-table-column>
          <el-table-column prop="request_path" label="Path" />
          <el-table-column label="Type">
            <span :class="row.type_class">{{ row.type_label }}</span>
          </el-table-column>
          <el-table-column label="Visible">
            <span :class="row.visible_class">{{ row.visible_label }}</span>
          </el-table-column>
          <el-table-column prop="perms_label" label="Permission" />
          <el-table-column v-if="can_act" label="Action">
            <a v-if="can_edit" class="user-btn user-btn-edit" :href="row.edit_href">Edit</a>
            <a v-if="can_add" class="user-btn user-btn-add" :href="row.add_href">Add</a>
            <a v-if="can_remove" class="user-btn user-btn-remove" :href="row.remove_href">Remove</a>
          </el-table-column>
        </el-table>
      </form>
      <form v-if="can_edit" id="menu-sort" method="post" action="/menus/sort">
        <input type="hidden" name="csrf" :value="csrf">
        <input type="hidden" name="keep_name" :value="query_menu_name">
        <input type="hidden" name="keep_state" :value="query_state">
        <input v-if="has_closed" type="hidden" name="keep_closed" :value="query_closed">
      </form>
      <el-pagination :total="total" />
      <el-dialog v-if="show_add" title="Add a menu">
        <el-form method="post" action="/menus/add">
          <input type="hidden" name="csrf" :value="csrf">
          <input type="hidden" name="keep_name" :value="query_menu_name">
          <input type="hidden" name="keep_state" :value="query_state">
          <input v-if="has_closed" type="hidden" name="keep_closed" :value="query_closed">
          <el-form-item label="Name">
            <el-input name="menu_name" />
          </el-form-item>
          <el-form-item label="Parent">
            <el-tree-select name="parent_id" :data="parents" :value="parent_id" node-key="menu_id" label-key="menu_name" />
          </el-form-item>
          <el-form-item label="Type">
            <el-radio-group name="menu_type">
              <el-radio value="M">Directory</el-radio>
              <el-radio value="C">Menu</el-radio>
              <el-radio value="F">Button</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="Permission">
            <el-input name="perms" />
          </el-form-item>
          <el-form-item label="Path">
            <el-input name="path" />
          </el-form-item>
          <el-button type="primary" class="user-btn menu-btn-add">Add</el-button>
        </el-form>
      </el-dialog>
      <el-dialog v-if="show_edit" title="Edit a menu">
        <el-form method="post" action="/menus/edit">
          <input type="hidden" name="csrf" :value="csrf">
          <input type="hidden" name="menu_id" :value="edit_menu_id">
          <input type="hidden" name="keep_name" :value="query_menu_name">
          <input type="hidden" name="keep_state" :value="query_state">
          <input v-if="has_closed" type="hidden" name="keep_closed" :value="query_closed">
          <el-form-item label="Name">
            <el-input name="menu_name" :value="edit_name" />
          </el-form-item>
          <el-form-item label="Parent">
            <el-tree-select name="parent_id" :data="parents" :value="edit_parent" node-key="menu_id" label-key="menu_name" />
          </el-form-item>
          <el-form-item label="Type">
            <el-radio-group name="menu_type" :value="edit_type">
              <el-radio value="M">Directory</el-radio>
              <el-radio value="C">Menu</el-radio>
              <el-radio value="F">Button</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="Visible">
            <el-radio-group name="visible" :value="edit_visible">
              <el-radio value="0">Show</el-radio>
              <el-radio value="1">Hide</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="Permission">
            <el-input name="perms" :value="edit_perms" />
          </el-form-item>
          <el-form-item label="Path">
            <el-input name="path" :value="edit_path" />
          </el-form-item>
          <el-button type="primary" class="user-btn menu-btn-edit">Edit</el-button>
        </el-form>
      </el-dialog>
      <el-dialog v-if="show_remove" title="Remove a menu">
        <el-form method="post" action="/menus/remove">
          <input type="hidden" name="csrf" :value="csrf">
          <input type="hidden" name="menu_id" :value="remove_menu_id">
          <input type="hidden" name="keep_name" :value="query_menu_name">
          <input type="hidden" name="keep_state" :value="query_state">
          <input v-if="has_closed" type="hidden" name="keep_closed" :value="query_closed">
          <p>{{ remove_name }}</p>
          <el-button type="primary" class="user-btn user-btn-remove">Remove</el-button>
        </el-form>
      </el-dialog>
    </div>
  </shell>
</template>
