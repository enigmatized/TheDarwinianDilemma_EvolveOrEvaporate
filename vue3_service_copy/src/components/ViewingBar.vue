<template>
  <div class="container">
	<div>
		<button v-for="button in buttons" :key="button.id" @click="handleClick(button)">
			{{ button.label }}
		</button>
	</div>	
	<div>
		<component :is="selectedComponent" v-if="selectedComponent !== null" />
	</div>
  </div>
</template>

<script>
import AboutThisProject     from "./AboutThisProject.vue";
import TradingSignals       from "./TradingSignals.vue";
import AboutMe              from "./AboutMe.vue";
import SelfImposedHackathon from "./SelfImposedHackathons.vue"

export default {
  data() {
    return {
      buttons: [
        { id: 1, label: "About This Project", component: AboutThisProject},
        { id: 2, label: "Trading Signals", component: TradingSignals},
        { id: 3, label: "Learning Projects", component: SelfImposedHackathon},
        { id: 4, label: "About Me", component: AboutMe},
        // Add more buttons as needed
      ],
      selectedComponent: null,
    };
  },
  methods: {
    handleClick(button) {
      // Handle button click event
      //console.log("Button clicked:", button);
      
      // Set the selected component based on the button clicked
      this.selectedComponent = button.component;
    },
  },
};
</script>

<style scoped>

.container {
  display: flex;
  flex-direction: column;
}

.container button {
  margin-right: 10px;
}


.buttons {
  /* Add styles for buttons container */
}

.component {
  /* Add styles for component container */
}

</style>

