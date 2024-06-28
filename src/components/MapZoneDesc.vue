<template>
    <div class="desc-title" :style="style">{{ zoneDescs[num] }}</div>
    <div v-if="showComment" class="comment">{{ zoneComments[num] }}</div>
</template>

<script setup lang="ts">
import { zoneDescs, zoneColors, zoneComments } from '../data/zoneData';

import { computed } from 'vue'
const props = defineProps({
    num: {
        type: Number,
        required: true,
    },
    display: {
        type: String,
        required: true,
    }
});

const style = computed(() => ({
    '--icon-color': zoneColors[props.num],
    'font-weight': props.display === 'detail' ? 'bold' : 'normal',
}));

const showComment = computed(() => props.display === 'detail');
</script>

<style scoped>
.desc-title {
    font-size: 15px;
    font-weight: 500;
    line-height: 1em;
}

.desc-title::before {
    content: "■";
    font-size: 30px;
    margin-right: 5px;
    vertical-align: -1px;
    color: var(--icon-color);
}

.comment {
    margin-top: 1em;
    font-weight: 400;
}
</style>