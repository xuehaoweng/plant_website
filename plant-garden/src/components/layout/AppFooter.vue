<template>
  <el-footer class="app-footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>关于我们</h3>
          <p>绿居园艺致力于为园艺爱好者提供专业的植物养护知识和交流平台。</p>
        </div>
        <div class="footer-section">
          <h3>快速链接</h3>
          <ul>
            <li><router-link to="/plants">植物分类</router-link></li>
            <li><router-link to="/care-guides">养护指南</router-link></li>
            <li><router-link to="/problems">常见问题</router-link></li>
            <li><router-link to="/community">社区交流</router-link></li>
          </ul>
        </div>
        <div class="footer-section">
          <h3>联系我们</h3>
          <ul>
            <li>邮箱：contact@greenhome.com</li>
            <li>电话：400-123-4567</li>
            <li>地址：北京市朝阳区园艺路123号</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2024 绿居园艺. All rights reserved.</p>
      </div>
    </div>
  </el-footer>
</template>

<style lang="scss" scoped>
.app-footer {
  background-color: #f5f5f5;
  padding: 40px 0 20px;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  margin-bottom: 30px;
}

.footer-section {
  h3 {
    font-size: 18px;
    margin-bottom: 15px;
    color: #333;
  }

  p {
    color: #666;
    line-height: 1.6;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;

    li {
      margin-bottom: 10px;
      color: #666;

      a {
        color: #666;
        text-decoration: none;
        transition: color 0.3s;

        &:hover {
          color: var(--el-color-primary);
        }
      }
    }
  }
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #ddd;
  color: #999;
}
</style> 