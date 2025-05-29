// 交易类型
export type TransactionType = 'earn' | 'spend'

// 交易来源
export type TransactionSource = 
  | 'post'           // 发帖奖励
  | 'answer'         // 回答问题奖励
  | 'consultation'   // 付费咨询
  | 'guide'          // 查看付费指南
  | 'system'         // 系统奖励

// 交易记录
export interface Transaction {
  id: number
  userId: number
  type: TransactionType
  amount: number
  source: TransactionSource
  description: string
  createdAt: string
}

// 园艺币规则
export const COIN_RULES = {
  // 获取规则
  earn: {
    post: 10,        // 发帖奖励
    answer: 5,       // 回答问题奖励
    system: 100      // 系统奖励（如注册奖励）
  },
  // 消费规则
  spend: {
    consultation: 50,  // 付费咨询
    guide: 20         // 查看付费指南
  }
} as const 