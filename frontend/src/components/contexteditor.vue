<template>

  <BModal :id="`modal-${contract.context_uuid}`">
    <div class="row">
      <div class="col-12">
        <h4>Edit Token IDs</h4>
        <div v-for="token_id in contract.token_id_whitelist">
          <div>
            <code> # {{ token_id}} </code>
            <b-btn>Remove</b-btn>
          </div>
        </div>
      </div>
    </div>
  </BModal>
</template>

<script>
export default {
  name: "ContextEditor",
  props: ['contract'],
}
</script>

<style scoped>

</style>