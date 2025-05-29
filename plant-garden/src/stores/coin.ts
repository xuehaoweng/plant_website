import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Transaction, TransactionType, TransactionSource } from '@/types/coin'
import { COIN_RULES } from '@/types/coin'

export const useCoinStore = defineStore('coin', () => {
  // 状态
  const transactions = ref<Transaction[]>([])
  const balance = ref(0)

  // 计算属性：交易历史
  const transactionHistory = computed(() => {
    return [...transactions.value].sort((a, b) => 
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    )
  })

  // 计算属性：收入统计
  const incomeStats = computed(() => {
    return transactions.value
      .filter(t => t.type === 'earn')
      .reduce((sum, t) => sum + t.amount, 0)
  })

  // 计算属性：支出统计
  const expenseStats = computed(() => {
    return transactions.value
      .filter(t => t.type === 'spend')
      .reduce((sum, t) => sum + t.amount, 0)
  })

  // 方法：添加交易记录
  const addTransaction = (
    userId: number,
    type: TransactionType,
    source: TransactionSource,
    description: string
  ) => {
    const amount = type === 'earn' 
      ? COIN_RULES.earn[source as keyof typeof COIN_RULES.earn]
      : COIN_RULES.spend[source as keyof typeof COIN_RULES.spend]

    const transaction: Transaction = {
      id: Date.now(),
      userId,
      type,
      amount,
      source,
      description,
      createdAt: new Date().toISOString()
    }

    transactions.value.push(transaction)
    balance.value += type === 'earn' ? amount : -amount

    return transaction
  }

  // 方法：检查余额是否足够
  const checkBalance = (amount: number) => {
    return balance.value >= amount
  }

  // 方法：获取交易记录
  const getTransactions = (userId: number) => {
    return transactions.value.filter(t => t.userId === userId)
  }

  // 方法：重置状态（用于测试）
  const reset = () => {
    transactions.value = []
    balance.value = 0
  }

  return {
    balance,
    transactions,
    transactionHistory,
    incomeStats,
    expenseStats,
    addTransaction,
    checkBalance,
    getTransactions,
    reset
  }
}) 