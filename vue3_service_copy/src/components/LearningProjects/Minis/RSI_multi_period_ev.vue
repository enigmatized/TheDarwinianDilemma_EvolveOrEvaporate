<template>
  <div class="additional-info">
  <p>Using historical data on the RSI (Relative Strength Index) indicator, I have constructed a lookup table. This lookup table includes the following information for each RSI level across 10 different time periods, focusing specifically on the AUD/USD currency pair on the Oanda forex exchange: 1)Probability of Profit: The table indicates the likelihood of a trade being profitable based on the corresponding RSI level.2) Average Profit/Loss: For each RSI level, I have calculated the average profit or loss for trades taken at that particular time period. 3)Expected Value (EV): The EV of a trade represents the projected outcome in terms of profit or loss across the 10 subsequent time periods.</p>
  </div>
</template>

<script>
export default {
  props: {
    info: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      // Component data goes here
    };
  },
  methods: {
    // Component methods go here
  }
};
</script>

<style scoped>
.additional-info {
  display: flex;
  flex-direction: column;
  /* Add any additional flexbox properties as needed */
}
</style>

