export default {
  login() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: {
            token: 'fake-jwt-token',
            user: { username: 'admin', role: 'admin' },
          },
          status: 200,
          statusText: 'OK',
        });
      }, 500);
    });
  },
};
