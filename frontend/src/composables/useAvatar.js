import { computed } from 'vue';
import { useUserStore } from '../store/userStore';

export function useAvatar() {
  const userStore = useUserStore();

  const avatarUrl = computed(() => {
    if (userStore.user?.avatar_url) {
      const baseUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5001';
      return `${baseUrl}/${userStore.user.avatar_url}`;
    }
    return null;
  });

  const hasAvatar = computed(() => !!userStore.user?.avatar_url);

  return { avatarUrl, hasAvatar };
}
