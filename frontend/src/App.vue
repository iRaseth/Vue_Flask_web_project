<template>
  <div id="app">
    <h1 class='app-header'> {{ header }} </h1>
    <hr>
    <router-view></router-view>
  </div>
</template>

<script>
import Home from './components/Home';
import Default from './components/Default';

export default {
  data() {
    return {
      header: 'Vue / Flask web project.',
    };
  },
  components: {
    home: Home,
    default: Default,
  },
};
</script>

<style>
body{

}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.app-header{
  font-size:25px;
  font-weight: lighter;
  letter-spacing: 3px;
}
</style>
