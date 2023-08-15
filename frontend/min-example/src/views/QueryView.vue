<script>

export default{
  name: 'Query',

  data(){
    return{
        queryValue : "",
        data: [],
        activeClass: "pi pi-search",
        searchingClass: "pi pi-spin pi-spinner",
        isSearching: false,
    }
  },

  methods: {

    onEnter: function() {

        console.log("Query: ", this.queryValue);
        const q = {query: this.queryValue,
                    response: ""};

        const path = 'http://127.0.0.1:8000/query/?q='+this.queryValue;
        this.isSearching = true;
        this.queryValue = "";

        this.axios.get(path).then((response) => {
        console.log(response.data[0]);
        q['response'] = response.data[0]
        this.data.push(q);
        this.isSearching = false;
        })
    }

  },

}

</script>

<template>
  <main>
    <h1>Ask a question:</h1>

    <div>
        <span class="p-input-icon-right">
            <i :class="[!isSearching ? activeClass : searchingClass]" />
            <InputText type="text" placeholder="edit me" v-model="queryValue" v-on:keyup.enter="onEnter"/>
        </span>

      <Card>
        <template #title> Response </template>
        <template #content>
          <li v-for="(item, index) in data">
            {{ item.query }} - {{ item.response }}
          </li>
        </template>
      </Card>
    </div>
  </main>

</template>
