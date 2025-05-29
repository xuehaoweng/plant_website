<template>
  <header class="nav-header">
    <div class="nav-container">
      <div class="nav-left">
        <router-link to="/" class="logo">
          <img src="@/assets/logo.svg" alt="绿居园艺" />
          <span>绿居园艺</span>
        </router-link>
        <nav class="nav-menu">
          <router-link to="/plants" class="nav-item">植物分类</router-link>
          <router-link to="/care-guides" class="nav-item">养护指南</router-link>
          <router-link to="/problems" class="nav-item">常见问题</router-link>
          <router-link to="/community" class="nav-item">社区交流</router-link>
        </nav>
      </div>
      <div class="nav-right">
        <template v-if="userStore.isLoggedIn">
          <div class="user-coins">
            <el-icon><Money /></el-icon>
            <span>{{ coinStore.balance }}</span>
          </div>
          <el-dropdown>
            <div class="user-info">
              <el-avatar :size="32" :src="userStore.currentUser?.avatar" />
              <span class="username">{{ userStore.currentUser?.name }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push('/user')">
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item @click="handleLogout">
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" @click="showLoginDialog">
            登录
          </el-button>
          <el-button @click="showRegisterDialog">
            注册
          </el-button>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useCoinStore } from '@/stores/coin'
import { Money } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const coinStore = useCoinStore()

// 计算当前激活的菜单项
const activeMenu = computed(() => route.path)

// 显示登录对话框
const showLoginDialog = () => {
  // TODO: 实现登录功能
}

// 显示注册对话框
const showRegisterDialog = () => {
  // TODO: 实现注册功能
}

// 处理退出登录
const handleLogout = () => {
  localStorage.removeItem('auth_token')
  userStore.isLoggedIn = false
  router.push('/')
}
</script>

<style lang="scss" scoped>
.nav-header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 40px;

  .logo {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: #333;

    img {
      height: 40px;
      margin-right: 10px;
    }

    span {
      font-size: 20px;
      font-weight: bold;
    }
  }

  .nav-menu {
    display: flex;
    gap: 30px;

    .nav-item {
      text-decoration: none;
      color: #333;
      font-size: 16px;
      padding: 5px 0;
      position: relative;

      &:hover {
        color: #409eff;
      }

      &.router-link-active {
        color: #409eff;

        &::after {
          content: '';
          position: absolute;
          bottom: -2px;
          left: 0;
          right: 0;
          height: 2px;
          background-color: #409eff;
        }
      }
    }
  }
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 20px;

  .user-coins {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 5px 10px;
    background-color: #f0f9eb;
    border-radius: 4px;
    color: #67c23a;

    .el-icon {
      font-size: 16px;
    }

    span {
      font-weight: bold;
    }
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 4px;
    transition: background-color 0.3s;

    &:hover {
      background-color: #f5f7fa;
    }

    .username {
      font-size: 14px;
      color: #333;
    }
  }
}

:deep(.el-button) {
  padding: 8px 20px;
  font-size: 14px;
}
</style> 