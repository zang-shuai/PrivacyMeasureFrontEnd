<template>
  <li>
    <a href="#" class="link-dark rounded" @click="$emit('select', formType, name)">
      {{ name }}
    </a>
  </li>
</template>

<script setup>
defineProps({
  name: String,
  formType: String
});

defineEmits(['select']);
</script>