document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const fortuneForm = document.getElementById('fortuneForm');
    const resultSection = document.getElementById('resultSection');
    const userBirthInfo = document.getElementById('userBirthInfo');
    const analysisTypeInfo = document.getElementById('analysisTypeInfo');
    const saveResultBtn = document.getElementById('saveResultBtn');
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');
    
    // 天干地支数据
    const heavenlyStems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
    const earthlyBranches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
    
    // 五行颜色
    const fiveElementColors = {
        '木': { bg: 'linear-gradient(135deg, #4CAF50, #8BC34A)', color: 'white' },
        '火': { bg: 'linear-gradient(135deg, #FF5722, #FF9800)', color: 'white' },
        '土': { bg: 'linear-gradient(135deg, #795548, #A1887F)', color: 'white' },
        '金': { bg: 'linear-gradient(135deg, #FFC107, #FFEB3B)', color: 'black' },
        '水': { bg: 'linear-gradient(135deg, #2196F3, #03A9F4)', color: 'white' }
    };
    
    // 天干五行对应
    const stemElements = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    };
    
    // 地支五行对应
    const branchElements = {
        '子': '水', '丑': '土', '寅': '木', '卯': '木',
        '辰': '土', '巳': '火', '午': '火', '未': '土',
        '申': '金', '酉': '金', '戌': '土', '亥': '水'
    };
    
    // 分析类型中文映射
    const analysisTypeMap = {
        'comprehensive': '综合分析',
        'personality': '性格特质',
        'career': '事业财运',
        'relationship': '感情婚姻',
        'health': '健康状况'
    };
    
    // 表单提交事件
    fortuneForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 获取表单数据
        const formData = new FormData(fortuneForm);
        const birthDate = formData.get('birthDate');
        const birthTime = formData.get('birthTime');
        const gender = formData.get('gender');
        const birthPlace = formData.get('birthPlace');
        const analysisType = formData.get('analysisType');
        
        // 显示结果区域
        resultSection.style.display = 'block';
        
        // 滚动到结果区域
        resultSection.scrollIntoView({ behavior: 'smooth' });
        
        // 更新用户信息
        const birthDateTime = new Date(`${birthDate}T${birthTime}`);
        const formattedDate = birthDateTime.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        const formattedTime = birthDateTime.toLocaleTimeString('zh-CN', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        userBirthInfo.textContent = `${formattedDate} ${formattedTime} · ${gender === 'male' ? '男' : '女'} · ${birthPlace}`;
        analysisTypeInfo.textContent = analysisTypeMap[analysisType];
        
        // 模拟生成八字命盘
        generateBaziChart(birthDateTime);
        
        // 模拟AI分析过程
        simulateAIAnalysis(birthDateTime, gender, birthPlace, analysisType);
    });
    
    // 生成八字命盘
    function generateBaziChart(birthDateTime) {
        // 这里仅作演示，实际应用中需要根据真实的天干地支计算规则
        // 在实际项目中，应该使用专业的历法转换库来计算
        
        const year = birthDateTime.getFullYear();
        const month = birthDateTime.getMonth() + 1;
        const day = birthDateTime.getDate();
        const hour = birthDateTime.getHours();
        
        // 模拟计算天干地支（实际项目中需要准确计算）
        // 这里仅用随机值演示效果
        const yearStem = heavenlyStems[year % 10];
        const yearBranch = earthlyBranches[year % 12];
        const monthStem = heavenlyStems[(year * 2 + month) % 10];
        const monthBranch = earthlyBranches[(month + 2) % 12];
        const dayStem = heavenlyStems[(year + month + day) % 10];
        const dayBranch = earthlyBranches[(day + 6) % 12];
        const hourStem = heavenlyStems[(day * 2 + hour) % 10];
        const hourBranch = earthlyBranches[Math.floor(hour / 2) % 12];
        
        // 更新命盘显示
        updatePillar('yearPillar', yearStem, yearBranch);
        updatePillar('monthPillar', monthStem, monthBranch);
        updatePillar('dayPillar', dayStem, dayBranch);
        updatePillar('hourPillar', hourStem, hourBranch);
    }
    
    // 更新命盘柱子
    function updatePillar(pillarId, stem, branch) {
        const pillar = document.getElementById(pillarId);
        const stemElement = pillar.querySelector('.heavenly-stem');
        const branchElement = pillar.querySelector('.earthly-branch');
        
        // 设置天干
        stemElement.textContent = stem;
        const stemFiveElement = stemElements[stem];
        if (stemFiveElement && fiveElementColors[stemFiveElement]) {
            stemElement.style.background = fiveElementColors[stemFiveElement].bg;
            stemElement.style.color = fiveElementColors[stemFiveElement].color;
        }
        
        // 设置地支
        branchElement.textContent = branch;
        const branchFiveElement = branchElements[branch];
        if (branchFiveElement) {
            branchElement.style.borderColor = getComputedStyle(document.documentElement)
                .getPropertyValue('--primary-color');
        }
    }
    
    // 模拟AI分析过程
    function simulateAIAnalysis(birthDateTime, gender, birthPlace, analysisType) {
        // 获取结果内容区域
        const baziInterpretation = document.getElementById('baziInterpretation');
        const personalityAnalysis = document.getElementById('personalityAnalysis');
        const careerAnalysis = document.getElementById('careerAnalysis');
        const relationshipAnalysis = document.getElementById('relationshipAnalysis');
        const healthAnalysis = document.getElementById('healthAnalysis');
        const adviceAnalysis = document.getElementById('adviceAnalysis');
        
        // 显示加载动画
        baziInterpretation.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>AI正在分析您的命盘...</p>
            </div>
        `;
        
        // 清空其他分析区域
        personalityAnalysis.innerHTML = '';
        careerAnalysis.innerHTML = '';
        relationshipAnalysis.innerHTML = '';
        healthAnalysis.innerHTML = '';
        adviceAnalysis.innerHTML = '';
        
        // 模拟API请求延迟
        setTimeout(() => {
            // 在实际项目中，这里应该是向后端API发送请求获取分析结果
            // 这里仅用模拟数据演示
            
            // 命盘解读
            baziInterpretation.innerHTML = `
                <p>您的八字命盘为：${getRandomElement(heavenlyStems)}${getRandomElement(earthlyBranches)}年、${getRandomElement(heavenlyStems)}${getRandomElement(earthlyBranches)}月、${getRandomElement(heavenlyStems)}${getRandomElement(earthlyBranches)}日、${getRandomElement(heavenlyStems)}${getRandomElement(earthlyBranches)}时。</p>
                <p>您的命盘中五行分布为：金${getRandomInt(1, 3)}，木${getRandomInt(1, 3)}，水${getRandomInt(1, 3)}，火${getRandomInt(1, 3)}，土${getRandomInt(1, 3)}。其中${getRandomElement(['金', '木', '水', '火', '土'])}最为旺盛，而${getRandomElement(['金', '木', '水', '火', '土'])}相对较弱。</p>
                <p>您的日主天干为${getRandomElement(heavenlyStems)}，属${stemElements[getRandomElement(heavenlyStems)]}，${getRandomElement(['偏强', '偏弱', '中和'])}。</p>
            `;
            
            // 性格特质
            personalityAnalysis.innerHTML = `
                <p>您天生具有${getRandomElement(['敏锐的洞察力', '坚韧的意志力', '温和的性格', '领导才能', '创造力'])}，性格${getRandomElement(['开朗外向', '内敛沉稳', '理性冷静', '热情洋溢', '谨慎细致'])}。</p>
                <p>在人际交往中，您通常表现得${getRandomElement(['善解人意', '直率坦诚', '谨慎保守', '圆滑世故', '独立自主'])}，善于${getRandomElement(['倾听他人', '表达自己', '协调关系', '解决冲突', '建立联系'])}。</p>
                <p>您的思维方式偏向${getRandomElement(['逻辑分析', '感性直觉', '实用主义', '创新思考', '系统全面'])}，在面对挑战时，往往采取${getRandomElement(['积极主动', '谨慎观望', '灵活变通', '坚持不懈', '寻求帮助'])}的态度。</p>
            `;
            
            // 事业财运
            careerAnalysis.innerHTML = `
                <p>在事业方面，您适合从事与${getRandomElement(['管理', '技术', '艺术', '服务', '研究', '教育'])}相关的工作，特别是在${getRandomElement(['金融', '科技', '医疗', '教育', '艺术', '服务'])}领域有较大发展空间。</p>
                <p>您的财运在${getRandomElement(['30-35岁', '35-40岁', '40-45岁', '45-50岁'])}期间将迎来高峰，但需要注意${getRandomElement(['投资风险', '财务管理', '合作伙伴', '市场变化'])}。</p>
                <p>建议您在职业发展中注重${getRandomElement(['专业技能提升', '人脉拓展', '领导能力培养', '创新思维', '团队协作'])}，这将有助于您的长期发展。</p>
            `;
            
            // 感情婚姻
            relationshipAnalysis.innerHTML = `
                <p>在感情方面，您${getRandomElement(['重视情感交流', '注重精神契合', '追求稳定关系', '渴望浪漫体验', '强调相互理解'])}，与${getRandomElement(['水', '火', '木', '金', '土'])}相属性的人缘分较深。</p>
                <p>您的婚姻运势在${getRandomElement(['25-30岁', '30-35岁', '35-40岁'])}阶段最为顺遂，理想的伴侣应具备${getRandomElement(['理解包容', '聪明才智', '温柔体贴', '坚强可靠', '幽默风趣'])}的特质。</p>
                <p>在维系感情关系时，建议您多关注${getRandomElement(['沟通方式', '情感表达', '生活习惯', '价值观差异', '未来规划'])}，以增进彼此理解和感情深度。</p>
            `;
            
            // 健康状况
            healthAnalysis.innerHTML = `
                <p>从命理角度看，您需要特别关注${getRandomElement(['消化系统', '呼吸系统', '心脑血管', '骨骼关节', '内分泌系统'])}的健康，建议定期检查。</p>
                <p>您的体质偏向${getRandomElement(['阳盛', '阴虚', '气虚', '湿热', '寒凉'])}，在日常保健中应注意${getRandomElement(['饮食规律', '适量运动', '充足睡眠', '情绪管理', '环境适应'])}。</p>
                <p>建议您选择${getRandomElement(['游泳', '瑜伽', '慢跑', '太极', '力量训练'])}等适合您体质的运动方式，并在饮食上注意${getRandomElement(['清淡饮食', '营养均衡', '少食多餐', '温热食物', '新鲜蔬果'])}。</p>
            `;
            
            // 运势建议
            adviceAnalysis.innerHTML = `
                <p>根据您的八字命盘，建议您在事业上把握${getRandomElement(['2024年', '2025年', '2026年'])}的发展机会，特别是在${getRandomElement(['春季', '夏季', '秋季', '冬季'])}可能出现重要转机。</p>
                <p>在人际关系方面，宜${getRandomElement(['广结善缘', '慎重选择', '加强沟通', '保持距离', '真诚以待'])}，避免与${getRandomElement(['金', '木', '水', '火', '土'])}相属性的人产生冲突。</p>
                <p>在个人发展上，建议您加强${getRandomElement(['专业知识', '沟通能力', '领导才能', '创新思维', '情绪管理'])}的培养，这将有助于您更好地把握未来机遇。</p>
                <p>吉祥物品：${getRandomElement(['玉石', '水晶', '红绳', '铜饰', '木雕'])}；幸运色：${getRandomElement(['红色', '蓝色', '绿色', '黄色', '白色'])}；幸运数字：${getRandomInt(1, 9)}。</p>
            `;
            
        }, 3000); // 模拟3秒延迟
    }
    
    // 新的分析按钮点击事件
    newAnalysisBtn.addEventListener('click', function() {
        // 隐藏结果区域
        resultSection.style.display = 'none';
        
        // 重置表单
        fortuneForm.reset();
        
        // 滚动到表单区域
        fortuneForm.scrollIntoView({ behavior: 'smooth' });
    });
    
    // 保存结果按钮点击事件
    saveResultBtn.addEventListener('click', function() {
        // 在实际项目中，这里应该实现保存功能
        // 可以是生成PDF、发送邮件或保存到用户账户等
        alert('分析结果已保存！在实际项目中，这里可以实现导出PDF或发送到邮箱等功能。');
    });
    
    // 辅助函数：从数组中随机获取一个元素
    function getRandomElement(array) {
        return array[Math.floor(Math.random() * array.length)];
    }
    
    // 辅助函数：获取指定范围内的随机整数
    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
}); 