document.addEventListener('DOMContentLoaded', function() {
    // 处理FAQ手风琴效果
    const accordionItems = document.querySelectorAll('.accordion-item');
    
    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');
        
        header.addEventListener('click', function() {
            // 关闭其他所有打开的项目
            accordionItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });
            
            // 切换当前项目的状态
            item.classList.toggle('active');
        });
    });
    
    // 默认打开第一个FAQ项目
    if (accordionItems.length > 0) {
        accordionItems[0].classList.add('active');
    }
    
    // 处理联系表单提交
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 获取表单数据
            const formData = new FormData(contactForm);
            const name = formData.get('name');
            const email = formData.get('email');
            const message = formData.get('message');
            
            // 在实际项目中，这里应该发送AJAX请求到后端API
            // 这里仅做演示，显示一个成功消息
            
            // 创建一个成功消息元素
            const successMessage = document.createElement('div');
            successMessage.className = 'success-message';
            successMessage.innerHTML = `
                <div class="success-icon">
                    <i class="fas fa-check"></i>
                </div>
                <h4>留言已发送！</h4>
                <p>感谢您的留言，${name}。我们会尽快回复您。</p>
            `;
            
            // 添加样式
            const style = document.createElement('style');
            style.textContent = `
                .success-message {
                    background: rgba(255, 255, 255, 0.8);
                    border-radius: var(--border-radius);
                    padding: 30px;
                    text-align: center;
                    animation: fadeIn 0.5s ease;
                }
                
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                
                .success-icon {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #4CAF50, #8BC34A);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin: 0 auto 20px;
                    color: white;
                    font-size: 1.5rem;
                }
                
                .success-message h4 {
                    font-size: 1.3rem;
                    color: var(--primary-color);
                    margin-bottom: 10px;
                }
                
                .success-message p {
                    color: var(--text-color);
                }
            `;
            document.head.appendChild(style);
            
            // 替换表单为成功消息
            contactForm.parentNode.replaceChild(successMessage, contactForm);
        });
    }
    
    // 添加团队成员卡片悬停效果
    const teamMembers = document.querySelectorAll('.team-member');
    teamMembers.forEach(member => {
        member.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.1)';
        });
        
        member.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // 添加宇宙背景动画效果
    const aboutHero = document.querySelector('.about-hero');
    if (aboutHero) {
        aboutHero.addEventListener('mousemove', function(e) {
            const cosmicCircle = document.querySelector('.cosmic-circle');
            if (cosmicCircle) {
                const x = e.clientX / window.innerWidth;
                const y = e.clientY / window.innerHeight;
                
                cosmicCircle.style.transform = `translate(${x * 20 - 10}px, ${y * 20 - 10}px) scale(1.05)`;
            }
        });
    }
    
    // 添加价值观卡片动画效果
    const valueCards = document.querySelectorAll('.value-card');
    valueCards.forEach((card, index) => {
        // 添加延迟出现动画
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * (index + 1));
    });
}); 