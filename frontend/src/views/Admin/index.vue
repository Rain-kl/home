<template>
  <main class="admin-page">
    <section v-if="!isLogin" class="login-shell">
      <div class="login-panel">
        <div class="brand">Home Admin</div>
        <el-form class="login-form" :model="loginForm" @submit.prevent>
          <el-form-item>
            <el-input v-model="loginForm.username" placeholder="用户名" size="large" />
          </el-form-item>
          <el-form-item>
            <el-input
              v-model="loginForm.password"
              placeholder="密码"
              show-password
              size="large"
              type="password"
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          <el-button
            class="login-button"
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form>
      </div>
    </section>

    <section v-else class="workspace">
      <aside class="setting-nav">
        <div class="nav-brand">
          <div class="eyebrow">站点配置</div>
          <h1>Home Admin</h1>
        </div>
        <button
          v-for="item in navItems"
          :key="item.key"
          :class="{ 'nav-item': true, active: activeSection === item.key }"
          type="button"
          @click="activeSection = item.key"
        >
          <component :is="item.icon" theme="outline" size="21" />
          <span>{{ item.label }}</span>
        </button>
        <div class="nav-spacer" />
        <div class="nav-actions">
          <el-button
            :icon="RefreshOne"
            circle
            :loading="loading"
            title="刷新"
            @click="loadAdminData"
          />
          <el-button :icon="Logout" circle title="退出登录" @click="handleLogout" />
        </div>
      </aside>

      <section class="setting-main">
        <header class="admin-header">
          <div>
            <div class="eyebrow">{{ activeMeta.eyebrow }}</div>
            <h2>{{ activeMeta.title }}</h2>
          </div>
          <div class="header-actions">
            <el-button v-if="activeSection === 'links'" :icon="Add" type="primary" @click="addLink">
              新增链接
            </el-button>
            <el-button :icon="Save" :loading="saving" @click="saveCurrentSection"
              >保存配置</el-button
            >
          </div>
        </header>

        <div v-if="activeSection !== 'links'" class="config-panel">
          <div v-for="field in activeFields" :key="field.key" class="field-row">
            <label :for="field.key">
              <span>{{ field.label }}</span>
              <small>{{ field.hint }}</small>
            </label>
            <el-input
              v-if="field.type !== 'textarea'"
              :id="field.key"
              v-model="configForm[field.key]"
              :placeholder="field.placeholder"
            />
            <el-input
              v-else
              :id="field.key"
              v-model="configForm[field.key]"
              :autosize="{ minRows: 3, maxRows: 5 }"
              :placeholder="field.placeholder"
              type="textarea"
            />
          </div>
        </div>

        <div v-else class="link-editor">
          <div v-for="(item, index) in links" :key="item.localId" class="link-row">
            <div class="order">{{ index + 1 }}</div>
            <el-select v-model="item.icon" class="icon-select" filterable placeholder="图标">
              <el-option v-for="icon in iconOptions" :key="icon" :label="icon" :value="icon" />
            </el-select>
            <el-input v-model="item.name" class="name-input" placeholder="名称" />
            <el-input v-model="item.link" class="url-input" placeholder="https://example.com" />
            <el-switch v-model="item.enabledFlag" :active-value="1" :inactive-value="0" />
            <el-button
              :icon="Up"
              circle
              title="上移"
              :disabled="index === 0"
              @click="moveLink(index, -1)"
            />
            <el-button
              :icon="Down"
              circle
              title="下移"
              :disabled="index === links.length - 1"
              @click="moveLink(index, 1)"
            />
            <el-button
              :icon="Delete"
              circle
              title="删除"
              type="danger"
              @click="removeLink(index)"
            />
          </div>
        </div>
      </section>
    </section>
  </main>
</template>

<script setup>
import {
  Add,
  Config,
  Delete,
  Down,
  EditName,
  LinkOne,
  Logout,
  SunOne,
  RefreshOne,
  Save,
  Up,
} from "@icon-park/vue-next";
import {
  getAdminInfo,
  getAdminSiteConfig,
  getAdminSiteLinks,
  loginAdmin,
  logoutAdmin,
  saveAdminSiteConfig,
  saveAdminSiteLinks,
} from "@/api";
import { defaultSiteConfig } from "@/utils/siteConfig";

