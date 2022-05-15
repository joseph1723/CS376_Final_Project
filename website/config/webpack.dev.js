const path = require('path');
const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'development',

  devtool: 'inline-source-map',

  devServer: {
    port: process.env.PORT | 1127,
    hot: true,
    historyApiFallback: true,
  },

  output: {
    path: undefined,
    filename: '[name].js',
  },
});
