<template>
    <div class="home">
      <h1>Welcome to the Foosball Tracker</h1>
      <p>This is the Vue.js frontend, providing a modern interface to track your foosball games.</p>
      <router-link to="/games">View Games</router-link>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Home',
  };
  </script>
  
  <style scoped>
  .home {
    text-align: center;
    padding: 20px;
  }
  
  h1 {
    color: #2c3e50;
  }
  </style>
  