<template>
  <div class="admlte-date-range">
    <span class="admlte-date-range-title"><slot></slot></span>
    <div class="admlte-date-range-pair">
      <div class="admlte-date-range-field">
        <input v-if="query_end" id="admlte-date-from" type="date" name="begin" :value="query_begin" :max="query_end">
        <input v-else id="admlte-date-from" type="date" name="begin" :value="query_begin">
      </div>
      <span class="admlte-date-range-arrow" aria-hidden="true">→</span>
      <div class="admlte-date-range-field">
        <input v-if="query_begin" id="admlte-date-to" type="date" name="end" :value="query_end" :min="query_begin">
        <input v-else id="admlte-date-to" type="date" name="end" :value="query_end">
      </div>
    </div>
  </div>
</template>
