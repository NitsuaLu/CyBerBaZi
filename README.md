# CyBerBaZi — 八字排盘算命工具

传统命理学与现代技术的结合。输入出生日期时间，自动排出八字命盘，提供十神分析、神煞、格局判定、旺衰判断、用神建议及完整命理报告。

## 功能概览

- **八字排盘** — 年柱/月柱/日柱/时柱，支持真太阳时校正
- **纳音五行** — 六十甲子纳音 + 五行属性标注
- **藏干十神** — 地支藏干识别 + 十神关系全标注
- **大运流年** — 大运顺逆排 + 起运年龄 + 流年流月推算
- **神煞系统** — 天乙贵人、文昌、桃花、驿马、禄神、羊刃、华盖、将星、天德、月德、空亡等
- **格局判定** — 正格 8 种 + 建禄格/月刃格 + 变格识别
- **旺衰分析** — 得令/得地/得生/得助 四维量化打分
- **用神建议** — 调候法 + 扶抑法，输出用神/喜神/忌神/仇神
- **命理报告** — 一键生成 Markdown / 纯文本双格式完整报告
- **REST API** — FastAPI 后端，Swagger 文档自动生成
- **Web 界面** — React 响应式前端，移动端适配

## 项目结构

```
CyBerBaZi/
├── packages/bazi-engine/         # 核心算法库 (纯 Python, 零 UI 依赖)
│   └── src/bazi/
│       ├── core/                 # 天干地支、五行、纳音、藏干、合冲刑害、十神
│       ├── calendar/             # 节气查询 (1900-2100)、干支纪日
│       ├── paipan/               # 四柱排盘、大运、流年、真太阳时
│       ├── analysis/             # 神煞、格局、旺衰、用神
│       └── report/               # 报告模板引擎
├── apps/
│   ├── backend/                  # FastAPI 后端
│   └── web/                      # React + TailwindCSS 前端
├── tools/                        # 节气数据生成脚本
├── docker-compose.yml            # 生产部署
├── nginx.conf                    # Nginx 配置
├── DEVELOPING_PLAN.md            # 开发计划
└── DEPLOYMENT.md                 # 部署指南
```

## 快速开始

### 环境要求

- Python >= 3.10
- Node.js >= 18

### 安装运行

```bash
# 1. 克隆仓库
git clone git@github.com:NitsuaLu/CyBerBaZi.git
cd CyBerBaZi

# 2. 安装 Python 核心引擎
cd packages/bazi-engine
python -m venv .venv
.venv/Scripts/pip install -e ".[dev]"
cp tools/generate_solar_terms.py . && python tools/generate_solar_terms.py
cd ../..

# 3. 安装后端
cd apps/backend
../bazi-engine/.venv/Scripts/pip install -e "."

# 4. 启动后端
uvicorn bazi_api.main:app --reload
# API 文档: http://127.0.0.1:8000/docs

# 5. 安装前端 (另开终端)
cd apps/web
npm install
npm run dev
# 前端页面: http://localhost:5173
```

### 运行测试

```bash
cd packages/bazi-engine
.venv/Scripts/python -m pytest tests/ -v

cd apps/backend
.venv/Scripts/python -m pytest tests/ -v
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/bazi/calculate` | 排盘：返回八字命盘 |
| POST | `/api/v1/bazi/analyze` | 分析：返回十神/神煞/格局/旺衰/用神 |
| POST | `/api/v1/bazi/report` | 报告：返回完整命理报告 |
| GET | `/api/v1/health` | 健康检查 |

### 请求示例

```json
POST /api/v1/bazi/calculate
{
  "birth_date": "2000-06-15",
  "birth_time": "12:00:00",
  "sex": "male",
  "longitude": 120.0
}
```

## 技术栈

| 层 | 技术 |
|---|---|
| 核心算法 | Python 3.13, ephem (天文计算) |
| 后端 | FastAPI + Pydantic v2 + Uvicorn |
| 前端 | React 19 + TypeScript + TailwindCSS 3 |
| 部署 | Docker + Nginx + Docker Compose |

## 免责声明

**本工具仅供学习研究和文化交流使用。**

- 八字命理学是中国传统文化的一部分，其理论和方法并未经过现代科学验证。本工具的计算结果和分析建议**不构成任何形式的科学结论、医疗建议、投资建议或人生决策依据**。
- 命理分析结果由算法基于传统规则自动生成，**仅供参考和娱乐**，请理性看待，切勿过度依赖。
- 使用者应对基于本工具输出所做的任何决定自行承担全部责任。**开发者不对因使用本工具而产生的任何直接或间接后果负责**。
- 节气数据由天文算法计算生成，可能存在数分钟误差，不应作为精确天文观测依据。
- 本工具不收集、不存储任何用户的出生信息或其他个人数据到远程服务器。所有计算均在本地完成。

> *"善易者不占。" — 《荀子》*

## License

MIT License — 详见 [LICENSE](LICENSE) 文件。
