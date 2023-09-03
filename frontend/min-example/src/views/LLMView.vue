<script>

export default {
    name: 'LLMView',

    data() {
        return {
            currentLLM: '',
            activeClass: "pi pi-search",
            searchingClass: "pi pi-spin pi-spinner",
            isLoading: false,
            model_id: '',
        }
    },

    methods: {
        getCurrentLLM: function () {
            const path = 'http://127.0.0.1:8000/query/llm/';
            this.axios.get(path).then((response) => {
                if (response.data.success == 200) {
                    this.currentLLM = response.data.model_id;
                    this.model_id = this.currentLLM;
                }
            })

        },

        onEnter: function () {
            const path = 'http://127.0.0.1:8000/query/llm/'
            const query_data = {
                model_id: this.model_id,
            }

            this.isLoading = true;

            this.axios.post(path, query_data).then((response) => {
                this.isLoading = false;
                if (response.data.success == 200) {
                    this.currentLLM = query_data.model_id;
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Model Load Completed', life: 3000 });
                }
                else {
                    this.$toast.add({ severity: 'danger', summary: 'Failure', detail: 'Model Load Failed: ' + response.data.message, life: 10000 });
                    console.log(response.data.message);
                }
            })
        },

    },

    mounted() {
        this.getCurrentLLM();
    },

}

</script>

<template>
    <main>
        <h1>Currently used llm: {{ currentLLM }}</h1>

        <label for="model_id_input">Model Huggingface Id:</label>
        <span class="p-input-icon-right">
            <i :class="[!isLoading ? activeClass : searchingClass]" />
            <InputText id="model_id_input" type="text" style="width: 500px;" placeholder="" v-model="model_id"
                v-on:keyup.enter="onEnter" />
        </span>

        <div>
            <br>
            <Button label="Load LLM" icon="pi pi-check" @click="onEnter" />
        </div>

        <br>
        <ProgressSpinner v-if="isLoading" style="width: 30px; height: 30px" strokeWidth="3" animationDuration=".5s"
            aria-label="Custom ProgressSpinner" />

        <Toast />

    </main>
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