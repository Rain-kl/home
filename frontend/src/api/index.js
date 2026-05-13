const HOME_API_PREFIX = import.meta.env.VITE_API_BASE_URL || "/api";

const request = async (url, options = {}) => {
  const res = await fetch(`${HOME_API_PREFIX}${url}`, {
    credentials: "include",
    ...options,
    headers: {
      ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...options.headers,
    },
  });
  const data = await res.json();
  if (data.code !== 200) {
    throw new Error(data.msg || "请求失败");
  }
  return data.data;
};

export const getSiteLinks = () => request("/pub/site-links");

export const getSiteConfig = () => request("/pub/site-config");

export const getAdminSiteLinks = () => request("/cms/site-links");

export const getAdminSiteConfig = () => request("/cms/site-config");

export const saveAdminSiteConfig = (configs) =>
  request("/cms/site-config", {
    method: "POST",
    body: JSON.stringify({ configs }),
  });

export const saveAdminSiteLinks = (links) =>
  request("/cms/site-links", {
    method: "POST",
    body: JSON.stringify(links),
  });

export const loginAdmin = (username, password) =>
  request("/oms/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username, password }),
  });

export const getAdminInfo = () => request("/oms/auth/info");

export const logoutAdmin = () =>
  request("/oms/auth/logout", {
    method: "POST",
  });

/**
 * 一言
 */

// 获取一言数据
export const getHitokoto = async () => {
  const res = await fetch("https://v1.hitokoto.cn");
  return await res.json();
};

/**
 * 天气
 */

// 获取高德地理位置信息
export const getAdcode = async (key) => {
  const res = await fetch(`https://restapi.amap.com/v3/ip?key=${key}`);
  return await res.json();
};

// 获取高德地理天气信息
export const getWeather = async (key, city) => {
  const res = await fetch(
    `https://restapi.amap.com/v3/weather/weatherInfo?key=${key}&city=${city}`,
  );
  return await res.json();
};

// 获取教书先生天气 API
// https://api.oioweb.cn/doc/weather/GetWeather
export const getOtherWeather = async () => {
  const res = await fetch("https://api.oioweb.cn/api/weather/GetWeather");
  return await res.json();
};
