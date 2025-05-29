import type { CareGuide } from '@/types/plant'

export const guides: CareGuide[] = [
  {
    id: 1,
    title: '室内植物浇水完全指南',
    category: 'watering',
    summary: '详细介绍不同季节、不同植物的浇水频率和注意事项，帮助您掌握正确的浇水技巧。',
    content: `
      <h3>浇水的基本原则</h3>
      <p>浇水是植物养护中最基本的环节，但也是最容易出错的环节。以下是几个基本原则：</p>
      <ul>
        <li>观察土壤湿度，不要盲目按固定频率浇水</li>
        <li>不同季节需要调整浇水频率</li>
        <li>不同植物对水分的需求不同</li>
      </ul>
      <h3>常见浇水错误</h3>
      <p>以下是新手常见的浇水错误：</p>
      <ul>
        <li>过度浇水导致烂根</li>
        <li>浇水不均匀</li>
        <li>使用不适当的水质</li>
      </ul>
    `,
    author: {
      id: 1,
      name: '园艺专家',
      avatar: 'https://picsum.photos/id/110/400/300'
    },
    date: '2024-01-15',
    views: 1234,
    likes: 89,
    tags: ['浇水', '室内植物', '新手指南']
  },
  {
    id: 2,
    title: '植物光照管理指南',
    category: 'lighting',
    summary: '了解不同植物对光照的需求，掌握正确的光照管理方法。',
    content: `
      <h3>光照的重要性</h3>
      <p>光照是植物进行光合作用的必要条件，对植物的生长至关重要：</p>
      <ul>
        <li>光照不足会导致植物徒长</li>
        <li>光照过强会灼伤叶片</li>
        <li>不同植物对光照的需求不同</li>
      </ul>
      <h3>光照管理技巧</h3>
      <p>以下是几个实用的光照管理技巧：</p>
      <ul>
        <li>根据植物特性选择合适的位置</li>
        <li>定期转动花盆，使植物均匀受光</li>
        <li>使用遮阳网调节光照强度</li>
      </ul>
    `,
    author: {
      id: 1,
      name: '园艺专家',
      avatar: 'https://picsum.photos/id/110/400/300'
    },
    date: '2024-01-20',
    views: 986,
    likes: 76,
    tags: ['光照', '植物养护', '室内植物']
  },
  {
    id: 3,
    title: '植物土壤养护指南',
    category: 'soil',
    summary: '了解土壤的重要性，掌握正确的土壤养护方法。',
    content: `
      <h3>土壤的重要性</h3>
      <p>土壤是植物生长的基础，良好的土壤环境对植物生长至关重要：</p>
      <ul>
        <li>提供植物生长所需的养分</li>
        <li>保持适当的水分和空气</li>
        <li>为根系提供支撑</li>
      </ul>
      <h3>土壤养护方法</h3>
      <p>以下是几个重要的土壤养护方法：</p>
      <ul>
        <li>定期松土，保持土壤疏松</li>
        <li>适时更换土壤，避免土壤板结</li>
        <li>根据植物需求选择合适的土壤类型</li>
      </ul>
    `,
    author: {
      id: 1,
      name: '园艺专家',
      avatar: 'https://picsum.photos/id/110/400/300'
    },
    date: '2024-01-25',
    views: 856,
    likes: 65,
    tags: ['土壤', '植物养护', '新手指南']
  }
] 