<template>
    <div :id="id" :class="className">
        <slot></slot>
    </div>
</template>

<script setup>
defineProps({
    id: String,
    className: String
});
</script>