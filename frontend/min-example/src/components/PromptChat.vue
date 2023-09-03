<script>
export default {
  name: 'PromptChat',

  data() {
    return {
      queryValue: "",
      data: [[]],
      current_chat: 0,
      activeClass: "pi pi-search",
      searchingClass: "pi pi-spin pi-spinner",
      isSearching: false,
    }
  },

  methods: {

    onEnter: function () {
      const q = {
        query: this.queryValue,
        response: ""
      };

      const path = 'http://127.0.0.1:8000/query/'
      const query_data = {
        q: this.queryValue,
        use_chat: this.current_chat
      }

      this.isSearching = true;
      this.queryValue = "";

      this.axios.post(path, query_data).then((response) => {
        q['response'] = response.data[0];
        this.data[this.current_chat] = [q, ...this.data[this.current_chat]];
        this.isSearching = false;
      })
    },

    resetHistory: function () {
      const path = 'http://127.0.0.1:8000/history/' + this.current_chat + '/reset/';
      this.axios.get(path).then((response) => {
        if (response.data.success == 200) {
          this.data[this.current_chat] = [];
        }
      })

    },

    addHistory: function () {
      this.data = [...this.data, []];
      this.current_chat = this.data.length - 1;
    },

  },

  mounted() {
    const path = 'http://127.0.0.1:8000/history/';
    this.axios.get(path).then((response) => {
      var histories = [];
      for (let i = 0; i < response.data.length; i++) {
        var history = [];
        for (let j = 0; j < response.data[i].length; j++) {
          const q = {
            query: response.data[i][j][0],
            response: response.data[i][j][1]
          };
          history = [q, ...history];
        }
        histories = [...histories, history];
      }
      this.data = histories;
    })
  },

}

</script>

<template>
  <h1>Ask a question:</h1>

  <div>
    <span class="p-input-icon-right">
      <i :class="[!isSearching ? activeClass : searchingClass]" />
      <InputText type="text" style="width: 500px;" placeholder="edit me" v-model="queryValue"
        v-on:keyup.enter="onEnter" />
    </span>

    <div>
      <br>
      <Button label="Submit" icon="pi pi-check" @click="onEnter" />
      <Button label="Add History" icon="pi pi-plus" @click="addHistory" />
      <Button label="Reset History" icon="pi pi-undo" @click="resetHistory" />
    </div>

    <div>
      <Card>
        <template #title> Response </template>
        <template #content>
          <ProgressSpinner v-if="isSearching" style="width: 30px; height: 30px" strokeWidth="3" animationDuration=".5s"
            aria-label="Custom ProgressSpinner" />

          <TabView v-model:activeIndex="current_chat">
            <TabPanel v-for="(tab, index) in data" :key="index" :header="'History ' + index">
              <li v-for="(item, index_item) in tab">
                <span>🤖 </span>
                <span>{{ item.query }} - </span>
                <span>{{ item.response }}</span>
              </li>
            </TabPanel>
          </TabView>

        </template>
      </Card>
    </div>

  </div>

  <Toast />
</template>

<style>
@keyframes p-progress-spinner-color {

  100%,
  0% {
    stroke: #008744;
  }

  20% {
    stroke: #09edde;
  }

  40% {
    stroke: #d62d20;
  }

  60% {
    stroke: #ffa700;
  }

  90% {
    stroke: #0057e7;
  }
}</style>