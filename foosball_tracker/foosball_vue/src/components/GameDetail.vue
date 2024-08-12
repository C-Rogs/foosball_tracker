<template>
    <div class="game-detail">
      <h2>Game Detail</h2>
      <div v-if="game">
        <h3>{{ game.name }}</h3>
        <p><strong>Players:</strong> {{ game.left_offense.name }} & {{ game.left_defense.name }} vs {{ game.right_offense.name }} & {{ game.right_defense.name }}</p>
        <p><strong>Score:</strong> {{ game.left_score }} - {{ game.right_score }}</p>
        <p><strong>Status:</strong> {{ game.status }}</p>
      </div>
      <div v-else>
        <p>Loading game details...</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'GameDetail',
    data() {
      return {
        game: null,
      };
    },
    created() {
      const gameId = this.$route.params.id;
      axios.get(`games/${gameId}/`)
        .then(response => {
          this.game = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching the game details:', error);
        });
    },
  };
  </script>
  
  <style scoped>
  .game-detail {
    padding: 20px;
  }
  
  h3 {
    color: #2c3e50;
  }
  </style>
  