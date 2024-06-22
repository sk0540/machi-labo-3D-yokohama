<template>
    <div class="desc" :style="style">{{ descs[num] }}</div>
    <div v-if="showComment" class="comment">{{ comments[num] }}</div>
</template>

<script setup lang="ts">

const descs: { [key: number]: string } = {
    1: "第一種低層住居専用地域",
    2: "第二種低層住居専用地域",
    3: "第一種中高層住居専用地域",
    4: "第二種中高層住居専用地域",
    5: "第一種住居地域",
    6: "第二種住居地域",
    7: "準住居地域",
    9: "近隣商業地域",
    10: "商業地域",
    11: "準工業地域",
    12: "工業地域",
    13: "工業専用地域",
    23: "市街化調整区域"
}

const comments: { [key: number]: string } = {
    1: "静かな戸建て住居の地域。他に学校や診療所なども可。店舗や事務所を制限。",
    2: "静かな住環境をある程度確保した地域。戸建て住居の他に小規模な店舗や飲食店も可能。",
    3: "都市化に対応しつつ住環境を重視する地域。中高層住宅の他に大学や病院なども可、店舗や事務所も一定規模まで可。",
    4: "都市機能と住環境の両立を目指す地域。中高層住居の他に商業施設やホテルなども可、工場や倉庫も一部可。",
    5: "比較的落ち着いた住環境をもつ地域。住宅の他に店舗や事務所は一定規模まで可。",
    6: "利便性の高い住環境をもつ地域。住宅の他に中規模な商業や小規模な工業なども可能。",
    7: "住居と商工業が混在する地域。商業や工業は住居への影響を考慮する必要あり。",
    9: "住宅と商業が共存する地域。住宅と店舗や診療所など生活に必要な商業施設が中心。工場や倉庫は制限有り。",
    10: "商業活動の中心を担う地域。大規模な商業施設やオフィス、娯楽施設なども可能。",
    11: "工業と住宅・商業の両立を目指す地域。工場や倉庫や研究施設などの他に一定規模の住居と店舗が可。",
    12: "工業活動の拠点となる地域。工場や倉庫や研究施設などが中心で住宅や店舗を制限。",
    13: "重工業や製造業に特化した地域。工場や倉庫や研究施設なのみで住宅や商業施設は不可。",
    23: "市街化を抑制している区域。農林漁業用の建物の建築や、一定規模以上の計画的開発に限定。"
}

import { computed } from 'vue'
const props = defineProps({
    color: {
        type: String,
        required: true,
    },
    num: {
        type: Number,
        required: true,
    },
    popupType: {
        type: String,
        required: true,
    }
});

const style = computed(() => ({
    '--icon-color': props.color,
    'font-weight': props.popupType === 'click' ? 'bold' : 'normal',
}));

const showComment = computed(() => props.popupType === 'click');
</script>

<style scoped>
.desc {
    font-size: 15px;
    font-weight: 500;
    line-height: 1em;
}

.desc::before {
    content: "■";
    font-size: 30px;
    margin-right: 5px;
    vertical-align: -1px;
    color: var(--icon-color);
}

.comment {
    margin-top: 1em;
}
</style>