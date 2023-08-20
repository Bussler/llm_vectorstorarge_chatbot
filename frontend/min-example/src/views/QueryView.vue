<script>

export default{
  name: 'Query',

  data(){
    return{
        queryValue : "",
        data: [[]],
        current_chat : 0,
        activeClass: "pi pi-search",
        searchingClass: "pi pi-spin pi-spinner",
        isSearching: false,
    }
  },

  methods: {

    onEnter: function() {

        //console.log("Query: ", this.queryValue);
        const q = {query: this.queryValue,
                    response: ""};

        const path = 'http://127.0.0.1:8000/query/'//?q='+this.queryValue;
        const query_data = {
          q: this.queryValue,
          use_chat: this.current_chat
        }

        this.isSearching = true;
        this.queryValue = "";

        this.axios.post(path, query_data).then((response) => {
        //console.log(response.data[0]);
        q['response'] = response.data[0];
        this.data[this.current_chat] = [q, ...this.data[this.current_chat]];
        this.isSearching = false;
        })
    },

    resetHistory: function(){
      const path = 'http://127.0.0.1:8000/history/' + this.current_chat + '/reset/';
      this.axios.get(path).then((response) => {
          if(response.data.success == 200){
            this.data[this.current_chat] = [];
          }
        })

    },

    addHistory: function(){
      this.data = [...this.data, []];
      // TODO: this is buggy right now! We can set the active tab, but not get the active tab!
      this.current_chat += 1;
    },

  },

}

</script>

<template>
  <main>
    <h1>Ask a question:</h1>

    <div>
        <span class="p-input-icon-right">
            <i :class="[!isSearching ? activeClass : searchingClass]" />
            <InputText type="text" style="width: 500px;" placeholder="edit me" v-model="queryValue" v-on:keyup.enter="onEnter"/>
        </span>

        <div>
          <br>
          <Button label="Submit" icon="pi pi-check" @click="onEnter" />
          <Button label="Add History" icon="pi pi-plus" @click="addHistory" />
          <Button label="Reset History" icon="pi pi-undo" @click="resetHistory"/>
        </div>

        <div>
          <Card>
            <template #title> Response </template>
            <template #content>
              <ProgressSpinner v-if="isSearching" style="width: 30px; height: 30px" strokeWidth="3"
              animationDuration=".5s" aria-label="Custom ProgressSpinner" />

              <TabView v-bind:activeIndex="current_chat">
                <TabPanel v-for="(tab, index) in data" :key="index" @click="current_chat = index" :header="'History '+index">
                  <li v-for="(item, index_item) in tab">
                      <span>🤖</span>
                      {{ item.query }} - {{ item.response }}
                 </li>
                </TabPanel>
              </TabView>

            </template>
          </Card>
        </div>

    </div>
    
  </main>

</template>
