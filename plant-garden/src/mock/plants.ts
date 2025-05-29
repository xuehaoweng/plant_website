import type { Plant } from '@/types/plant'

export const plants: Plant[] = [
  {
    id: 1,
    name: '绿萝',
    scientificName: 'Epipremnum aureum',
    category: 'foliage',
    difficulty: 'easy',
    image: 'https://picsum.photos/id/110/400/300',
    description: '绿萝是一种常见的室内观叶植物，具有极强的适应性，适合新手种植。',
    light: '散射光',
    water: '中等',
    temperature: '18-28℃',
    soil: '疏松透气',
    careGuide: '绿萝喜欢温暖湿润的环境，需要保持土壤湿润但不要积水。定期擦拭叶片可以保持叶片光泽。',
    commonProblems: [
      '叶子发黄：可能是浇水过多或光照不足',
      '叶子发黑：可能是温度过低或浇水过多',
      '生长缓慢：可能是光照不足或营养不足'
    ]
  },
  {
    id: 2,
    name: '多肉植物',
    scientificName: 'Succulent Plants',
    category: 'succulent',
    difficulty: 'easy',
    image: 'https://picsum.photos/id/110/400/300',
    description: '多肉植物以其独特的外形和易于养护的特点受到欢迎。',
    light: '充足阳光',
    water: '少量',
    temperature: '15-30℃',
    soil: '砂质土',
    careGuide: '多肉植物喜欢干燥的环境，浇水要适量，避免积水。需要充足的光照，但夏季要避免暴晒。',
    commonProblems: [
      '徒长：光照不足',
      '烂根：浇水过多',
      '叶片发软：缺水'
    ]
  },
  {
    id: 3,
    name: '君子兰',
    scientificName: 'Clivia miniata',
    category: 'flowering',
    difficulty: 'medium',
    image: 'https://picsum.photos/id/110/400/300',
    description: '君子兰是一种优雅的观花植物，以其鲜艳的花朵和优雅的叶片著称。',
    light: '散射光',
    water: '中等',
    temperature: '15-25℃',
    soil: '肥沃疏松',
    careGuide: '君子兰喜欢温暖湿润的环境，需要定期施肥，保持土壤湿润但不积水。',
    commonProblems: [
      '不开花：光照不足或营养不足',
      '叶片发黄：浇水不当或光照过强',
      '生长缓慢：温度不适或营养不足'
    ]
  }
] 