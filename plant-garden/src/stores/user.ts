import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface User {
  id: number
  name: string
  avatar: string
  bio: string
  coins: number
  posts: number
  followers: number
  following: number
}

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<User | null>(null)
  const isLoggedIn = ref(false)

  // 登录
  const login = async (_username: string, _password: string) => {
    try {
      // TODO: 实现实际的登录API调用
      // 模拟登录成功
      currentUser.value = {
        id: 1,
        name: '园艺达人',
        avatar: '/images/avatars/user1.jpg',
        bio: '热爱园艺，专注室内植物养护',
        coins: 1000,
        posts: 128,
        followers: 256,
        following: 64
      }
      isLoggedIn.value = true
      return true
    } catch (error) {
      console.error('登录失败:', error)
      return false
    }
  }

  // 登出
  const logout = () => {
    currentUser.value = null
    isLoggedIn.value = false
  }

  // 更新用户信息
  const updateUserInfo = async (userInfo: Partial<User>) => {
    try {
      // TODO: 实现实际的更新API调用
      if (currentUser.value) {
        currentUser.value = { ...currentUser.value, ...userInfo }
      }
      return true
    } catch (error) {
      console.error('更新用户信息失败:', error)
      return false
    }
  }

  // 更新园艺币
  const updateCoins = (amount: number) => {
    if (currentUser.value) {
      currentUser.value.coins += amount
    }
  }

  return {
    currentUser,
    isLoggedIn,
    login,
    logout,
    updateUserInfo,
    updateCoins
  }
}) 