<template>
  <div class="care-guides">
    <!-- 搜索和分类 -->
    <div class="search-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索养护指南..."
        class="search-input"
        :prefix-icon="Search"
      />
      <div class="category-tabs">
        <el-tabs v-model="activeCategory" @tab-click="handleCategorySelect">
          <el-tab-pane label="全部" name="all" />
          <el-tab-pane label="浇水技巧" name="watering" />
          <el-tab-pane label="光照管理" name="lighting" />
          <el-tab-pane label="土壤养护" name="soil" />
          <el-tab-pane label="施肥方法" name="fertilizer" />
          <el-tab-pane label="病虫害防治" name="pest" />
        </el-tabs>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 指南列表 -->
      <div class="guides-list">
        <el-card v-for="guide in filteredGuides" :key="guide.id" class="guide-card">
          <div class="guide-header">
            <h3>{{ guide.title }}</h3>
            <el-tag :type="getCategoryType(guide.category)" size="small">
              {{ getCategoryLabel(guide.category) }}
            </el-tag>
          </div>
          <p class="guide-summary">{{ guide.summary }}</p>
          <div class="guide-meta">
            <div class="author-info">
              <el-avatar :size="24" :src="guide.author.avatar" />
              <span>{{ guide.author.name }}</span>
            </div>
            <div class="guide-stats">
              <span><el-icon><View /></el-icon> {{ guide.views }}</span>
              <span><el-icon><Thumb /></el-icon> {{ guide.likes }}</span>
            </div>
          </div>
          <div class="guide-footer">
            <el-button type="primary" @click="showGuideDetail(guide)">查看详情</el-button>
          </div>
        </el-card>

        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 30, 50]"
            :total="totalGuides"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>

      <!-- 侧边栏 -->
      <div class="sidebar">
        <!-- 热门指南 -->
        <el-card class="popular-guides">
          <template #header>
            <div class="card-header">
              <span>热门指南</span>
            </div>
          </template>
          <ul class="popular-list">
            <li v-for="guide in popularGuides" :key="guide.id" @click="showGuideDetail(guide)">
              <span class="title">{{ guide.title }}</span>
              <span class="views">{{ guide.views }} 阅读</span>
            </li>
          </ul>
        </el-card>
      </div>
    </div>

    <!-- 指南详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="selectedGuide?.title"
      width="70%"
      class="guide-dialog"
    >
      <div v-if="selectedGuide" class="guide-detail">
        <div class="guide-header">
          <el-tag :type="getCategoryType(selectedGuide.category)" size="small">
            {{ getCategoryLabel(selectedGuide.category) }}
          </el-tag>
          <div class="guide-meta">
            <div class="author-info">
              <el-avatar :size="32" :src="selectedGuide.author.avatar" />
              <span>{{ selectedGuide.author.name }}</span>
            </div>
            <div class="date">{{ selectedGuide.date }}</div>
          </div>
        </div>
        <div class="guide-content" v-html="selectedGuide.content"></div>
        <div class="guide-tags">
          <el-tag
            v-for="tag in selectedGuide.tags"
            :key="tag"
            size="small"
            class="tag"
          >
            {{ tag }}
          </el-tag>
        </div>
        <div class="guide-actions">
          <el-button type="primary" @click="likeGuide">
            <el-icon><Thumb /></el-icon>
            点赞 ({{ selectedGuide.likes }})
          </el-button>
          <el-button @click="shareGuide">
            <el-icon><Share /></el-icon>
            分享
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search, Plus, More, ThumbUp, ChatDotRound } from '@element-plus/icons-vue'
import type { CareGuide, GuideCategory } from '@/types/plant'
import { guides } from '@/mock/guides'

// 状态
const activeCategory = ref<GuideCategory | 'all'>('all')
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const selectedGuide = ref<CareGuide | null>(null)

// 计算属性：过滤后的指南列表
const filteredGuides = computed(() => {
  return guides.filter(guide => {
    const matchesSearch = guide.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         guide.summary.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = activeCategory.value === 'all' || guide.category === activeCategory.value
    return matchesSearch && matchesCategory
  })
})

// 计算属性：总指南数量
const totalGuides = computed(() => filteredGuides.value.length)

// 计算属性：热门指南
const popularGuides = computed(() => {
  return [...guides]
    .sort((a, b) => b.views - a.views)
    .slice(0, 5)
})

// 方法：获取分类标签类型
const getCategoryType = (category: GuideCategory) => {
  const types = {
    watering: 'primary',
    lighting: 'success',
    soil: 'warning',
    fertilizer: 'info',
    pest: 'danger'
  }
  return types[category] || 'info'
}

// 方法：获取分类标签文本
const getCategoryLabel = (category: GuideCategory) => {
  const labels = {
    watering: '浇水技巧',
    lighting: '光照管理',
    soil: '土壤养护',
    fertilizer: '施肥方法',
    pest: '病虫害防治'
  }
  return labels[category] || '其他'
}

// 方法：处理分类选择
const handleCategorySelect = (category: GuideCategory | 'all') => {
  activeCategory.value = category
  currentPage.value = 1
}

// 方法：显示指南详情
const showGuideDetail = (guide: CareGuide) => {
  selectedGuide.value = guide
  dialogVisible.value = true
}

// 方法：处理分页
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

// 方法：点赞指南
const likeGuide = () => {
  if (selectedGuide.value) {
    selectedGuide.value.likes++
  }
}

// 方法：分享指南
const shareGuide = () => {
  // TODO: 实现分享功能
}
</script>

<style lang="scss" scoped>
.care-guides {
  padding: 20px;
}

.search-section {
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
  margin-bottom: 20px;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 20px;
}

.guide-card {
  margin-bottom: 20px;
}

.guide-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.guide-header h3 {
  margin: 0;
  font-size: 18px;
}

.guide-summary {
  color: #666;
  margin: 10px 0;
}

.guide-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px 0;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.guide-stats {
  display: flex;
  gap: 16px;
  color: #999;
}

.guide-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.guide-footer {
  margin-top: 15px;
  text-align: right;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.popular-guides {
  position: sticky;
  top: 20px;
}

.popular-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.popular-list li {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.popular-list li:last-child {
  border-bottom: none;
}

.popular-list .title {
  flex: 1;
  margin-right: 10px;
}

.popular-list .views {
  color: #999;
  font-size: 12px;
}

.guide-detail {
  padding: 20px;
}

.guide-detail .guide-header {
  margin-bottom: 20px;
}

.guide-content {
  line-height: 1.6;
  margin: 20px 0;
}

.guide-tags {
  margin: 20px 0;
}

.guide-tags .tag {
  margin-right: 8px;
}

.guide-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}
</style> 