<template>
  <div class="about-me">
    <h1>Trading Signals</h1>
    <!-- Add your content here -->
    <!--The temperature will be: {{ temperature }} -->
    <img :src="imageSrc1" alt="Image" />
  </div>
</template>

<script>

import axios from "axios";

export default {
  // Component options
	data() {
		return {
		temperature: 0,
		precip_type: 'rain',
		precip_chance: 80,
		imageSrc1: '',
		};
	},
	async mounted() {
                await axios({ method: "GET", "url": "/temp" })
          .then(result => {

            if (this.temperature === 0 ) {this.temperature = result.data['temperature_c'];}
            //console.log("what is 5777", result.data);
          }, error => {
            console.error(error);
          });
                await axios({ method: "GET", "url": "/manyrsi",  responseType: "blob" })
          .then(result1 => {
		const reader = new FileReader();
		reader.onloadend = () => {
			this.imageSrc1 = reader.result; };
		reader.readAsDataURL(result1.data);
          }, error => {
            console.error(error);
          });
	//await axios({ method: "GET", "url": `http://44.224.32.114/precipitation?temp=${this.temperature}` })
	}

}
</script>

<style scoped>
.about-me {
  /* Add your styles here */
}
</style>

