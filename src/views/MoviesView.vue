<template>
  <div class="container mt-4">
    <h2>Movies</h2>

    <div class="row">
      <div class="col-md-4 mb-3" v-for="movie in movies" :key="movie.id">

        <div class="card">
          <img :src="`http://localhost:8080/api/v1/posters/${movie.poster}`" class="card-img-top" />
          

          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text">{{ movie.description }}</p>
          </div>

        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);

function fetchMovies() {
  fetch("/api/v1/movies")
    .then(res => res.json())
    .then(data => {
      movies.value = data.movies;
    });
}

onMounted(() => {
  fetchMovies();
});
</script>