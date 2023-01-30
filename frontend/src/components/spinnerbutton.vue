<template>
  <b-button @click="e => $emit('click', e)" :disabled="busy">
    <b-spinner v-if="busy" small style="margin-bottom: 3px;"></b-spinner>
    <slot>

    </slot>
  </b-button>
</template>

<script>
export default {
  name: "SpinnerButton",
  props: ['busy']
}
</script>

<style scoped>

</style>