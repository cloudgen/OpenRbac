<template>
  <shell v-if="signed_in">
    <p v-if="message" class="error">{{ message }}</p>
    <p v-if="detail">{{ detail }}</p>
  </shell>
  <div v-else class="login">
    <h1>{{ title }}</h1>
    <p v-if="message" class="error">{{ message }}</p>
    <p v-if="detail">{{ detail }}</p>
    <p><a href="/login">Sign in</a></p>
  </div>
</template>