const iconOptions = [
  "Blog",
  "Cloud",
  "CompactDisc",
  "Compass",
  "Book",
  "Fire",
  "LaptopCode",
  "Link",
];

const sectionMap = {
  site: {
    title: "站点资料",
    eyebrow: "基础资源",
    fields: [
      ["siteName", "站点名称", "加载页与应用名称", "例如：主页"],
      ["siteAuthor", "作者", "页脚版权展示", "例如：Ryan"],
      ["siteUrl", "站点地址", "Logo 文本与页脚链接", "example.com"],
      ["siteLogo", "标签图标", "浏览器标题栏与书签图标", "/images/icon/favicon.ico"],
      ["siteMainLogo", "主页头像", "左侧主视觉 Logo", "/images/icon/logo.png"],
      ["siteAppleLogo", "Apple 图标", "iOS 添加到主屏幕时使用", "/images/logo/apple-touch-icon.png"],
      ["siteStart", "建站日期", "YYYY-MM-DD 或 YYYY", "2020-10-24"],
      ["siteIcp", "ICP备案号", "留空则不显示", "豫ICP备..."],
      ["siteKeywords", "关键词", "用于站点元信息", "个人主页,导航"],
      ["siteDescription", "站点简介", "用于站点元信息", "一个默默无闻的主页", "textarea"],
    ],
  },
  description: {
    title: "首页文案",
    eyebrow: "简介卡片",
    fields: [
      ["descHello", "默认招呼", "简介卡片首行", "Hello World !"],
      ["descText", "默认简介", "简介卡片正文", "一个建立于 21 世纪的小站", "textarea"],
      ["descHelloOther", "切换招呼", "打开右侧盒子时展示", "Oops !"],
      ["descTextOther", "切换简介", "打开右侧盒子时展示", "哎呀，这都被你发现了", "textarea"],
    ],
  },
  media: {
    title: "天气服务",
    eyebrow: "外部服务",
    fields: [["weatherKey", "高德天气 Key", "留空则使用备用天气接口", ""]],
  },
};

const navItems = [
  { key: "site", label: "站点资料", icon: Config },
  { key: "description", label: "首页文案", icon: EditName },
  { key: "media", label: "天气服务", icon: SunOne },
  { key: "links", label: "导航链接", icon: LinkOne },
];

const isLogin = ref(false);
const loading = ref(false);
const saving = ref(false);
const activeSection = ref("site");
const loginForm = reactive({
  username: "",
  password: "",
});
const configForm = reactive({ ...defaultSiteConfig });
const links = ref([]);

const activeMeta = computed(() => {
  if (activeSection.value === "links") {
    return { title: "导航链接", eyebrow: "链接资源" };
  }
  return sectionMap[activeSection.value];
});

const activeFields = computed(() =>
  (sectionMap[activeSection.value]?.fields || []).map(
    ([key, label, hint, placeholder, type = "text"]) => ({
      key,
      label,
      hint,
      placeholder,
      type,
    }),
  ),
);

const normalizeLinks = (list) =>
  list.map((item, index) => ({
    localId: `${Date.now()}-${index}-${item.id || "new"}`,
    id: item.id,
    icon: item.icon || "Link",
    name: item.name || "",
    link: item.link || "",
    sortOrder: index + 1,
    enabledFlag: item.enabledFlag ?? 1,
  }));

const loadConfig = async () => {
  const data = await getAdminSiteConfig();
  Object.assign(configForm, defaultSiteConfig);
  data.forEach((item) => {
    configForm[item.configKey] = item.configValue ?? "";
  });
};

const loadLinks = async () => {
  const data = await getAdminSiteLinks();
  links.value = normalizeLinks(data || []);
};

const loadAdminData = async () => {
  loading.value = true;
  try {
    await Promise.all([loadConfig(), loadLinks()]);
  } catch (error) {
    ElMessage.error(error.message || "读取配置失败");
  } finally {
    loading.value = false;
  }
};

const handleLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.warning("请输入用户名和密码");
    return;
  }
  loading.value = true;
  try {
    await loginAdmin(loginForm.username, loginForm.password);
    isLogin.value = true;
    await loadAdminData();
  } catch (error) {
    ElMessage.error(error.message || "登录失败");
  } finally {
    loading.value = false;
  }
};

const addLink = () => {
  links.value.push({
    localId: `${Date.now()}-${links.value.length}`,
    icon: "Blog",
    name: "",
    link: "",
    sortOrder: links.value.length + 1,
    enabledFlag: 1,
  });
};

const removeLink = (index) => {
  links.value.splice(index, 1);
};

const moveLink = (index, step) => {
  const targetIndex = index + step;
  const nextLinks = [...links.value];
  const [current] = nextLinks.splice(index, 1);
  nextLinks.splice(targetIndex, 0, current);
  links.value = nextLinks;
};

const saveConfig = async () => {
  await saveAdminSiteConfig({ ...configForm });
  ElMessage.success("站点配置已保存");
  await loadConfig();
};

const saveLinks = async () => {
  const invalid = links.value.some((item) => !item.icon || !item.name || !item.link);
  if (invalid) {
    ElMessage.warning("请补全图标、名称和链接");
    return;
  }
  await saveAdminSiteLinks(
    links.value.map((item, index) => ({
      icon: item.icon,
      name: item.name,
      link: item.link,
      sortOrder: index + 1,
      enabledFlag: item.enabledFlag,
    })),
  );
  ElMessage.success("导航链接已保存");
  await loadLinks();
};

const saveCurrentSection = async () => {
  saving.value = true;
  try {
    if (activeSection.value === "links") {
      await saveLinks();
    } else {
      await saveConfig();
    }
  } catch (error) {
    ElMessage.error(error.message || "保存失败");
  } finally {
    saving.value = false;
  }
};

const handleLogout = async () => {
  await logoutAdmin().catch(() => {});
  isLogin.value = false;
  loginForm.password = "";
};

onMounted(async () => {
  try {
    await getAdminInfo();
    isLogin.value = true;
    await loadAdminData();
  } catch {
    isLogin.value = false;
  }
});
</script>

<style lang="scss" scoped>
.admin-page {
  position: relative;
  z-index: 3;
  width: 100%;
  height: 100%;
  padding: 40px;
  overflow-y: auto;
  background: rgb(0 0 0 / 35%);
  backdrop-filter: blur(14px);
  animation: fade 0.5s;
}

