<template>
    <div>
      <h1>Game List</h1>
      <ul>
        <li v-for="game in games" :key="game.id">
          <router-link :to="'/games/' + game.id">{{ game.name }}</router-link>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        games: [],
      };
    },
    created() {
      axios.get('games/')
        .then(response => {
          this.games = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
  };
  </script>
  