<template>
    <div class="desc-title">{{ zoneDescs[num] }}</div>
    <div v-if="showComment" class="comment">{{ zoneComments[num] }}</div>
</template>

<script setup lang="ts">
import { zoneDescs, zoneColors, zoneComments } from '../data/zoneData';
import { ref } from 'vue';

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
const iconColor = ref<string>(zoneColors[props.num]);
const showComment = computed(() => props.display === "detail");

const titleWeight = computed(() => {
    return showComment.value ? 'bold' : 'normal';
});


</script>

<style scoped>
.desc-title {
    font-size: 15px;
    font-weight: v-bind(titleWeight);
    line-height: 1em;

}

.desc-title::before {
    content: "■";
    font-size: 30px;
    margin-right: 5px;
    vertical-align: -1px;
    color: v-bind(iconColor);
}

.comment {
    margin-top: 1em;
    font-weight: 400;
}
</style>