// 植物分类
export type PlantCategory = 'foliage' | 'flowering' | 'succulent' | 'aquatic' | 'herb'

// 养护难度
export type DifficultyLevel = 'easy' | 'medium' | 'hard'

// 植物信息接口
export interface Plant {
  id: number
  name: string
  scientificName: string
  category: PlantCategory
  difficulty: DifficultyLevel
  image: string
  description: string
  light: string
  water: string
  temperature: string
  soil: string
  careGuide: string
  commonProblems: string[]
}

// 养护指南分类
export type GuideCategory = 'watering' | 'lighting' | 'soil' | 'fertilizer' | 'pest'

// 作者信息
export interface Author {
  id: number
  name: string
  avatar: string
}

// 养护指南接口
export interface CareGuide {
  id: number
  title: string
  category: GuideCategory
  summary: string
  content: string
  author: Author
  date: string
  views: number
  likes: number
  tags: string[]
} 