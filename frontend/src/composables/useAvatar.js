import { computed } from 'vue';
import { useUserStore } from '../store/userStore';
import catImg from '../assets/cat.png';

export function useAvatar() {
  const userStore = useUserStore();

  const avatarUrl = computed(() => {
    if (userStore.user?.avatar_url) {
      const baseUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5001';
      return `${baseUrl}/${userStore.user.avatar_url}`;
    }
    return catImg;
  });

  return { avatarUrl };
}