.login-shell {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-panel,
.workspace {
  border-radius: 8px;
  background: rgb(0 0 0 / 38%);
  border: 1px solid rgb(255 255 255 / 18%);
  box-shadow: 0 20px 60px rgb(0 0 0 / 22%);
}

.login-panel {
  width: min(420px, 100%);
  padding: 34px;
}

.brand {
  margin-bottom: 28px;
  font-family: "Pacifico-Regular", sans-serif;
  font-size: 2rem;
  text-align: center;
  text-shadow: 0 0 8px #00000070;
}

.login-button {
  width: 100%;
}

.workspace {
  width: min(1240px, 100%);
  min-height: calc(100vh - 80px);
  margin: 0 auto;
  padding: 18px;
  display: grid;
  grid-template-columns: 250px minmax(0, 1fr);
  gap: 18px;
}

.setting-nav,
.setting-main {
  border-radius: 8px;
  border: 1px solid rgb(255 255 255 / 14%);
  background: rgb(255 255 255 / 9%);
}

.setting-nav {
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nav-brand {
  margin-bottom: 18px;
  h1 {
    font-family: "Pacifico-Regular", sans-serif;
    font-size: 2rem;
    line-height: 1.2;
  }
}

.eyebrow {
  margin-bottom: 4px;
  color: rgb(255 255 255 / 68%);
  font-size: 0.9rem;
}

.nav-item {
  height: 44px;
  padding: 0 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  border: 1px solid transparent;
  border-radius: 7px;
  background: transparent;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;

  &:hover,
  &.active {
    background: rgb(255 255 255 / 16%);
    border-color: rgb(255 255 255 / 22%);
  }

  &.active {
    box-shadow: 0 10px 28px rgb(0 0 0 / 18%);
  }
}

.nav-spacer {
  flex: 1;
}

.nav-actions,
.header-actions {
  display: flex;
  gap: 10px;
}

.setting-main {
  padding: 28px;
  min-width: 0;
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
  h2 {
    font-size: 2rem;
    line-height: 1.2;
  }
}

.config-panel {
  display: grid;
  gap: 14px;
}

.field-row {
  display: grid;
  grid-template-columns: minmax(150px, 210px) minmax(0, 1fr);
  gap: 18px;
  align-items: start;
  padding: 14px;
  border-radius: 8px;
  background: rgb(255 255 255 / 9%);
  border: 1px solid rgb(255 255 255 / 12%);

  label {
    display: flex;
    flex-direction: column;
    gap: 5px;
    line-height: 1.4;

    small {
      color: rgb(255 255 255 / 58%);
    }
  }
}

.link-editor {
  display: grid;
  gap: 12px;
}

.link-row {
  display: grid;
  grid-template-columns: 42px 150px 160px minmax(220px, 1fr) 70px 40px 40px 40px;
  gap: 10px;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  background: rgb(255 255 255 / 10%);
  border: 1px solid rgb(255 255 255 / 12%);
}

.order {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: rgb(255 255 255 / 14%);
  font-family: "UnidreamLED", sans-serif;
}

:deep(.el-input__wrapper),
:deep(.el-select__wrapper),
:deep(.el-textarea__inner) {
  background: rgb(0 0 0 / 22%);
  box-shadow: 0 0 0 1px rgb(255 255 255 / 14%) inset;
}

:deep(.el-input__inner),
:deep(.el-select__placeholder),
:deep(.el-select__selected-item),
:deep(.el-textarea__inner) {
  color: #fff;
}

// Keep admin buttons readable against the page's glass background.
:deep(.el-button) {
  --el-button-text-color: #fff;
  --el-button-bg-color: rgb(0 0 0 / 60%);
  --el-button-border-color: rgb(255 255 255 / 20%);
  --el-button-hover-text-color: #fff;
  --el-button-hover-bg-color: rgb(0 0 0 / 80%);
  --el-button-hover-border-color: rgb(255 255 255 / 40%);
  --el-button-active-text-color: #fff;
  --el-button-active-bg-color: rgb(0 0 0 / 85%);
  --el-button-active-border-color: rgb(255 255 255 / 48%);
}

:deep(.el-button--default) {
  color: #fff;
  background-color: rgb(0 0 0 / 60%);
  border-color: rgb(255 255 255 / 20%);

  &:hover,
  &:focus {
    background-color: rgb(0 0 0 / 80%);
    border-color: rgb(255 255 255 / 40%);
  }
}

:deep(.el-button--primary) {
  color: #fff;
  background-color: #000;
  border-color: rgb(255 255 255 / 24%);

  &:hover,
  &:focus {
    color: #fff;
    background-color: rgb(0 0 0 / 88%);
    border-color: rgb(255 255 255 / 42%);
  }
}

:deep(.el-button--default *) {
  color: inherit;
}

:deep(.el-button--primary *) {
  color: inherit;
}

@media (max-width: 980px) {
  .admin-page {
    padding: 18px;
  }
  .workspace {
    grid-template-columns: 1fr;
    min-height: auto;
  }
  .setting-nav {
    flex-direction: row;
    align-items: center;
    overflow-x: auto;
  }
  .nav-brand,
  .nav-spacer {
    display: none;
  }
  .nav-item {
    white-space: nowrap;
  }
}

@media (max-width: 720px) {
  .setting-main {
    padding: 18px;
  }
  .admin-header,
  .header-actions {
    flex-wrap: wrap;
  }
  .field-row {
    grid-template-columns: 1fr;
  }
  .link-row {
    grid-template-columns: 38px 1fr 1fr 58px;
    .url-input {
      grid-column: 2 / 5;
    }
  }
}

@media (max-width: 560px) {
  .admin-page {
    padding: 12px;
  }
  .link-row {
    grid-template-columns: 34px 1fr 58px;
    .icon-select,
    .name-input,
    .url-input {
      grid-column: 2 / 4;
    }
  }
}
</style>
