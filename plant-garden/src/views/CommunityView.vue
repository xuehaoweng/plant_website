<template>
  <div class="community-page">
    <div class="page-header">
      <h1>社区交流</h1>
      <p>与园艺爱好者分享经验，解答疑惑</p>
    </div>

    <div class="main-content">
      <!-- 左侧帖子列表 -->
      <div class="posts-section">
        <div class="posts-header">
          <el-input
            v-model="searchQuery"
            placeholder="搜索帖子..."
            class="search-input"
            :prefix-icon="Search"
          />
          <el-button type="primary" @click="showNewPostDialog">
            <el-icon><Plus /></el-icon> 发布新帖
          </el-button>
        </div>

        <div class="posts-list">
          <el-card v-for="post in filteredPosts" :key="post.id" class="post-card">
            <div class="post-header">
              <div class="author-info">
                <el-avatar :size="40" :src="post.author.avatar" />
                <div class="author-details">
                  <span class="author-name">{{ post.author.name }}</span>
                  <span class="post-time">{{ post.time }}</span>
                </div>
              </div>
              <el-dropdown>
                <el-button type="text">
                  <el-icon><More /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item>收藏</el-dropdown-item>
                    <el-dropdown-item>分享</el-dropdown-item>
                    <el-dropdown-item v-if="post.author.id === currentUser?.id">删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-content">{{ post.content }}</p>
            <div class="post-images" v-if="post.images?.length">
              <el-image
                v-for="(image, index) in post.images"
                :key="index"
                :src="image"
                :preview-src-list="post.images"
                fit="cover"
                class="post-image"
              />
            </div>
            <div class="post-footer">
              <div class="post-actions">
                <el-button type="text" @click="handleLike(post)">
                  <el-icon><Star /></el-icon>
                  {{ post.likes }}
                </el-button>
                <el-button type="text" @click="handleComment(post)">
                  <el-icon><ChatDotRound /></el-icon>
                  {{ post.comments }}
                </el-button>
              </div>
              <el-tag size="small" :type="getTagType(post.tag)">
                {{ getTagLabel(post.tag) }}
              </el-tag>
            </div>
          </el-card>
        </div>

        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 30, 50]"
            :total="totalPosts"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>

      <!-- 右侧边栏 -->
      <div class="sidebar">
        <!-- 热门话题 -->
        <el-card class="hot-topics">
          <template #header>
            <div class="card-header">
              <span>热门话题</span>
            </div>
          </template>
          <ul class="topics-list">
            <li v-for="topic in hotTopics" :key="topic.id">
              <span class="topic-title">{{ topic.title }}</span>
              <span class="topic-count">{{ topic.count }} 讨论</span>
            </li>
          </ul>
        </el-card>

        <!-- 活跃用户 -->
        <el-card class="active-users">
          <template #header>
            <div class="card-header">
              <span>活跃用户</span>
            </div>
          </template>
          <ul class="users-list">
            <li v-for="user in activeUsers" :key="user.id">
              <el-avatar :size="32" :src="user.avatar" />
              <span class="user-name">{{ user.name }}</span>
              <span class="user-posts">{{ user.posts }} 帖子</span>
            </li>
          </ul>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search, Plus, More, Star, ChatDotRound } from '@element-plus/icons-vue'
import { useCoinStore } from '@/stores/coin'
// import type { TransactionType, TransactionSource } from '@/types/coin'

// 状态
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const currentUser = ref({
  id: 1,
  name: '当前用户',
  avatar: '/images/avatars/user1.jpg'
})

// 模拟帖子数据
const posts = ref([
  {
    id: 1,
    title: '我的绿萝养护经验分享',
    content: '经过一年的养护，我的绿萝长得非常茂盛，分享一下我的养护经验...',
    author: {
      id: 1,
      name: '园艺达人',
      avatar: '/images/avatars/user1.jpg'
    },
    time: '2024-01-15 14:30',
    likes: 128,
    comments: 32,
    tag: 'experience',
    images: [
      '/images/posts/luluo1.jpg',
      '/images/posts/luluo2.jpg'
    ]
  },
  {
    id: 2,
    title: '求助：多肉植物叶子发软怎么办？',
    content: '最近发现我的多肉植物叶子开始发软，不知道是什么原因，求大神指点...',
    author: {
      id: 2,
      name: '多肉爱好者',
      avatar: '/images/avatars/user2.jpg'
    },
    time: '2024-01-14 09:15',
    likes: 45,
    comments: 28,
    tag: 'question'
  }
])

