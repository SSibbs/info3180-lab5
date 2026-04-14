<template>
  <form id="movieForm" @submit.prevent="saveMovie">
    
    <div class="form-group mb-3">
      <label>Movie Title</label>
      <input type="text" name="title" class="form-control" />
    </div>

    <div class="form-group mb-3">
      <label>Description</label>
      <textarea name="description" class="form-control"></textarea>
    </div>

    <div class="form-group mb-3">
      <label>Poster</label>
      <input type="file" name="poster" class="form-control" />
    </div>

    <button class="btn btn-primary">Submit</button>

  </form>
</template>

<script setup>
function saveMovie() {
  console.log("form submitted")
}
</script>