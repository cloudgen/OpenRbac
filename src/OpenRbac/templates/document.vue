<template>
  <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{{ title }}</title>
      <link rel="stylesheet" href="/apex.css">
      <link rel="stylesheet" :href="theme_href">
    </head>
    <body>
      <slot></slot>
    </body>
  </html>
</template>
