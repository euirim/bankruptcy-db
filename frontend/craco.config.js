const CracoLessPlugin = require("craco-less");

module.exports = {
  plugins: [
    {
      plugin: CracoLessPlugin,
      options: {
        lessLoaderOptions: {
          modifyVars: {
            "@border-radius-base": "2px",
            "@font-family":
              "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'",
            "@font-size-base": "16px",
            "@border-color-split": "#dcdde1",
          },
          javascriptEnabled: true
        }
      }
    }
  ]
};
