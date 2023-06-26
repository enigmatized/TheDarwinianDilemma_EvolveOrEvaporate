<template>
  <div>
    <h2>List of Learning Projects</h2>
    <p> This is a collection of learning projects, categorized as micro, mini, medium, or long term. Mini learning projects are akin to self-imposed hackathons, where I set a goal to complete a project within a day or just a few hours. Medium/Long term maybe still in proccess and can range from a week to years. Micro on the other hand is similiar to mini, but instead of the goal being "creating a functioning product", micro are usually abouts understanding a concept or how to do something. Clicking on a project's title provides a detailed description.</p>
    <ul>
      <li v-for="title in titles" :key="title.id" @click="toggleInfo(title.id)">
        Mini  <b>{{ title.name }}</b> June 23rd 2023
        <div v-if="expandedItem === title.id">
          <!-- <p>{{ title.description }}</p>-->
          <component :is="title.component" :info="title.description" ></component>
          <p>Additional information: {{ title.additionalInfo }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>

import RSI_multi_period_ev from "./LearningProjects/Minis/RSI_multi_period_ev.vue";
const RSI_project = RSI_multi_period_ev;
export default {
  data() {
    return {
      rsi_descript: "Using historical data on the RSI (Relative Strength Index) indicator, I have constructed a lookup table. This lookup table includes the following information for each RSI level across 10 different time periods, focusing specifically on the AUD/USD currency pair on the Oanda forex exchange: 1)Probability of Profit: The table indicates the likelihood of a trade being profitable based on the corresponding RSI level.2) Average Profit/Loss: For each RSI level, I have calculated the average profit or loss for trades taken at that particular time period. 3)Expected Value (EV): The EV of a trade represents the projected outcome in terms of profit or loss across the 10 subsequent time periods.",
      titles: [
        { id: 1, name: 'Live Expected Profit of Trade Based on RSI', description: 'Using historical data on the RSI (Relative Strength Index) indicator, I have constructed a lookup table. This lookup table includes the following information for each RSI level across 10 different time periods, focusing specifically on the AUD/USD currency pair on the Oanda forex exchange: 1)Probability of Profit: The table indicates the likelihood of a trade being profitable based on the corresponding RSI level.2) Average Profit/Loss: For each RSI level, I have calculated the average profit or loss for trades taken at that particular time period. 3)Expected Value (EV): The EV of a trade represents the projected outcome in terms of profit or loss across the 10 subsequent time periods.' , additionalInfo: 'Info 1', component: RSI_project },
        { id: 2, name: 'Title 2', description: 'Description 2', additionalInfo: 'Info 2', component:RSI_project },
        { id: 3, name: 'Title 3', description: 'Description 3', additionalInfo: 'Info 3', component:RSI_project  }
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