// 模拟热门话题
const hotTopics = ref([
  { id: 1, title: '室内植物养护技巧', count: 156 },
  { id: 2, title: '多肉植物繁殖方法', count: 98 },
  { id: 3, title: '植物病虫害防治', count: 87 }
])

// 模拟活跃用户
const activeUsers = ref([
  { id: 1, name: '园艺达人', avatar: '/images/avatars/user1.jpg', posts: 128 },
  { id: 2, name: '多肉爱好者', avatar: '/images/avatars/user2.jpg', posts: 95 },
  { id: 3, name: '植物医生', avatar: '/images/avatars/user3.jpg', posts: 76 }
])

// 计算属性：过滤后的帖子列表
const filteredPosts = computed(() => {
  return posts.value.filter(post => {
    return post.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
           post.content.toLowerCase().includes(searchQuery.value.toLowerCase())
  })
})

// 计算属性：总帖子数量
const totalPosts = computed(() => filteredPosts.value.length)

// 获取标签类型
const getTagType = (tag: string) => {
  const types = {
    experience: 'success',
    question: 'warning',
    share: 'info'
  }
  return types[tag as keyof typeof types] || 'info'
}

// 获取标签文本
const getTagLabel = (tag: string) => {
  const labels = {
    experience: '经验分享',
    question: '求助',
    share: '分享'
  }
  return labels[tag as keyof typeof labels] || '其他'
}

const coinStore = useCoinStore()

// 点赞帖子
const handleLike = (post: any) => {
  post.likes++
  
  coinStore.addTransaction(
    currentUser.value.id,
    'earn',
    1,
    'post',
    '帖子获得点赞',
    new Date().toISOString()
  )
}

// 发表评论
const handleComment = (post: any) => {
  post.comments++
  
  coinStore.addTransaction(
    currentUser.value.id,
    'earn',
    5,
    'post',
    '发表评论',
    new Date().toISOString()
  )
}

// 显示新帖对话框
const showNewPostDialog = () => {
  // TODO: 实现发帖功能
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
.community-page {
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

.main-content {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 20px;
}

.posts-section {
  .posts-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    .search-input {
      width: 300px;
    }
  }
}

.post-card {
  margin-bottom: 20px;

  .post-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;

    .author-info {
      display: flex;
      align-items: center;
      gap: 10px;

      .author-details {
        display: flex;
        flex-direction: column;

        .author-name {
          font-weight: bold;
        }

        .post-time {
          font-size: 12px;
          color: #999;
        }
      }
    }
  }

  .post-title {
    font-size: 18px;
    margin-bottom: 10px;
  }

  .post-content {
    color: #666;
    margin-bottom: 15px;
    line-height: 1.6;
  }

  .post-images {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
    margin-bottom: 15px;

    .post-image {
      width: 100%;
      height: 150px;
      border-radius: 4px;
    }
  }

  .post-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .post-actions {
      display: flex;
      gap: 20px;
    }
  }
}

.sidebar {
  .el-card {
    margin-bottom: 20px;
  }

  .card-header {
    font-weight: bold;
  }
}

.topics-list {
  list-style: none;
  padding: 0;
  margin: 0;

  li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #eee;

    &:last-child {
      border-bottom: none;
    }

    .topic-title {
      color: #333;
    }

    .topic-count {
      color: #999;
      font-size: 12px;
    }
  }
}

.users-list {
  list-style: none;
  padding: 0;
  margin: 0;

  li {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid #eee;

    &:last-child {
      border-bottom: none;
    }

    .user-name {
      flex: 1;
      color: #333;
    }

    .user-posts {
      color: #999;
      font-size: 12px;
    }
  }
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
</style> 