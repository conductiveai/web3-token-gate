<template>
  <div class="header-logo-wrapper">
    <div class="logo-wrapper">
      <router-link to="/">

      </router-link>
    </div>
    <div class="toggle-sidebar" @click="toggle_sidebar">
      <feather
        class="status_toggle middle sidebar-toggle"
        type="align-center"
        id="sidebar-toggle"
      ></feather>
    </div>
  </div>
</template>

<script>


  export default {
    name: 'Logo',
    methods: {
      toggle_sidebar() {
        this.$store.dispatch('menu/opensidebar');
      },
    },
  };
</script>
<style scoped>
.logo-green{fill:#99f868;}
              .logo-white{fill:#FFFFFF;}
</style>
