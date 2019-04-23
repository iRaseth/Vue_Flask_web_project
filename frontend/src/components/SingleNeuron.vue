<template lang="html">
  <div>
    <div class="row">
      <div class="col-xs-2">

      </div>
      <div class="col-xs-8">
        <h4> Train the neuron to get correct weights : </h4>
      </div>
      <div class="col-xs-2">
        <span class='glyphicon glyphicon-info-sign' @click="config.showModalInfo = true"></span>
      </div>
    </div>
    <div class="row input-row">
      <div class="col-xs-4">
        <label for='x1'>Input x1</label>
      </div>
      <div class="col-xs-2">
        <input name='x1' v-model="neuronJSON.x1">
      </div>
    </div>
    <div class="row input-row">
      <div class="col-xs-4">
        <label for='x2'>Input x2</label>
      </div>
      <div class="col-xs-2">
        <input name='x2' v-model="neuronJSON.x2">
      </div>
    </div>
    <div class="row input-row">
      <div class="col-xs-6">
        <label for='iterator'>Iterator</label>
        <select name="iterator" v-model="neuronJSON.iterator">
          <option v-for="value in neuronData.iterations"
                  > {{ value }} </option>
        </select>
      </div>
      <div class="col-xs-6">
        <label for='learning_parameter'>Learning parameter</label>
        <select name="learning_parameter" v-model="neuronJSON.learningParameter">
          <option v-for="parameter in neuronData.learningParameter"
                  v-bind:value="parameter"
                  > {{ parameter }} </option>
        </select>
      </div>
    </div>
    <div class="row input-row">
      <div class="col-xs-4">
        <label for='y'>Expected output: </label>
      </div>
      <div class="col-xs-4">
        <input name='y' v-model="neuronJSON.output">
      </div>
    </div>
    <br>
    <input style="margin:auto;" name="submit" type="submit" value="submit" @click="sendNeuron">
    <div class="col-xs-12" v-if="neuronOutput.visible">
      <h3>Learning parameters :</h3>
      <p>Output value: {{ neuronOutput.data.output }} </p>
      <p>Neuron input weights: {{ neuronOutput.data.weights }} </p>
    </div>
    <div class="col-xs-12" v-else-if="neuronOutput.empty">
      <h4 class="neuron-empty-input"> Please input data for the neuron in order to proceed. </h4>
    </div>
    <transition name="infoBox">
      <div class="modal" v-if="config.showModalInfo == true">
        <div class="modal-info">
          <div class="row">
            <div class="col-xs-8 col-xs-offset-2">
              <h4 style="text-align:center;">Informations !</h4>
            </div>
            <div class="col-xs-2">
              <span style="margin-top:8px; cursor:pointer;"
                    class="glyphicon glyphicon-remove"
                    @click="config.showModalInfo = false" ></span>
            </div>
          </div>
            <div class="col-xs-12 col-lg-6 col-md-6 col-sm-6">
              <p>The neuron is implemented <b>without activation function</b> because the example
              is shown only to present how <b>weights</b> adapt to the different circumstances.</p>
              <p>As it is only one neuron some operations are not possible for it.</p>
            </div>
            <div class="col-xs-12 col-lg-6 col-md-6 col-sm-6">
              <p>Recommendations :</p>
              <ul>
                <li>Use small input variables</li>
                <li>Use small learning parameter</li>
                <li>Use small expected output</li>
              </ul>
              <p><b>Load default input :</b></p>
              <span style="cursor:pointer;"
              class="glyphicon glyphicon-circle-arrow-down"
              @click="getDefault"></span>
            </div>
          </div>
        </div>
    </transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      config: {
        showModalInfo: false,
      },
      neuronData: {
        iterations: [5, 10, 15, 25, 50, 75, 100],
        learningParameter: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
      },
      neuronJSON: {
        x1: '',
        x2: '',
        iterator: '5',
        learningParameter: '0.1',
        output: '',
      },
      neuronOutput: {
        empty: false,
        visible: false,
        data: {

        },
      },
    };
  },
  methods: {
    sendNeuron() {
      this.$http.post('/set_single_neuron', this.neuronJSON)
        .then((response) => {
          if (response.body.output !== undefined) {
            this.neuronOutput.visible = true;
            this.neuronOutput.empty = false;
            this.neuronOutput.data = response.body;
          } else {
            this.neuronOutput.empty = true;
          }
          console.log(this.neuronOutput.data.output);
        }, (error) => {
          console.log(error);
        });
    },
    getDefault() {
      this.$http.get('/default_neuron')
        .then((response) => {
          this.neuronJSON.x1 = response.body.x1;
          this.neuronJSON.x2 = response.body.x2;
          this.neuronJSON.iterator = response.body.iterator;
          this.neuronJSON.learningParameter = response.body.learning_parameter;
          this.neuronJSON.output = response.body.expected_output;
        }, (error) => {
          console.log(error);
        });
      this.config.showModalInfo = false;
    },
  },
};
</script>

<style lang="css" scoped>
.input-row{
    margin-bottom:15px;
    text-align: left;
}
.neuron-empty-input{
  color:red;
  font-weight: 700;
  letter-spacing: 1px;
}
.glyphicon{
  font-size:20px;
}
.glyphicon-info-sign{
  cursor:pointer;
}
/* INFO BOX */
.infoBox-enter{
  opacity:0;
}
.infoBox-enter-active{
  transition: opacity 350ms ease-in;
}
.infoBox-leave{

}
.infoBox-leave-active{
  opacity:0;
  transition: opacity 350ms ease-in;
}
.modal{
  top:0;
  left:0;
  width:100%;
  height:400px;
  z-index:9999;
  position:absolute;
  display: block;
  background-color: rgba(120,120,120,0.7);
}
.modal-info{
  top:25%;
  left:0;
  width:100%;
  height:200px;
  display:block;
  position:relative;
  background-color: rgb(120,120,120);
  color:white;
}
</style>
