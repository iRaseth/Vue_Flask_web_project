<template>
  <div class='container'>
    <div class='row'>
      <div class='col-xs-6'>
        <button class='btn btn-custom-vue' @click='ShowRegistration'>Registration</button>
        <br>
        <button class='btn btn-custom-vue' @click='ShowLogin'>Login</button>
      </div>

        <div class='col-xs-6' v-bind:style="{ 'background-color': currentColor}">
            <div v-show='visibleLogin'>
              <h3 class="header-min">Log in to access ann panel :</h3>
                <div class="form-group form-inline">
                    <label for="username">Username :</label>
                    <input name="username" type="text" class="form-control" placeholder="Enter username" v-model="userLogin.username" autocomplete="off">
                </div>
                <div class="form-group form-inline">
                    <label for="password">Password :</label>
                    <input name="password" type="password" class="form-control" placeholder="Enter password" v-model="userLogin.password">
                </div>
                <p style="color:red; font-weight:700;">{{ disclaimer.login }}</p>
                <button type="submit" class="btn btn-info" @click="SendLoginData">Submit</button>
            </div>
            <div v-show='visibleRegistration'>
                  <h3 class="header-min">Register an account :</h3>
                    <div class="form-group form-inline">
                        <label for="username">Username :</label>
                        <input name ="username" type="text" class="form-control" placeholder="Enter username" v-model="userRegister.username" autocomplete="off">
                    </div>
                    <div class="form-group form-inline">
                        <label for="password">Password :</label>
                        <input name="password" type="password" class="form-control" placeholder="Enter password" v-model="userRegister.password">
                    </div>
                    <p style="color:red; font-weight:700;">{{ disclaimer.register }}</p>
                    <button type="submit" class="btn btn-warning" @click="SendRegisterData">Submit</button>
            </div>
        </div>
      </div>
    </div>
</template>
<script>

export default{
  data() {
    return {
      visibleLogin: false,
      visibleRegistration: true,
      currentColor: 'rgb(252, 243, 204)',
      loginColor: 'rgb(230, 255, 226)',
      registerColor: 'rgb(252, 243, 204)',
      userRegister: {
        username: '',
        password: '',
      },
      userLogin: {
        username: '',
        password: '',
      },
      disclaimer: {
        login: '',
        register: '',
      },
    };
  },
  methods: {
      ShowLogin() {
        this.visibleLogin = true;
        this.visibleRegistration = false;
        this.currentColor = this.loginColor;
      },
      ShowRegistration() {
        this.visibleLogin = false;
        this.visibleRegistration = true;
        this.currentColor = this.registerColor;
      },
      SendRegisterData() {
        this.$http.post('/register', this.userRegister)
          .then( response => {
          if (response.body == "user has been created successfuly") {
              this.$router.push('/register');
            } else {
              this.disclaimer.register = response.body;
            }
          }, error => {
            console.log('error' + error);
          });
      },
      SendLoginData() {
        this.$http.post('/login', this.userLogin)
          .then( response => {
          if (response.body == "login success") {
              this.$router.push('/default');
          } else if (response.body == "user already logged in") {
              this.$router.push('/default');
          } else {
              this.disclaimer.login = response.body;
            }
          }, error => {
            console.log('error' + error);
          });
      },
    },
    //To check if user is already logged in
    //server doesnt check input data if the user
    //remains in flask_session
  created: function() {
      this.$http.post('/login', this.userLogin)
        .then( (response) => {
          if (response.body == "user already logged in") {
            this.$router.push('/default');
          }
        }, (error) => {
          console.log('error' + error);
        });
  },
};
</script>
<style scoped>
label{
  font-size:13px;
  letter-spacing: 2px;
  font-weight: lighter;
}
.btn{
  margin-bottom:20px;
  font-size:12px;
  letter-spacing: 1px;
  font-weight: lighter;
}
.btn-custom-vue{
  margin-top:20px;
  background-color: rgb(104, 104, 104);
  color:white;
  font-weight: 700;
  padding:15px 15px 15px 15px;
  transition: 300ms all ease-in;
  width:150px;
}
.btn-custom-vue:hover{
  background-color:rgb(45, 45, 45);
}
.header-min{
  font-size:18px;
  letter-spacing: 2px;
  font-weight: lighter;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease-out;
}
</style>
