const { createProxyMiddleware } = require("http-proxy-middleware")

module.exports = (app) => {
  app.use(
    ["/api"],
    createProxyMiddleware({
      target: process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8000/' : 'https://c404project.herokuapp.com/',
      changeOrigin: true
    })
  );
};