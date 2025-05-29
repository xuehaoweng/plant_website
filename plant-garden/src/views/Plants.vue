<template>
  <div class="plants-page">
    <!-- 搜索和筛选区域 -->
    <div class="search-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索植物名称、特性..."
        class="search-input"
        :prefix-icon="Search"
      />
      <el-select v-model="selectedCategory" placeholder="选择分类" class="category-select">
        <el-option
          v-for="category in categories"
          :key="category.value"
          :label="category.label"
          :value="category.value"
        />
      </el-select>
      <el-select v-model="selectedDifficulty" placeholder="养护难度" class="difficulty-select">
        <el-option
          v-for="level in difficultyLevels"
          :key="level.value"
          :label="level.label"
          :value="level.value"
        />
      </el-select>
    </div>

    <!-- 植物列表 -->
    <div class="plants-grid">
      <el-card
        v-for="plant in filteredPlants"
        :key="plant.id"
        class="plant-card"
        @click="showPlantDetail(plant)"
      >
        <img :src="plant.image" :alt="plant.name" class="plant-image" />
        <div class="plant-info">
          <h3>{{ plant.name }}</h3>
          <p class="scientific-name">{{ plant.scientificName }}</p>
          <div class="plant-tags">
            <el-tag size="small" :type="getDifficultyType(plant.difficulty)">
              {{ getDifficultyLabel(plant.difficulty) }}
            </el-tag>
            <el-tag size="small" type="success">{{ plant.category }}</el-tag>
          </div>
          <p class="plant-description">{{ plant.description }}</p>
        </div>
      </el-card>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="totalPlants"
        :page-sizes="[12, 24, 36, 48]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 植物详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="selectedPlant?.name"
      width="70%"
      class="plant-detail-dialog"
    >
      <div v-if="selectedPlant" class="plant-detail">
        <div class="detail-header">
          <img :src="selectedPlant.image" :alt="selectedPlant.name" class="detail-image" />
          <div class="detail-info">
            <h2>{{ selectedPlant.name }}</h2>
            <p class="scientific-name">{{ selectedPlant.scientificName }}</p>
            <div class="detail-tags">
              <el-tag size="small" :type="getDifficultyType(selectedPlant.difficulty)">
                {{ getDifficultyLabel(selectedPlant.difficulty) }}
              </el-tag>
              <el-tag size="small" type="success">{{ selectedPlant.category }}</el-tag>
            </div>
          </div>
        </div>
        
        <el-tabs>
          <el-tab-pane label="基本信息">
            <div class="detail-content">
              <p>{{ selectedPlant.description }}</p>
              <h4>生长习性</h4>
              <ul>
                <li>光照需求：{{ selectedPlant.light }}</li>
                <li>水分需求：{{ selectedPlant.water }}</li>
                <li>适宜温度：{{ selectedPlant.temperature }}</li>
                <li>土壤要求：{{ selectedPlant.soil }}</li>
              </ul>
            </div>
          </el-tab-pane>
          <el-tab-pane label="养护指南">
            <div class="care-guide">
              <h4>日常养护</h4>
              <p>{{ selectedPlant.careGuide }}</p>
              <h4>常见问题</h4>
              <ul>
                <li v-for="(problem, index) in selectedPlant.commonProblems" :key="index">
                  {{ problem }}
                </li>
              </ul>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'
import type { Plant, PlantCategory, DifficultyLevel } from '@/types/plant'
import { plants } from '@/mock/plants'

// 搜索和筛选状态
const searchQuery = ref('')
const selectedCategory = ref<PlantCategory | ''>('')
const selectedDifficulty = ref<DifficultyLevel | ''>('')
const currentPage = ref(1)
const pageSize = ref(12)
const dialogVisible = ref(false)
const selectedPlant = ref<Plant | null>(null)

// 分类选项
const categories = [
  { label: '观叶植物', value: 'foliage' as PlantCategory },
  { label: '观花植物', value: 'flowering' as PlantCategory },
  { label: '多肉植物', value: 'succulent' as PlantCategory },
  { label: '水生植物', value: 'aquatic' as PlantCategory },
  { label: '草本植物', value: 'herb' as PlantCategory }
]

// 难度等级
const difficultyLevels = [
  { label: '简单', value: 'easy' as DifficultyLevel },
  { label: '中等', value: 'medium' as DifficultyLevel },
  { label: '困难', value: 'hard' as DifficultyLevel }
]

// 计算属性：过滤后的植物列表
const filteredPlants = computed(() => {
  return plants.filter(plant => {
    const matchesSearch = plant.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         plant.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = !selectedCategory.value || plant.category === selectedCategory.value
    const matchesDifficulty = !selectedDifficulty.value || plant.difficulty === selectedDifficulty.value
    return matchesSearch && matchesCategory && matchesDifficulty
  })
})

// 计算属性：总植物数量
const totalPlants = computed(() => filteredPlants.value.length)

// 方法：获取难度标签类型
const getDifficultyType = (difficulty: DifficultyLevel) => {
  const types = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger'
  }
  return types[difficulty] || 'info'
}

// 方法：获取难度标签文本
const getDifficultyLabel = (difficulty: DifficultyLevel) => {
  const labels = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return labels[difficulty] || '未知'
}

// 方法：显示植物详情
const showPlantDetail = (plant: Plant) => {
  selectedPlant.value = plant
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
</script>

<style lang="scss" scoped>
.plants-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;

  .search-section {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;

    .search-input {
      flex: 1;
    }

    .category-select,
    .difficulty-select {
      width: 150px;
    }
  }

  .plants-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 30px;

    .plant-card {
      cursor: pointer;
      transition: transform 0.3s ease;

      &:hover {
        transform: translateY(-5px);
      }

      .plant-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 4px;
      }

      .plant-info {
        padding: 15px;

        h3 {
          margin: 0 0 5px;
          font-size: 1.2em;
        }

        .scientific-name {
          color: #666;
          font-style: italic;
          margin-bottom: 10px;
        }

        .plant-tags {
          display: flex;
          gap: 10px;
          margin-bottom: 10px;
        }

        .plant-description {
          color: #666;
          font-size: 0.9em;
          line-height: 1.4;
        }
      }
    }
  }

  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 30px;
  }
}

.plant-detail-dialog {
  .plant-detail {
    .detail-header {
      display: flex;
      gap: 20px;
      margin-bottom: 20px;

      .detail-image {
        width: 300px;
        height: 300px;
        object-fit: cover;
        border-radius: 4px;
      }

      .detail-info {
        flex: 1;

        h2 {
          margin: 0 0 10px;
        }

        .scientific-name {
          color: #666;
          font-style: italic;
          margin-bottom: 15px;
        }

        .detail-tags {
          display: flex;
          gap: 10px;
        }
      }
    }

    .detail-content,
    .care-guide {
      h4 {
        margin: 20px 0 10px;
        color: #333;
      }

      ul {
        padding-left: 20px;
        color: #666;

        li {
          margin-bottom: 5px;
        }
      }
    }
  }
}
</style> 