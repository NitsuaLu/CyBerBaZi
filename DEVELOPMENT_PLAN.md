# 八字排盘算命工具 — 完整开发计划

## 背景与目标

开发一个完整的八字排盘/算命工具。先做 Web 应用，核心算法独立成 Python 包以便后续扩展手机 App。功能覆盖：四柱排盘、十神分析、五行旺衰、格局判断、用神忌神、大运流年、神煞、命理报告生成。

---

## 技术选型

| 层 | 选择 | 理由 |
|---|---|---|
| 核心算法 | 独立 Python 包 `bazi-engine` | 零 UI 依赖，可复用、可独立发布 PyPI |
| 后端框架 | FastAPI + Pydantic v2 | 性能好、自动 OpenAPI 文档、类型安全 |
| 前端框架 | React + Vite + TailwindCSS | 生态成熟，后续 React Native 可复用类型和 API 层 |
| 图表库 | ECharts | 中文排版好，五行雷达图开箱即用 |
| 包管理 | pip + setuptools | 当前环境使用 |

---

## 项目目录结构

```
D:/CyBerBaZi/
├── packages/
│   └── bazi-engine/                 # 核心算法库 (纯 Python)
│       └── src/bazi/
│           ├── core/                # 天干地支、五行、纳音、藏干、合冲刑害、十神
│           ├── calendar/            # 节气、干支纪日、农历转换
│           ├── paipan/              # 四柱排盘、大运、流年
│           ├── analysis/            # 神煞、格局、用神、旺衰
│           └── report/              # 报告生成
│
├── apps/
│   ├── backend/                     # FastAPI 后端
│   └── web/                         # React 前端
│
├── tools/                           # 数据生成工具 (节气/农历 JSON)
└── data/                            # 共享数据文件
```

---

## 分阶段开发计划

### Phase 1: 核心基础数据 ✅ 已完成
- 天干 (HeavenlyStem)、地支 (EarthlyBranch)、五行 (WuXing) 枚举与属性
- 六十甲子纳音表、地支藏干表
- 天干五合、地支六合/三合/三会/六冲/六害/三刑
- 十神关系推导引擎
- 141 项测试全部通过

### Phase 2: 历法系统
- 节气数据 JSON (1900-2100，精确到分钟)
- 干支纪日推算
- 公历 <-> 农历互转

### Phase 3: 排盘引擎
- 年柱/月柱/日柱/时柱排盘
- 真太阳时校正
- 大运排盘 (顺排/逆排 + 起运年龄)
- 主入口 `build_chart()`

### Phase 4: 分析引擎
- 十神标注、神煞系统
- 格局判定 (正格 8 种 + 变格)
- 旺衰判断 + 用神忌神分析

### Phase 5: 报告生成
- 基于模板的命理分析报告

### Phase 6: 后端 API
- FastAPI + Pydantic Schema

### Phase 7: 前端 Web 应用
- React + Vite + TailwindCSS + ECharts

### Phase 8: 完善与部署

---

## 关键技术决策

- **节气数据**：预计算 JSON，不依赖运行时天文库
- **真太阳时**：默认北京时间，可选经度校正
- **输入方式**：同时支持公历和农历输入
- **子时处理**：23 点后为次日子时

---

## 验证方式

- 核心模块：pytest 单元测试
- 排盘引擎：已知八字验证案例回归测试
- 后端 API：FastAPI TestClient 集成测试
- 边界测试：节气交节前后、闰月出生、子时出生
