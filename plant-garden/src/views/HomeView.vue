<template>
  <div class="home-page">
    <!-- 顶部横幅 -->
    <div class="banner">
      <div class="banner-content">
        <h1>绿居园艺</h1>
        <p>让生活充满绿意，让心灵回归自然</p>
        <el-button type="primary" size="large" @click="$router.push('/plants')">
          开始探索
        </el-button>
      </div>
    </div>

    <!-- 特色服务 -->
    <div class="features">
      <div class="feature-item">
        <el-icon size="40"><House /></el-icon>
        <h3>植物分类</h3>
        <p>专业的植物分类系统，帮助您快速找到心仪的植物</p>
      </div>
      <div class="feature-item">
        <el-icon size="40"><Reading /></el-icon>
        <h3>养护指南</h3>
        <p>详细的养护知识，让您的植物茁壮成长</p>
      </div>
      <div class="feature-item">
        <el-icon size="40"><ChatDotRound /></el-icon>
        <h3>社区交流</h3>
        <p>与园艺爱好者分享经验，解答疑惑</p>
      </div>
    </div>

    <!-- 热门植物 -->
    <div class="section">
      <div class="section-header">
        <h2>热门植物</h2>
        <router-link to="/plants" class="more-link">
          查看更多 <el-icon><ArrowRight /></el-icon>
        </router-link>
      </div>
      <div class="plants-grid">
        <el-card v-for="plant in popularPlants" :key="plant.id" class="plant-card">
          <img :src="plant.image" :alt="plant.name" class="plant-image" />
          <div class="plant-info">
            <h3>{{ plant.name }}</h3>
            <p class="scientific-name">{{ plant.scientificName }}</p>
            <p class="description">{{ plant.description }}</p>
            <el-tag size="small" :type="getDifficultyType(plant.difficulty)">
              {{ getDifficultyLabel(plant.difficulty) }}
            </el-tag>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 最新指南 -->
    <div class="section">
      <div class="section-header">
        <h2>最新养护指南</h2>
        <router-link to="/care-guides" class="more-link">
          查看更多 <el-icon><ArrowRight /></el-icon>
        </router-link>
      </div>
      <div class="guides-grid">
        <el-card v-for="guide in latestGuides" :key="guide.id" class="guide-card">
          <div class="guide-header">
            <h3>{{ guide.title }}</h3>
            <el-tag :type="getCategoryType(guide.category)" size="small">
              {{ getCategoryLabel(guide.category) }}
            </el-tag>
          </div>
          <p class="summary">{{ guide.summary }}</p>
          <div class="guide-meta">
            <div class="author">
              <el-avatar :size="24" :src="guide.author.avatar" />
              <span>{{ guide.author.name }}</span>
            </div>
            <span class="date">{{ guide.date }}</span>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { House, Reading, ChatDotRound, ArrowRight } from '@element-plus/icons-vue'
import type { Plant as PlantType, CareGuide } from '../types/plant'
import { plants } from '../mock/plants'
import { guides } from '../mock/guides'

// 获取热门植物
const popularPlants = ref<PlantType[]>(plants.slice(0, 4))

// 获取最新指南
const latestGuides = ref<CareGuide[]>(guides.slice(0, 3))

// 获取难度标签类型
const getDifficultyType = (difficulty: string) => {
  const types = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger'
  }
  return types[difficulty as keyof typeof types] || 'info'
}

// 获取难度标签文本
const getDifficultyLabel = (difficulty: string) => {
  const labels = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return labels[difficulty as keyof typeof labels] || '未知'
}

// 获取分类标签类型
const getCategoryType = (category: string) => {
  const types = {
    watering: 'primary',
    lighting: 'success',
    soil: 'warning',
    fertilizer: 'info',
    pest: 'danger'
  }
  return types[category as keyof typeof types] || 'info'
}

// 获取分类标签文本
const getCategoryLabel = (category: string) => {
  const labels = {
    watering: '浇水技巧',
    lighting: '光照管理',
    soil: '土壤养护',
    fertilizer: '施肥方法',
    pest: '病虫害防治'
  }
  return labels[category as keyof typeof labels] || '其他'
}
</script>

<style lang="scss" scoped>
.home-page {
  padding-top: 60px;
}

.banner {
  height: 500px;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
              url('@/assets/banner.svg') center/cover;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #fff;
  margin-bottom: 60px;

  .banner-content {
    h1 {
      font-size: 48px;
      margin-bottom: 20px;
    }

    p {
      font-size: 24px;
      margin-bottom: 30px;
    }
  }
}

.features {
  max-width: 1200px;
  margin: 0 auto 60px;
  padding: 0 20px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  text-align: center;

  .feature-item {
    padding: 30px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

    .el-icon {
      color: var(--el-color-primary);
      margin-bottom: 20px;
    }

    h3 {
      font-size: 20px;
      margin-bottom: 15px;
    }

    p {
      color: #666;
      line-height: 1.6;
    }
  }
}

.section {
  max-width: 1200px;
  margin: 0 auto 60px;
  padding: 0 20px;

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;

    h2 {
      font-size: 28px;
      margin: 0;
    }

    .more-link {
      color: var(--el-color-primary);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 5px;
    }
  }
}

.plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;

  .plant-card {
    cursor: pointer;
    transition: transform 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    .plant-image {
      width: 100%;
      height: 200px;
      object-fit: cover;
    }

    .plant-info {
      padding: 15px;

      h3 {
        margin: 0 0 5px;
        font-size: 18px;
      }

      .scientific-name {
        color: #666;
        font-style: italic;
        margin-bottom: 10px;
      }

      .description {
        color: #666;
        margin-bottom: 10px;
        line-height: 1.4;
      }
    }
  }
}

.guides-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;

  .guide-card {
    .guide-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;

      h3 {
        margin: 0;
        font-size: 18px;
      }
    }

    .summary {
      color: #666;
      margin-bottom: 15px;
      line-height: 1.4;
    }

    .guide-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: #999;

      .author {
        display: flex;
        align-items: center;
        gap: 8px;
      }
    }
  }
}
</style> 