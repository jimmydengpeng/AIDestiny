<template>
  <div class="testimonial">
    <div class="user-avatar">
      <i class="fas fa-user-circle" v-if="!avatar"></i>
      <img :src="avatar" v-if="avatar" :alt="name">
    </div>
    <div class="testimonial-content">
      <p>"{{ content }}"</p>
      <h4>- {{ name }}</h4>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestimonialCard',
  props: {
    content: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    avatar: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.testimonial {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: var(--border-radius);
  background: rgba(255, 255, 255, 0.5);
  margin-bottom: 20px;
  transition: var(--transition);
}

.testimonial:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 20px;
  flex-shrink: 0;
}

.user-avatar i {
  font-size: 1.8rem;
  color: var(--light-text);
}

.user-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.testimonial-content p {
  font-style: italic;
  margin-bottom: 10px;
}

.testimonial-content h4 {
  font-weight: 600;
  color: var(--primary-color);
}

@media (max-width: 480px) {
  .testimonial {
    flex-direction: column;
    text-align: center;
  }
  
  .user-avatar {
    margin-right: 0;
    margin-bottom: 15px;
  }
}
</style> 