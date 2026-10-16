<template>
  <shell>
    <p v-if="error" class="error">{{ error }}</p>
    <p>Signed in as <strong>{{ user_name }}</strong>.</p>
    <pre>{{ who }}</pre>
  </shell>
</template>
