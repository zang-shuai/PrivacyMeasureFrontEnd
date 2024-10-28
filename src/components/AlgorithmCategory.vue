<template>
  <li class="mb-2">
    <button class="btn btn-toggle align-items-center rounded collapsed" :data-bs-toggle="'collapse'"
      :data-bs-target="'#' + id" aria-expanded="false">
      {{ title }}
    </button>
    <div class="collapse" :id="id">
      <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
        <slot></slot>
      </ul>
    </div>
  </li>
</template>

<script setup>
defineProps({
  title: String,
  id: String
});
</script>