document.addEventListener('DOMContentLoaded', function() {
    // 添加平滑滚动效果
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 添加导航栏滚动效果
    const header = document.querySelector('header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // 向下滚动
            header.style.transform = 'translateY(-100%)';
        } else {
            // 向上滚动
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // 添加宇宙背景动画效果
    const heroSection = document.querySelector('.hero');
    if (heroSection) {
        heroSection.addEventListener('mousemove', function(e) {
            const cosmicCircle = document.querySelector('.cosmic-circle');
            if (cosmicCircle) {
                const x = e.clientX / window.innerWidth;
                const y = e.clientY / window.innerHeight;
                
                cosmicCircle.style.transform = `translate(${x * 20 - 10}px, ${y * 20 - 10}px) scale(1.05)`;
            }
        });
    }
    
    // 添加特性卡片悬停效果
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 8px 32px 0 rgba(0, 0, 0, 0.1)';
        });
    });
    
    // 添加响应式导航菜单
    const createMobileMenu = () => {
        if (window.innerWidth <= 768 && !document.querySelector('.mobile-menu-toggle')) {
            const nav = document.querySelector('nav');
            const header = document.querySelector('header');
            
            // 创建移动菜单按钮
            const menuToggle = document.createElement('div');
            menuToggle.className = 'mobile-menu-toggle';
            menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
            header.appendChild(menuToggle);
            
            // 添加菜单切换事件
            menuToggle.addEventListener('click', function() {
                nav.classList.toggle('active');
                this.innerHTML = nav.classList.contains('active') ? 
                    '<i class="fas fa-times"></i>' : 
                    '<i class="fas fa-bars"></i>';
            });
            
            // 添加移动菜单样式
            const style = document.createElement('style');
            style.textContent = `
                @media (max-width: 768px) {
                    nav {
                        position: absolute;
                        top: 100%;
                        left: 0;
                        right: 0;
                        background: var(--card-bg);
                        backdrop-filter: blur(10px);
                        padding: 20px;
                        border-radius: 0 0 var(--border-radius) var(--border-radius);
                        box-shadow: 0 8px 32px 0 var(--shadow-color);
                        display: none;
                        z-index: 100;
                    }
                    
                    nav.active {
                        display: block;
                    }
                    
                    nav ul {
                        flex-direction: column;
                        align-items: center;
                    }
                    
                    nav ul li {
                        margin: 10px 0;
                    }
                    
                    .mobile-menu-toggle {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        background: rgba(255, 255, 255, 0.2);
                        cursor: pointer;
                        font-size: 1.2rem;
                        color: var(--primary-color);
                    }
                }
            `;
            document.head.appendChild(style);
        }
    };
    
    // 初始化移动菜单
    createMobileMenu();
    
    // 窗口大小改变时重新检查
    window.addEventListener('resize', createMobileMenu);
}); 