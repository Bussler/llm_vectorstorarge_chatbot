<script>

export default {
    name: 'VectorDbView',

    data() {
        return {
            vector_documents: [],
            vector_documents_count: 0,
            isUploading: false,
        }
    },

    methods: {
        onStartUpload: function () {
            this.isUploading = true;
        },

        onUpload: function () {
            this.isUploading = false;
            this.$toast.add({ severity: 'success', summary: 'Success', detail: 'File Upload Completed', life: 3000 });
            this.getVectorDBDocuments();
        },

        getVectorDBDocuments: function () {
            const path = 'http://127.0.0.1:8000/vectordb/documents/';
            this.axios.get(path).then((response) => {
                if (response.data.success == 200) {
                    this.vector_documents = response.data.docs;
                    this.vector_documents_count = this.vector_documents.length;
                }
            })
        },

        deleteDoc: function (filename) {
            const path = 'http://127.0.0.1:8000/vectordb/delete/';
            const query_data = {
                documents: [filename],
            }

            this.axios.post(path, query_data).then((response) => {
                if (response.data.success == 200) {
                    this.getVectorDBDocuments();
                }
            })
        },

    },

    mounted() {
        this.getVectorDBDocuments();
    },

}

</script>

<template>
    <main>

        <div>
            <FileUpload mode="basic" name="files" url="http://127.0.0.1:8000/vectordb/add/" accept=".txt" :multiple="true"
                @upload="onUpload" @before-upload="onStartUpload" :auto="true" chooseLabel="Add File" />

            <ProgressBar v-if="isUploading" mode="indeterminate" style="height: 6px"></ProgressBar>
        </div>

        <div>
            <h1>Vector DB:</h1>
            <p>Document Count: {{ vector_documents_count }}</p>

            <ul class="list">
                <li v-for="item in vector_documents">
                    <table>
                        <tr>
                            <th><span><i class="pi pi-file"></i></span></th>
                            <th><span>{{ item }}</span></th>
                            <th><Button label="Delete" icon="pi pi-minus-circle" @click="deleteDoc(item)" /></th>
                        </tr>
                    </table>
                    <hr class="!border-t-2">
                </li>
            </ul>
        </div>

        <Toast />

    </main>
</template>
