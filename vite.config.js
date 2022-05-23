export default {
  build: {
    rollupOptions: {
      input: {
        main: './index.html',
        recommender: './recommender.html',
      },
    },
    sourcemap: true,
    target: 'esnext'
  }
}
