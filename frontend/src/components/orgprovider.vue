<template>
<div class="col-xl-12 p-t-10 text-right">
  <p>Select Organization</p>
  <select class="button btn btn-secondary" v-model="selectedOrg">
    <option :key="org.id" :value="org" v-for="org in organizations">{{org.name}}</option>
  </select>
  <slot :organization="selectedOrg"></slot>
</div>
</template>

<script>

export default {
  name: "orgprovider",
  props: ['value'],
  data() {
    return {
      selectedOrg: null,
      organizations: [],
    }
  },
  computed: {
    user() {
      return this.$store.state.user.user
    }
  },

  watch: {
    user: {
      handler() {
        if (this.user.wallet) {
          this.organizations = this.user.organizations;
          this.selectedOrg = this.organizations[0];
          this.$emit('input', this.selectedOrg);
        }
      },
      immediate: true
    },
    selectedOrg() {
      this.$emit('input', this.selectedOrg);
    }
  },
}
</script>

<style scoped>

</style>