<template>
  <div class="about-me">
    <h1>About Me</h1>
    <p>{{ jsonData.aboutMe }}</p>
    <!-- Add your content here -->
  </div>
</template>

<script>
import jsonData from '@/assets/aboutMe.json';

export default {
   data() {
    return {
      jsonData: null
    };
  },
  mounted() {
    this.jsonData = jsonData;
  }
}
</script>

<style scoped>
.about-me {
  /* Add your styles here */
}
</style>

