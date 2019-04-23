<template id="">
  <div class="container">
    <div class='row'>
      <div class='col-lg-6' style="border-right: 1px solid gray;">
      <!--<form action="/send_msg" method="post">-->
        <posts v-bind:auth_user="auth_user"></posts>
      </div>
      <!--  -->
      <div class='col-lg-6'>
        <SingleNeuron></SingleNeuron>
      </div>
    </div>
  </div>
</template>
<script>
import SingleNeuron from './SingleNeuron';
import Posts from './Posts';

export default{
  data() {
    return {
      auth_user: '',
    };
  },
  components: {
    SingleNeuron,
    posts: Posts,
  },
  created: function () {
    this.$http.get('/get_id')
      .then( (response) => {
        this.auth_user = response.body;
      }, (error) => {
        console.log(response);
      });
  }
  //Write post for neuron and do backend for it !
  // Including tests
}
</script>
<style media="screen" scoped>

</style>
