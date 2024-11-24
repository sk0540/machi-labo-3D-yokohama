import { defineStore } from 'pinia';

//表示するメニューの遷移をPiniaで行う
//文字列で切り替え
//'guide':ガイド
//'menu':地図を表示
//'legend':凡例
//'search':検索
//todo:切り替え可能なモードをリストとして登録
export const useMapStore = defineStore('map', {
    state: () => ({
        mode: 'guide',//初期モード
        searchGuide: true,//ガイドがあるかの検索（未使用）
    }),
    actions: {
        toggleMode(newMode: string) {
            this.mode = newMode;
        },//関数によるモードの切替（未使用）
    },
});