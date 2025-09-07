# 本地开发指南

## 环境要求
- Ruby 2.6+
- Bundler

## 安装依赖
```bash
bundle install
```

## 本地预览
启动本地Jekyll服务器：
```bash
bundle exec jekyll serve
```

或者使用实时重载：
```bash
bundle exec jekyll serve --livereload
```

## 访问本地网站
启动后访问：http://localhost:4000

## 常用命令
- `bundle exec jekyll serve` - 启动本地服务器
- `bundle exec jekyll serve --drafts` - 包含草稿文章
- `bundle exec jekyll serve --livereload` - 自动刷新浏览器
- `bundle exec jekyll build` - 构建静态网站到 `_site` 目录

## 开发流程
1. 编辑Markdown文件
2. 保存文件（如果使用--livereload，浏览器会自动刷新）
3. 在浏览器中查看效果
4. 满意后提交到GitHub

## 注意事项
- 修改 `_config.yml` 后需要重启服务器
- 本地预览的效果与GitHub Pages基本一致
- `_site` 目录是自动生成的，不需要提交到Git
