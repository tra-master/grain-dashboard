---
name: fix-chart-lazy-init
overview: 修复 GitHub Pages 上非默认Tab页图表不显示的问题：将图表初始化改为懒加载（点击Tab时才渲染），并推送到 GitHub Pages。
todos:
  - id: modify-spreads-html
    content: 修改源文件 spreads.html：更新 loadData() 和 showPage() 函数实现懒加载逻辑
    status: pending
  - id: sync-deploy-index
    content: 复制更新后的 spreads.html 到 gh-deploy/index.html，保持部署文件同步
    status: pending
    dependencies:
      - modify-spreads-html
  - id: git-commit-push
    content: 执行 git add、commit、push 命令，推送更改到 GitHub 远端仓库
    status: pending
    dependencies:
      - sync-deploy-index
  - id: verify-deployment
    content: 验证 GitHub Pages 已更新，通过浏览器测试各页面图表是否正常显示
    status: pending
    dependencies:
      - git-commit-push
---

## 问题描述

GitHub Pages 上的谷物期现价差分析看板 (https://tra-master.github.io/grain-dashboard/) 在别人电脑上打开时，DCE月间价差、CBOT-DCE价差、小麦-玉米价差、FOB基差这四个页面的图表无法显示，而本地正常。

## 根本原因

页面加载时 `loadData()` 函数一次性调用所有四个子页面的图表初始化函数（`initDCECharts()`、`initCBTDCharts()`、`initWheatCharts()`、`initFOB()`），但这四个页面的 HTML 容器都设置了 `class="hidden"`（即 `display: none`）。

Chart.js 在 `display: none` 的容器中无法获取正确的画布尺寸（宽高均为 0），导致图表渲染失败、显示为空白。本地可能因浏览器缓存或窗口 resize 事件触发了重绘，意外显示了图表。

## 修复需求

1. 实现图表**懒加载**机制：仅当用户点击对应 Tab 时，才在该页面变为可见（`display: block`）后初始化其图表
2. 避免重复初始化：已初始化的页面不重复调用初始化函数
3. 同步更新源文件和部署文件，保持一致
4. 推送到 GitHub Pages 完成远端部署，使所有用户都能正常访问

## 核心功能

- 修改 `loadData()` 函数：移除对四个子页面图表的直接初始化调用，仅保留总览页面的数据更新
- 修改 `showPage()` 函数：加入状态追踪对象和条件初始化逻辑
- 页面切换时自动判断是否需要渲染该页面的图表
- 保持现有的 localStorage 年份显示记忆功能

## 技术栈

- **前端框架**：纯 HTML + JavaScript（无框架依赖）
- **图表库**：Chart.js + chartjs-adapter-date-fns（CDN 加载）
- **数据存储**：内嵌 JSON（EMBEDDED_DATA 对象）
- **部署方式**：GitHub Pages（静态网站托管）
- **版本控制**：Git 命令行

## 实现方案

### 核心修改策略

采用**页面懒加载模式**，通过状态追踪实现按需初始化：

1. **维护初始化状态字典**：创建 `initializedPages` 对象记录每个页面是否已完成图表初始化

```
initializedPages = {
'dce-spreads': false,
'cbot-dce': false,
'wheat-corn': false,
'fob': false
}
```

2. **修改 loadData() 函数**：

- 保留 `spreadData = EMBEDDED_DATA` 和 `updateOverviewCards()`
- 删除对 `initDCECharts()` 等四个函数的直接调用
- 添加初始化状态字典的创建

3. **修改 showPage() 函数**：

- 隐藏其他页面、显示目标页面（现有逻辑不变）
- 在显示目标页面后，检查 `initializedPages[pageId]` 状态
- 若为 `false`，调用对应的初始化函数（如 `initDCECharts`）并标记为 `true`
- 若为 `true`，跳过初始化

4. **页面 → 初始化函数映射**：

```
'dce-spreads' → initDCECharts()
'cbot-dce' → initCBTDCharts()
'wheat-corn' → initWheatCharts()
'fob' → initFOB()
```

### 设计特点

- **无功能损失**：所有现有功能（localStorage 状态记忆、图表交互、总览数据卡片）保持不变
- **性能优化**：避免浏览器在加载时处理四个隐藏页面的图表，减少初始化时间
- **跨浏览器兼容**：纯 JavaScript 实现，无浏览器差异问题
- **向后兼容**：修改不影响现有的数据结构或事件绑定

### 预期效果

| 场景 | 修复前 | 修复后 |
| --- | --- | --- |
| 打开页面点击 "DCE月间价差" | 图表空白 | 图表正常显示 |
| 重复点击同一 Tab | 创建重复图表对象 | 使用已缓存图表，无重复 |
| 点击 "总览" 再回到 "DCE月间价差" | 可能出现渲染问题 | 使用缓存的已初始化图表 |
| 年份显示状态记忆 | 正常 | 正常（未改动） |


## 实现注意事项

1. **初始化状态字典作用域**：应为全局变量或紧靠 `loadData()` 函数定义，确保在整个页面生命周期内可访问
2. **Tab 点击事件流**：现有代码通过 `data-page` 属性传递页面标识，确保映射的函数名与实际定义一致
3. **Chart.js 对象生命周期**：已初始化的图表对象会被追踪，避免内存泄漏
4. **总览页特殊处理**：overview 页面在 `loadData()` 时就可见，保持原有逻辑不变