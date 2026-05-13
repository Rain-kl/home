import { defineStore } from "pinia";
import { getSiteConfig } from "@/api";
import { defaultSiteConfig } from "@/utils/siteConfig";

export const mainStore = defineStore("main", {
  state: () => {
    return {
      imgLoadStatus: false, // 壁纸加载状态
      innerWidth: null, // 当前窗口宽度
      coverType: "0", // 壁纸种类
      siteStartShow: false, // 建站日期显示
      backgroundShow: false, // 壁纸展示状态
      boxOpenState: false, // 盒子开启状态
      mobileOpenState: false, // 移动端开启状态
      mobileFuncState: false, // 移动端功能区开启状态
      setOpenState: false, // 设置页面开启状态
      footerBlur: true, // 底栏模糊
      siteConfig: { ...defaultSiteConfig },
      siteConfigLoaded: false,
    };
  },
  getters: {
    // 获取页面宽度
    getInnerWidth(state) {
      return state.innerWidth;
    },
    getSiteConfig(state) {
      return state.siteConfig;
    },
  },
  actions: {
    async loadSiteConfig() {
      try {
        const data = await getSiteConfig();
        this.siteConfig = {
          ...defaultSiteConfig,
          ...(data || {}),
        };
      } catch (error) {
        console.error("站点配置读取失败，使用本地默认配置", error);
        this.siteConfig = { ...defaultSiteConfig };
      } finally {
        this.siteConfigLoaded = true;
      }
    },
    // 更改当前页面宽度
    setInnerWidth(value) {
      this.innerWidth = value;
      if (value >= 720) {
        this.mobileOpenState = false;
        this.mobileFuncState = false;
      }
    },
    // 更改壁纸加载状态
    setImgLoadStatus(value) {
      this.imgLoadStatus = value;
    },
  },
  persist: {
    key: "data",
    storage: window.localStorage,
    paths: [
      "coverType",
      "siteStartShow",
      "footerBlur",
    ],
  },
});
