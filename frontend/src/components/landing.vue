<template>
  <div style="padding: 30px">
    <p class="text-center" style="color: white">Please Use a link you were provided with instead of direct access, or connect your wallet if you are an administrator.</p>
  </div>
</template>

<script>

export default {
  name: "landing",
  computed: {
    user() {
      return this.$store.state.user.user
    }
  },
  watch: {
    user: {
      handler() {
        if (this.user.wallet) {
          if (this.user.is_super_admin) {
            console.log("User is superadmin, redirect", this.user)
            this.$router.push({name: 'superadmin'})
          } else if (this.user.organizations.length) {
            this.$router.push({name: 'dashboard'})
          } else {
            this.$router.push({name: 'wallets'})
          }
        }
      },
      immediate: true
    }
  }
}
</script>

<style scoped>

</style>