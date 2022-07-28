const webpack = require("webpack");

module.exports = {
  configureWebpack: config => {
    config.output.libraryExport = "default";
    config.plugins.push(
      new webpack.DefinePlugin({
        GEODE: JSON.stringify(require("./package.json").geode)
      })
    );
  }
};
