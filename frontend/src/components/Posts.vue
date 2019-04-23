<template>
  <div class="note-box">
    <h4> Pinup disclaimers about SNN ! </h4>
    <h5>Posts : </h5>
    <ul>
      <li class="post" v-for="post in postsJSON">
        <span style="color:white; float:left; padding-right:5px;"><b>{{ post.author }}: </b></span> {{ post.body }}
        <span class="glyphicon glyphicon-remove"
        v-if="auth_user == post.author"
        @click="deletePost(post.id, post.author)"
        style="float:right;"></span>
      </li>
    </ul>
    <label for="body"></label>
    <input name="body" type="text" v-model="post.message"></input>
    <label for="submit"></label>
    <input name="submit" type="submit" value="submit" @click="sendPost"></input>
    <p v-if="postResponse.success !== '' "
      style='font-weight: lighter; color: green; font-style: italic; '>
      {{ postResponse.success }} </p>
    <p v-if="postResponse.fail !== '' "
      style='font-weight: lighter; color: red; font-style: italic; '>
      {{ postResponse.fail }} </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      post: {
        message: '',
      },
      postResponse: {
        success: '',
        fail: '',
      },
      postsJSON: {},
    };
  },
  props: {
    auth_user: {
      type: String,
    },
  },
  methods: {
    sendPost() {
      this.$http.post('/send_msg', this.post)
        .then( (response) => {
          if (response.data == 'u have added post') {
            this.postResponse.success = response.data;
            this.postResponse.fail = '';
            setTimeout( () => {
              this.$router.go();
            }, 1500);
          } else {
            this.postResponse.fail = response.data;
            this.postResponse.success = '';
          }
        }, (error) => {
          console.log('error');
        });
    },
    deletePost(id, author) {
      this.$http.delete('/delete_post/'+id)
        .then( (response) => {
          this.$router.go();
        }, (error) => {
            console.log(response);
        });
    },
  },
  watch: {
    'postResponse.success' : function(newVal, oldVal) {
      let vm = this;
      setTimeout( () => {
        this.postResponse.success = '';
      }, 3000);
    },
    'postResponse.fail' : function(newVal, oldVal) {
      let vm = this;
      setTimeout( () => {
        this.postResponse.fail = '';
      }, 3000);
    },
  },
  mounted() {
    this.$http.get('/get_posts').
      then( (response) => {
        this.postsJSON = response.data;
      }, (error) => {
        console.log(response);
      });
  },
}
</script>

<style lang="css" scoped>
.note-box{
  height:300px;
}
.post{
text-align: left;
padding: 5px 10px 5px 10px;
margin-top:15px;
border-top-left-radius: 3px;
border-bottom-left-radius: 3px;
background-image: linear-gradient(to right, gray , white);
word-break: break-all;
word-wrap: break-word;
white-space: initial;
text-overflow: ellipsis;
}
.glyphicon{
  cursor:pointer;
  margin-left:20px;
  padding:3px 3px 3px 3px;
}
</style>
