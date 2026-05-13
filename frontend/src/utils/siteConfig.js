export const defaultSiteConfig = {
  siteName: import.meta.env.VITE_SITE_NAME || "無名の主页",
  siteAuthor: import.meta.env.VITE_SITE_AUTHOR || "無名",
  siteKeywords: import.meta.env.VITE_SITE_KEYWORDS || "無名,个人主页",
  siteDescription: import.meta.env.VITE_SITE_DES || "一个默默无闻的主页",
  siteUrl: import.meta.env.VITE_SITE_URL || "imsyy.top",
  siteLogo: import.meta.env.VITE_SITE_LOGO || "/images/icon/favicon.ico",
  siteMainLogo: import.meta.env.VITE_SITE_MAIN_LOGO || "/images/icon/logo.png",
  siteAppleLogo: import.meta.env.VITE_SITE_APPLE_LOGO || "/images/logo/apple-touch-icon.png",
  descHello: import.meta.env.VITE_DESC_HELLO || "Hello World !",
  descText: import.meta.env.VITE_DESC_TEXT || "一个建立于 21 世纪的小站，存活于互联网的边缘",
  descHelloOther: import.meta.env.VITE_DESC_HELLO_OTHER || "Oops !",
  descTextOther: import.meta.env.VITE_DESC_TEXT_OTHER || "哎呀，这都被你发现了（ 再点击一次可关闭 ）",
  weatherKey: import.meta.env.VITE_WEATHER_KEY || "",
  siteStart: import.meta.env.VITE_SITE_START || "2020-10-24",
  siteIcp: import.meta.env.VITE_SITE_ICP || "",
  songApi: import.meta.env.VITE_SONG_API || "https://api-meting.imsyy.top/api",
  songServer: import.meta.env.VITE_SONG_SERVER || "netease",
  songType: import.meta.env.VITE_SONG_TYPE || "playlist",
  songId: import.meta.env.VITE_SONG_ID || "",
};

export const splitSiteUrl = (url = defaultSiteConfig.siteUrl) => {
  const fallback = "imsyy.top";
  const target = url || fallback;
  const cleanUrl = target.replace(/^(https?:\/\/)/, "");
  const parts = cleanUrl.split(".");
  return parts.length >= 2 ? parts : fallback.split(".");
};

export const normalizeSiteHref = (url = defaultSiteConfig.siteUrl) => {
  if (!url) return "https://www.imsyy.top";
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    return `//${url}`;
  }
  return url;
};
