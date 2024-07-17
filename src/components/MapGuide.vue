<template>
    <div v-show="store.mode == 'guide'" id="info">
        <div class="guide-header">ガイド<button @click="store.mode = 'menu'"><img :src="close" /></button></div>
        <div class="guide-contents">
            <h2>操作のしかた</h2>
            <ul>
                <li class="guide-item"><strong>地域の詳細を見る</strong><br>見たい場所を左クリック／タップ</li>
                <li class="guide-item"><strong>地図を移動する</strong><br>メイン画面を左ドラッグ／スワイプ</li>
                <li class="guide-item"><strong>拡大／縮小する</strong><br>マウスホイールを回す／二本指で広げる・狭める</li>
                <li class="guide-item"><strong>回転させる</strong><br>右ドラッグがCtrlキー＋左ドラッグで<br>左右移動／二本指で回転</li>
                <li class="guide-item"><strong>傾きを変化させる</strong><br>右ドラッグがCtrlキー＋左ドラッグで<br>上下移動／二本指で上下移動</li>
                <li class="guide-item"><strong>北が上に向きを戻す</strong><br>左下のコンパスボタン<img :src="compass">を押す</li>
                <li class="guide-item"><strong>現在位置を取得</strong><br>左下の現在位置ボタン<img :src="locate">を押す
                </li>
                <li class="guide-item"><strong>検索した場所に移動する</strong><br>検索入力フォームをクリック／タップして入力し検索</li>
            </ul>
            <h2>このWebサイトについて</h2>
            「まちラボ3D横浜」は、神奈川県横浜市の市内における都市計画を学ぶことができる3Dのマップです。<br>
            第1弾として用途地域を3Dで調べるマップを提供しています。
            <h3>用途地域とは？</h3>

            <blockquote>
                <div>「用途地域」とは、土地利用の目的に応じて13種類に分かれた地域のことで、建築できる用途や規模などに関する一定のルールを定めたものです。</div>
                <div class="quote-source">出典:<a
                        href="https://www.city.yokohama.lg.jp/business/bunyabetsu/kenchiku/toshikeikaku/tetsuduki/youto/youtominaoshi.html">横浜市</a>
                </div>
            </blockquote>

            このうち横浜市内には12種類の用途地域と市街化調整区域が定められています。
        </div>
    </div>
</template>
<script setup lang="ts">
import { onMounted } from 'vue';
import { useMapStore } from '../store/mapStore';
import close from '../assets/x.svg';
import compass from '../assets/compass.svg';
import locate from '../assets/geolocate.svg';
const store = useMapStore();

onMounted(() => {
    document.addEventListener('click', (event) => {
        const target = event.target as HTMLElement;
        if (target.closest('#guide-menu')) {
            let mode: string;
            if (store.mode === 'guide') {
                mode = 'menu';
            } else {
                mode = 'guide';
            }
            store.mode = mode;
        } else if (!target.closest('#info') && !target.closest('#guide-menu')) {
            if (store.mode == 'guide') {
                store.mode = 'menu';
            }
        }


    });
});

</script>
<style scoped>
#info {
    position: fixed;
    top: 45.5%;
    left: 50%;
    width: 550px;
    transform: translate(-50%, -50%);
    z-index: 9999;
    background: #fff;
    border-radius: 4px;
    color: #333;
    box-shadow: 0 0 0 2px rgba(0, 0, 0, .1);

}

.guide-contents {
    overflow-y: scroll;
    max-height: calc(100vh - 24.5rem);
    max-height: calc(100dvh - 24.5rem);
    padding: 18px;
    min-height: 160px;
}

@media screen and (max-width: 600px) {
    #info {
        left: 10%;
        width: auto;
        transform: translate(-5%, -50%);
    }
}

.guide-header {
    font-size: 24px;
    color: #333;
    font-weight: bold;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-left: 2.5rem;
    border-bottom: #ccc 1px solid;
}

.guide-header button {
    background-color: transparent;
    border: 0;
    width: 48px;
    height: 48px;
    margin-right: 0;
    cursor: pointer;
}

.guide-header button img {
    margin-bottom: -4px;
    opacity: 0.5;
}

.guide-header button:hover {
    background-color: rgb(0 0 0 / 5%);
}

.guide-contents {
    color: #333;
    padding-top: 0;
    line-height: 2;
}

.guide-contents {
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    padding-bottom: 4rem;
}


.guide-contents ul {
    margin-left: -1rem;
    padding-bottom: 2rem;
}

.guide-contents li::marker {
    color: #00479B;
}

.guide-contents h2 {
    border-bottom: #6296dd 1px solid;
    line-height: 2.5rem;
}

.guide-item {
    line-height: 2em;
    margin: 14px 28px 0px 0;

}

.guide-item img {
    margin-bottom: -8px;
    opacity: 0.75;
}

.guide-contents blockquote {

    margin-left: 1em;

}

.quote-source {
    text-align: right;
}


.guide-contents {

    background: linear-gradient(white 30%, transparent),
        linear-gradient(transparent, white 70%) 0 100%,
        linear-gradient(rgba(0, 32, 64, 0.1) 5%, transparent),
        linear-gradient(transparent, rgba(0, 32, 64, 0.15) 95%) 0 100%;

    background-size: 100% 50px, 100% 50px, 100% 20px, 100% 20px;
    background-repeat: no-repeat;
    background-color: white;
    background-attachment: local, local, scroll, scroll;
}
</style>