<script setup>
import PromptChat from '@/components/PromptChat.vue'
</script>

<script>

export default {
  name: 'Query',
  components: [PromptChat],

  data() {
    return {
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
    },

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

    <PromptChat />

  </main>
</template>
