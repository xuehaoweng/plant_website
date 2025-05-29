<template>
  <div class="user-page">
    <div class="page-header">
      <h1>个人中心</h1>
    </div>

    <div class="main-content">
      <!-- 左侧导航 -->
      <div class="nav-section">
        <el-menu
          :default-active="activeTab"
          class="user-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="profile">
            <el-icon><User /></el-icon>
            <span>个人资料</span>
          </el-menu-item>
          <el-menu-item index="coins">
            <el-icon><Money /></el-icon>
            <span>我的园艺币</span>
          </el-menu-item>
          <el-menu-item index="favorites">
            <el-icon><Star /></el-icon>
            <span>我的收藏</span>
          </el-menu-item>
          <el-menu-item index="posts">
            <el-icon><Document /></el-icon>
            <span>我的帖子</span>
          </el-menu-item>
          <el-menu-item index="qa">
            <el-icon><ChatDotRound /></el-icon>
            <span>我的问答</span>
          </el-menu-item>
          <el-menu-item index="settings">
            <el-icon><Setting /></el-icon>
            <span>账号设置</span>
          </el-menu-item>
        </el-menu>
      </div>

      <!-- 右侧内容区 -->
      <div class="content-section">
        <!-- 个人资料 -->
        <div v-if="activeTab === 'profile'" class="profile-section">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>个人资料</span>
                <el-button type="primary" @click="handleEditProfile">编辑资料</el-button>
              </div>
            </template>
            <div class="profile-info">
              <el-avatar :size="100" :src="userInfo.avatar" />
              <div class="user-details">
                <h2>{{ userInfo.name }}</h2>
                <p class="user-bio">{{ userInfo.bio }}</p>
                <div class="user-stats">
                  <div class="stat-item">
                    <span class="stat-value">{{ userInfo.posts }}</span>
                    <span class="stat-label">帖子</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-value">{{ userInfo.followers }}</span>
                    <span class="stat-label">粉丝</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-value">{{ userInfo.following }}</span>
                    <span class="stat-label">关注</span>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 园艺币 -->
        <div v-if="activeTab === 'coins'" class="coins-section">
          <el-card class="balance-card">
            <template #header>
              <div class="card-header">
                <span>园艺币余额</span>
                <el-button type="primary" @click="showRechargeDialog">充值</el-button>
              </div>
            </template>
            <div class="balance-info">
              <el-icon size="40" class="coin-icon"><Money /></el-icon>
              <div class="balance-details">
                <span class="balance-amount">{{ userInfo.coins }}</span>
                <span class="balance-label">园艺币</span>
              </div>
            </div>
            <div class="balance-stats">
              <div class="stat-item">
                <span class="stat-label">总收入</span>
                <span class="stat-value">+{{ coinStore.incomeStats }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">总支出</span>
                <span class="stat-value">-{{ coinStore.expenseStats }}</span>
              </div>
            </div>
          </el-card>

          <el-card class="transactions-card">
            <template #header>
              <div class="card-header">
                <span>交易记录</span>
              </div>
            </template>
            <div class="transactions-list">
              <div v-for="tx in transactions" :key="tx.id" class="transaction-item">
                <div class="transaction-info">
                  <span class="transaction-type" :class="tx.type">
                    {{ tx.type === 'earn' ? '+' : '-' }}{{ tx.amount }}
                  </span>
                  <span class="transaction-desc">{{ tx.description }}</span>
                </div>
                <span class="transaction-time">{{ new Date(tx.createdAt).toLocaleString() }}</span>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 其他标签页内容 -->
        <div v-else class="other-sections">
          <!-- 这里可以添加其他标签页的内容 -->
        </div>
      </div>
    </div>

    <!-- 充值对话框 -->
    <el-dialog
      v-model="rechargeDialogVisible"
      title="园艺币充值"
      width="400px"
    >
      <div class="recharge-content">
        <div class="amount-options">
          <div
            v-for="amount in rechargeAmounts"
            :key="amount.value"
            class="amount-option"
            :class="{ active: selectedAmount === amount.value }"
            @click="selectedAmount = amount.value"
          >
            <span class="amount">{{ amount.value }}元</span>
            <span class="coins">{{ amount.coins }}园艺币</span>
          </div>
        </div>
        <div class="payment-methods">
          <div class="method-title">选择支付方式</div>
          <div class="method-options">
            <div
              class="method-option"
              :class="{ active: selectedMethod === 'wechat' }"
              @click="selectedMethod = 'wechat'"
            >
              <el-icon><Money /></el-icon>
              <span>微信支付</span>
            </div>
            <div
              class="method-option"
              :class="{ active: selectedMethod === 'alipay' }"
              @click="selectedMethod = 'alipay'"
            >
              <el-icon><Money /></el-icon>
              <span>支付宝</span>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="rechargeDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleRecharge">
            确认支付 {{ selectedAmount }}元
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { User, Money, Star, Document, ChatDotRound, Setting } from '@element-plus/icons-vue'
import { useCoinStore } from '@/stores/coin'
import type { Transaction } from '@/types/coin'
import { ElMessage } from 'element-plus'

// 状态
const activeTab = ref('profile')
const coinStore = useCoinStore()
const rechargeDialogVisible = ref(false)
const selectedAmount = ref(10)
const selectedMethod = ref('wechat')

// 充值金额选项
const rechargeAmounts = [
  { value: 10, coins: 100 },
  { value: 50, coins: 550 },
  { value: 100, coins: 1200 },
  { value: 200, coins: 2600 },
  { value: 500, coins: 7000 },
  { value: 1000, coins: 15000 }
]

// 用户信息
const userInfo = ref({
  id: 1,
  name: '园艺达人',
  avatar: '/images/avatars/user1.jpg',
  bio: '热爱园艺，专注室内植物养护',
  coins: coinStore.balance,
  posts: 128,
  followers: 256,
  following: 64
})

// 交易记录
const transactions = ref<Transaction[]>([])

// 获取交易记录
const loadTransactions = () => {
  transactions.value = coinStore.getTransactions(userInfo.value.id)
}

// 初始化
loadTransactions()

// 处理菜单选择
const handleMenuSelect = (key: string) => {
  activeTab.value = key
}

// 显示充值对话框
const showRechargeDialog = () => {
  rechargeDialogVisible.value = true
}

// 处理充值
const handleRecharge = () => {
  // 模拟充值过程
  const amount = selectedAmount.value
  const coins = rechargeAmounts.find(a => a.value === amount)?.coins || 0
  
  // 添加交易记录
  coinStore.addTransaction(
    userInfo.value.id,
    'earn',
    coins,
    'system',
    `充值${amount}元`,
    new Date().toISOString()
  )

  // 更新用户余额
  userInfo.value.coins += coins

  // 关闭对话框
  rechargeDialogVisible.value = false

  // 显示成功提示
  ElMessage.success(`充值成功，获得${coins}园艺币`)
}

// 编辑个人资料
const handleEditProfile = () => {
  // TODO: 实现编辑个人资料功能
}
</script>

<style lang="scss" scoped>
.user-page {
  max-width: 1200px;
  margin: 80px auto 40px;
  padding: 0 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;

  h1 {
    font-size: 32px;
    margin-bottom: 10px;
  }
}

.main-content {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 20px;
}

.nav-section {
  .user-menu {
    border-right: none;
  }
}

.content-section {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.profile-section {
  .profile-info {
    display: flex;
    gap: 30px;

    .user-details {
      flex: 1;

      h2 {
        margin: 0 0 10px;
      }

      .user-bio {
        color: #666;
        margin-bottom: 20px;
      }

      .user-stats {
        display: flex;
        gap: 40px;

        .stat-item {
          text-align: center;

          .stat-value {
            display: block;
            font-size: 24px;
            font-weight: bold;
            color: #333;
          }

          .stat-label {
            color: #666;
          }
        }
      }
    }
  }
}

.coins-section {
  .balance-card {
    margin-bottom: 20px;

    .balance-info {
      display: flex;
      align-items: center;
      gap: 20px;
      margin-bottom: 20px;

      .coin-icon {
        color: #f0a500;
      }

      .balance-details {
        .balance-amount {
          display: block;
          font-size: 32px;
          font-weight: bold;
          color: #333;
        }

        .balance-label {
          color: #666;
        }
      }
    }

    .balance-stats {
      display: flex;
      gap: 40px;

      .stat-item {
        .stat-label {
          display: block;
          color: #666;
          margin-bottom: 5px;
        }

        .stat-value {
          font-weight: bold;
          color: #333;
        }
      }
    }
  }

  .transactions-card {
    .transactions-list {
      .transaction-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 0;
        border-bottom: 1px solid #eee;

        &:last-child {
          border-bottom: none;
        }

        .transaction-info {
          display: flex;
          align-items: center;
          gap: 10px;

          .transaction-type {
            font-weight: bold;

            &.earn {
              color: #67c23a;
            }

            &.spend {
              color: #f56c6c;
            }
          }

          .transaction-desc {
            color: #666;
          }
        }

        .transaction-time {
          color: #999;
          font-size: 14px;
        }
      }
    }
  }
}

.recharge-content {
  .amount-options {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 20px;

    .amount-option {
      border: 1px solid #dcdfe6;
      border-radius: 4px;
      padding: 10px;
      text-align: center;
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        border-color: #409eff;
      }

      &.active {
        border-color: #409eff;
        background-color: #ecf5ff;
      }

      .amount {
        display: block;
        font-size: 18px;
        font-weight: bold;
        color: #333;
      }

      .coins {
        display: block;
        font-size: 12px;
        color: #666;
        margin-top: 5px;
      }
    }
  }

  .payment-methods {
    .method-title {
      margin-bottom: 10px;
      color: #666;
    }

    .method-options {
      display: flex;
      gap: 10px;

      .method-option {
        flex: 1;
        border: 1px solid #dcdfe6;
        border-radius: 4px;
        padding: 15px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;

        &:hover {
          border-color: #409eff;
        }

        &.active {
          border-color: #409eff;
          background-color: #ecf5ff;
        }

        .el-icon {
          font-size: 24px;
          margin-bottom: 5px;
        }

        span {
          display: block;
          color: #666;
        }
      }
    }
  }
}
</style> 