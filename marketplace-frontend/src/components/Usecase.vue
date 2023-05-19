<template>
  <h4 style="margin-left: 20px; margin-top: 10px; font-weight: normal">
    or, click on a category to see automated workflows for that group of users
  </h4>
  <v-container class="text-center">
    <v-row justify="center">
      <v-col cols="12" sm="6" md="4">
        <a :href="downloadLink" download>
          <v-btn block rounded="lg" size="x-large">Download</v-btn>
        </a>
      </v-col>

      <v-col cols="12" sm="6" md="4">
        <input ref="fileInput" type="file" style="display: none" @change="handleFileUpload" />
        <v-btn block rounded="lg" size="x-large" @click="triggerFileUpload">Upload</v-btn>
      </v-col>
  
        <v-col cols="12" sm="6" md="4">
          <v-btn block rounded="lg" size="x-large">Real Estate</v-btn>
        </v-col>
  
        <v-col cols="12" sm="6" md="4">
          <v-btn block rounded="lg" size="x-large">Finance</v-btn>
        </v-col>
  
        <v-col cols="12" sm="6" md="4">
          <v-btn block rounded="lg" size="x-large">Science</v-btn>
        </v-col>
  
        <v-col cols="12" sm="6" md="4">
          <v-btn block rounded="lg" size="x-large">Admin</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      downloadLink: 'http://127.0.0.1:8000/download/sample.txt', // Initial link
    };
  },
  methods: {
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
    async handleFileUpload(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('file', file);

      // Replace 'http://127.0.0.1:8000' with your FastAPI server's address
      const response = await axios.post('http://127.0.0.1:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Assuming the server returns a response in the form { filename: '...' }
      this.downloadLink = `http://127.0.0.1:8000/download/${response.data.filename}`;
    },
  },
};
</script>