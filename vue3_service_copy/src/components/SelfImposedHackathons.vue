<template>
  <div>
    <h2>List of Titles</h2>
    <ul>
      <li v-for="title in titles" :key="title.id" @click="toggleInfo(title.id)">
        {{ title.name }}
        <div v-if="expandedItem === title.id">
          <p>{{ title.description }}</p>
          <p>Additional information: {{ title.additionalInfo }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      titles: [
        { id: 1, name: 'Title 1', description: 'Description 1', additionalInfo: 'Info 1' },
        { id: 2, name: 'Title 2', description: 'Description 2', additionalInfo: 'Info 2' },
        { id: 3, name: 'Title 3', description: 'Description 3', additionalInfo: 'Info 3' }
      ],
      expandedItem: null
    };
  },
  methods: {
    toggleInfo(itemId) {
      this.expandedItem = this.expandedItem === itemId ? null : itemId;
    }
  }
};
</script>

<style scoped>
li {
  cursor: pointer;
  padding: 10px;
  margin-bottom: 5px;
  background-color: #eee;
  border-radius: 5px;
}
li:hover {
  background-color: #ddd;
}
div[aria-expanded="true"] {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
}
</style>

