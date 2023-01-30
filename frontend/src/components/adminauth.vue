<template>
<div>
  <h3 v-if="!user.wallet" class="m-t-50 text-center">Please connect your wallet to prove you have access to this organization</h3>
  <h3 v-else class="m-t-50 text-center">Wallet <code>{{ user.wallet.address }}</code> does not have access to this organization. Please connect another one</h3>
  <div v-if="allowedAt.length">
    <h4 class="m-t-50 text-center">Your organizations:</h4>
    <ul class="text-center">
      <li v-for="(org, i) in allowedAt" :key="i">{{ org }}</li>
    </ul>
  </div>
</div>
</template>

<script>
export default {
  name: "AdminAuth",

  computed: {
    user() {
      return this.$store.state.user.user
    },
    allowedAt() {
      if (!this.user.wallet) {
        return [];
      }
      return this.user.organizations.map(org => org.name);
    }
  },
  methods: {

  },

  watch: {
    user: {
      handler() {
        const orgId = parseInt(this.$route.params.org_id);
        if (!this.user.wallet) {
          return;
        }
        if (this.user.organizations.find(org => org.id === orgId) !== undefined) {
          this.$router.push({name: 'dashboard'})
        }
      },
      immediate: true
    }
  },
}
</script>

<style scoped>

</style>