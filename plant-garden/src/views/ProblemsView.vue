<template>
  <div class="problems-page">
    <div class="page-header">
      <h1>常见问题</h1>
      <p>解答您在植物养护过程中遇到的常见问题</p>
    </div>

    <div class="search-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索问题..."
        class="search-input"
        :prefix-icon="Search"
      />
      <el-select v-model="selectedCategory" placeholder="选择分类" class="category-select">
        <el-option label="全部" value="all" />
        <el-option label="病虫害" value="pest" />
        <el-option label="浇水" value="watering" />
        <el-option label="光照" value="lighting" />
        <el-option label="土壤" value="soil" />
        <el-option label="施肥" value="fertilizer" />
      </el-select>
    </div>

    <div class="problems-list">
      <el-collapse v-model="activeNames">
        <el-collapse-item
          v-for="problem in filteredProblems"
          :key="problem.id"
          :name="problem.id"
        >
          <template #title>
            <div class="problem-title">
              <h3>{{ problem.title }}</h3>
              <el-tag size="small" :type="getCategoryType(problem.category)">
                {{ getCategoryLabel(problem.category) }}
              </el-tag>
            </div>
          </template>
          <div class="problem-content">
            <p class="description">{{ problem.description }}</p>
            <div class="solution">
              <h4>解决方案：</h4>
              <p>{{ problem.solution }}</p>
            </div>
            <div class="prevention">
              <h4>预防措施：</h4>
              <p>{{ problem.prevention }}</p>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 30, 50]"
        :total="totalProblems"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'

// 状态
const searchQuery = ref('')
const selectedCategory = ref('all')
const activeNames = ref<string[]>([])
const currentPage = ref(1)
const pageSize = ref(10)

// 模拟问题数据
const problems = ref([
  {
    id: 1,
    title: '植物叶子发黄怎么办？',
    category: 'watering',
    description: '最近发现植物的叶子开始发黄，不知道是什么原因。',
    solution: '叶子发黄通常是由于浇水不当或光照不足导致的。建议检查土壤湿度，确保浇水适量，并调整植物位置以获得适当的光照。',
    prevention: '定期检查土壤湿度，保持适当的浇水频率，确保植物获得充足的光照。'
  },
  {
    id: 2,
    title: '如何防治植物病虫害？',
    category: 'pest',
    description: '植物叶片上出现白色粉末状物质，可能是白粉病。',
    solution: '可以使用专门的杀菌剂进行喷洒，同时保持通风，避免过度浇水。',
    prevention: '定期检查植物健康状况，保持适当的通风和光照，避免过度浇水。'
  }
])

// 计算属性：过滤后的问题列表
const filteredProblems = computed(() => {
  return problems.value.filter(problem => {
    const matchesSearch = problem.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         problem.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value === 'all' || problem.category === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

// 计算属性：总问题数量
const totalProblems = computed(() => filteredProblems.value.length)

// 获取分类标签类型
const getCategoryType = (category: string) => {
  const types = {
    pest: 'danger',
    watering: 'primary',
    lighting: 'success',
    soil: 'warning',
    fertilizer: 'info'
  }
  return types[category as keyof typeof types] || 'info'
}

// 获取分类标签文本
const getCategoryLabel = (category: string) => {
  const labels = {
    pest: '病虫害',
    watering: '浇水',
    lighting: '光照',
    soil: '土壤',
    fertilizer: '施肥'
  }
  return labels[category as keyof typeof labels] || '其他'
}

// 处理分页
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}
</script>

<style lang="scss" scoped>
.problems-page {
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

  p {
    color: #666;
    font-size: 16px;
  }
}

.search-section {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;

  .search-input {
    width: 300px;
  }

  .category-select {
    width: 200px;
  }
}

.problems-list {
  margin-bottom: 30px;

  .problem-title {
    display: flex;
    align-items: center;
    gap: 10px;

    h3 {
      margin: 0;
      font-size: 16px;
    }
  }

  .problem-content {
    padding: 10px 0;

    .description {
      color: #666;
      margin-bottom: 15px;
    }

    .solution, .prevention {
      margin-top: 15px;

      h4 {
        color: #333;
        margin-bottom: 10px;
      }

      p {
        color: #666;
        line-height: 1.6;
      }
    }
  }
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
</style> 