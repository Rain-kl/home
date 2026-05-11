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
          <el-button class="login-button" type="primary" size="large" :loading="loading" @click="handleLogin">
            登录
          </el-button>
        </el-form>
      </div>
    </section>

    <section v-else class="workspace">
      <header class="admin-header">
        <div>
          <div class="eyebrow">站点配置</div>
          <h1>导航链接</h1>
        </div>
        <div class="header-actions">
          <el-button :icon="RefreshOne" circle :loading="loading" title="刷新" @click="loadLinks" />
          <el-button :icon="Logout" circle title="退出登录" @click="handleLogout" />
        </div>
      </header>

      <div class="toolbar">
        <el-button :icon="Add" type="primary" @click="addLink">新增链接</el-button>
        <el-button :icon="Save" :loading="saving" @click="saveLinks">保存配置</el-button>
      </div>

      <div class="link-editor">
        <div v-for="(item, index) in links" :key="item.localId" class="link-row">
          <div class="order">{{ index + 1 }}</div>
          <el-select v-model="item.icon" class="icon-select" filterable placeholder="图标">
            <el-option v-for="icon in iconOptions" :key="icon" :label="icon" :value="icon" />
          </el-select>
          <el-input v-model="item.name" class="name-input" placeholder="名称" />
          <el-input v-model="item.link" class="url-input" placeholder="https://example.com" />
          <el-switch v-model="item.enabledFlag" :active-value="1" :inactive-value="0" />
          <el-button :icon="Up" circle title="上移" :disabled="index === 0" @click="moveLink(index, -1)" />
          <el-button
            :icon="Down"
            circle
            title="下移"
            :disabled="index === links.length - 1"
            @click="moveLink(index, 1)"
          />
          <el-button :icon="Delete" circle title="删除" type="danger" @click="removeLink(index)" />
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { Add, Delete, Down, Logout, RefreshOne, Save, Up } from "@icon-park/vue-next";
import {
  getAdminInfo,
  getAdminSiteLinks,
  loginAdmin,
  logoutAdmin,
  saveAdminSiteLinks,
} from "@/api";

const iconOptions = ["Blog", "Cloud", "CompactDisc", "Compass", "Book", "Fire", "LaptopCode"];

const isLogin = ref(false);
const loading = ref(false);
const saving = ref(false);
const loginForm = reactive({
  username: "",
  password: "",
});
const links = ref([]);

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

const loadLinks = async () => {
  loading.value = true;
  try {
    const data = await getAdminSiteLinks();
    links.value = normalizeLinks(data || []);
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
    await loadLinks();
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

const saveLinks = async () => {
  const invalid = links.value.some((item) => !item.icon || !item.name || !item.link);
  if (invalid) {
    ElMessage.warning("请补全图标、名称和链接");
    return;
  }
  saving.value = true;
  try {
    await saveAdminSiteLinks(
      links.value.map((item, index) => ({
        icon: item.icon,
        name: item.name,
        link: item.link,
        sortOrder: index + 1,
        enabledFlag: item.enabledFlag,
      })),
    );
    ElMessage.success("配置已保存");
    await loadLinks();
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
    await loadLinks();
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
  min-height: 100%;
  padding: 40px;
  overflow: auto;
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
  width: min(1180px, 100%);
  margin: 0 auto;
  padding: 28px;
}

.admin-header,
.toolbar,
.link-row {
  display: flex;
  align-items: center;
}

.admin-header {
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
  h1 {
    font-size: 2rem;
    line-height: 1.2;
  }
}

.eyebrow {
  margin-bottom: 4px;
  color: rgb(255 255 255 / 68%);
  font-size: 0.9rem;
}

.header-actions,
.toolbar {
  display: flex;
  gap: 10px;
}

.toolbar {
  margin-bottom: 18px;
}

.link-editor {
  display: grid;
  gap: 12px;
}

.link-row {
  display: grid;
  grid-template-columns: 42px 150px 160px minmax(220px, 1fr) 70px 40px 40px 40px;
  gap: 10px;
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
:deep(.el-select__wrapper) {
  background: rgb(0 0 0 / 22%);
  box-shadow: 0 0 0 1px rgb(255 255 255 / 14%) inset;
}

:deep(.el-input__inner),
:deep(.el-select__placeholder),
:deep(.el-select__selected-item) {
  color: #fff;
}

@media (max-width: 900px) {
  .admin-page {
    padding: 18px;
  }
  .workspace {
    padding: 18px;
  }
  .admin-header {
    align-items: flex-start;
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
  .admin-header,
  .toolbar {
    flex-wrap: wrap;
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
