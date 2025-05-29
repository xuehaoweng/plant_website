<template>
  <div class="home">
    <!-- 顶部横幅 -->
    <div class="banner">
      <div class="banner-content">
        <h1>欢迎来到园艺之家</h1>
        <p>在这里，您可以找到专业的园艺知识，分享种植经验，解答园艺问题</p>
        <el-button type="primary" size="large" @click="startExploring">
          开始探索
        </el-button>
      </div>
    </div>

    <!-- 功能区块 -->
    <div class="features">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="feature-card">
            <template #header>
              <div class="card-header">
                <el-icon><Plant /></el-icon>
                <span>植物图鉴</span>
              </div>
            </template>
            <div class="card-content">
              探索丰富的植物数据库，了解各种植物的特性和养护方法
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="feature-card">
            <template #header>
              <div class="card-header">
                <el-icon><ChatDotRound /></el-icon>
                <span>问答社区</span>
              </div>
            </template>
            <div class="card-content">
              向园艺专家提问，分享您的种植经验，解决园艺难题
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="feature-card">
            <template #header>
              <div class="card-header">
                <el-icon><Collection /></el-icon>
                <span>养护指南</span>
              </div>
            </template>
            <div class="card-content">
              获取专业的植物养护知识，让您的植物茁壮成长
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 热门问题 -->
    <div class="hot-questions">
      <h2>热门问题</h2>
      <el-card v-for="question in hotQuestions" :key="question.id" class="question-card">
        <div class="question-header">
          <span class="question-title">{{ question.title }}</span>
          <el-tag size="small" :type="question.status === 'solved' ? 'success' : 'warning'">
            {{ question.status === 'solved' ? '已解决' : '待解决' }}
          </el-tag>
        </div>
        <div class="question-content">{{ question.content }}</div>
        <div class="question-footer">
          <span class="author">{{ question.author }}</span>
          <span class="time">{{ question.time }}</span>
          <span class="views">
            <el-icon><View /></el-icon>
            {{ question.views }}
          </span>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Plant, ChatDotRound, Collection, View } from '@element-plus/icons-vue'

const router = useRouter()

const startExploring = () => {
  router.push('/plants')
}

// 模拟热门问题数据
const hotQuestions = ref([
  {
    id: 1,
    title: '多肉植物叶子发黄怎么办？',
    content: '最近发现我的多肉植物叶子开始发黄，不知道是什么原因...',
    author: '绿植爱好者',
    time: '2小时前',
    views: 156,
    status: 'solved'
  },
  {
    id: 2,
    title: '室内植物如何正确浇水？',
    content: '想请教一下室内植物浇水的正确方法，特别是不同季节的浇水频率...',
    author: '园艺新手',
    time: '5小时前',
    views: 89,
    status: 'pending'
  }
])
</script>

<style lang="scss" scoped>
.home {
  .banner {
    height: 400px;
    background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
                url('@/assets/banner.svg') center/cover;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
    margin-bottom: 40px;

    .banner-content {
      max-width: 800px;
      padding: 0 20px;

      h1 {
        font-size: 2.5em;
        margin-bottom: 20px;
      }

      p {
        font-size: 1.2em;
        margin-bottom: 30px;
      }
    }
  }

  .features {
    max-width: 1200px;
    margin: 0 auto 40px;
    padding: 0 20px;

    .feature-card {
      height: 100%;

      .card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.2em;
        font-weight: bold;
      }

      .card-content {
        color: #666;
        line-height: 1.6;
      }
    }
  }

  .hot-questions {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;

    h2 {
      margin-bottom: 20px;
      font-size: 1.8em;
    }

    .question-card {
      margin-bottom: 20px;

      .question-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;

        .question-title {
          font-size: 1.2em;
          font-weight: bold;
        }
      }

      .question-content {
        color: #666;
        margin-bottom: 10px;
      }

      .question-footer {
        display: flex;
        gap: 20px;
        color: #999;
        font-size: 0.9em;

        .views {
          display: flex;
          align-items: center;
          gap: 4px;
        }
      }
    }
  }
}
</style> 