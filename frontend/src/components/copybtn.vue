<template>
<button
    class="btn btn-primary" style="white-space: nowrap"
    @click="copyText()">
  {{ displayHTML }}
</button>
</template>

<script>
export default {
  name: "CopyBtn",
  props: {
    text: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: false
    }
  },
  data() {
    return {
      copied: false
    }
  },
  methods: {
    copyText() {
      navigator.clipboard.writeText(this.text);
      this.copied = true;
      setTimeout(() => {
        this.copied = false;
      }, 2000);
    },

  },
  computed: {
    displayHTML() {
      if (this.copied) {
        return "Copied!";
      } else {
        return this.label || "Copy";
      }
    }
  }
}
</script>

<style scoped>

</style>