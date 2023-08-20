<script>

export default{
  name: 'Query',

  data(){
    return{
        queryValue : "",
        data: [],
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
        this.data = [q, ...this.data];
        this.isSearching = false;
        })
    },

    resetHistory: function(){
      const path = 'http://127.0.0.1:8000/history/' + this.current_chat + '/reset/';
      this.axios.get(path).then((response) => {
          if(response.data.success == 200){
            this.data = [];
          }
        })

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
          <Button label="Reset History" icon="pi pi-undo" @click="resetHistory"/>
        </div>

        <div>
          <Card>
            <template #title> Response </template>
            <template #content>
              <ProgressSpinner v-if="isSearching" style="width: 30px; height: 30px" strokeWidth="3"
              animationDuration=".5s" aria-label="Custom ProgressSpinner" />

              <li v-for="(item, index) in data">
                <span>🤖</span>
                {{ item.query }} - {{ item.response }}
              </li>
            </template>
          </Card>
        </div>

    </div>
  </main>

</template>
