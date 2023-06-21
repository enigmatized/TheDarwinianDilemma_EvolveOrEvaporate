<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <!-- <HelloWorld msg="This should be showing, I have too much todo, and this is annoying"/> -->
  <ViewingBar />
  <!-- <TradingSignals /> -->
</template>

<script>
//import HelloWorld from './components/HelloWorld.vue'
import ViewingBar from "./components/ViewingBar.vue";
//import TradingSignals from "./components/TradingSignals.vue";
export default {
  name: 'App',
  components: {
    //HelloWorld,
    ViewingBar
    //TradingSignals,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
