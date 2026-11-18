# campus-secondhand-market

面向校内学生的二手物品发布、浏览与交易沟通平台。支持卖家发布闲置商品、买家浏览检索与咨询、买卖双方确认成交，以及管理员审核用户、处理举报、违规下架和推荐位调整。

## 技术栈

- 语言：Python 3.12
- 后端框架：Django 5.2
- 数据库：SQLite（第一版）
- 前端：服务端模板 + 原生 JavaScript
- 实时沟通：P1，可选 WebSocket / 短轮询

## 目录结构

> 以下结构按软件需求规格说明书列出，实际工程目录以提交后的代码为准。

```
campus-secondhand-market/
├── accounts/          # 注册、登录、退出、密码重置、个人资料与审核
├── items/             # 商品创建、列表、详情、状态操作、下架、评价
├── locations/         # 商品分类、成色标准、交易方式维护
├── chat/              # P1 商品内文字沟通
├── admin/             # Django 管理入口或维护工具
├── core/              # 公共配置、工具与基础模型
├── templates/         # 服务端模板
├── static/            # 静态资源（CSS、JS、图片）
├── tests/             # 后端自动化测试
│   └── js/            # 前端自动化测试
├── docs/              # 交付文档（见下方“文档清单”）
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## 环境准备

1. 安装 Python 3.12。
2. 克隆仓库：

```bash
git clone https://github.com/【用户名】/campus-secondhand-market.git
cd campus-secondhand-market
```

3. 创建虚拟环境并安装依赖：

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt
```

4. 复制环境变量样例并按需填写：

```bash
cp .env.example .env
```

> `.env` 不提交到仓库；其中的密钥、数据库口令、邮箱授权码等只能通过环境变量提供。

## 初始化与运行

```bash
# 生成迁移（如代码已含迁移文件，可直接 migrate）
python manage.py makemigrations

# 执行数据库迁移
python manage.py migrate

# 创建管理员账号（按需）
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

浏览器访问终端输出的地址（默认 `http://127.0.0.1:8000/`）。

## 测试与质量检查

```bash
# Django 系统检查
python manage.py check

# 迁移是否遗漏
python manage.py makemigrations --check --dry-run

# 后端自动化测试
python manage.py test

# 前端测试（如存在对应测试文件）
node --test tests/js/register.test.cjs
```

## 配置说明

| 配置项 | 说明 | 是否必填 |
| --- | --- | --- |
| `SECRET_KEY` | Django 密钥，生产环境必须使用随机长密钥 | 是 |
| `DEBUG` | 调试模式，生产环境必须为 `False` | 是 |
| `ALLOWED_HOSTS` | 允许访问的主机名 | 是 |
| `DATABASE_URL` / 数据库配置 | SQLite 默认本地文件；后续可迁移独立数据库 | 否 |
| `EMAIL_HOST` / `EMAIL_PORT` / `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` / `EMAIL_USE_TLS` | 可选密码重置邮件 SMTP 配置 | 否 |
| `SITE_DOMAIN` | 站点对外域名，用于生成密码重置链接 | 按需 |

## 文档清单（docs/）

| 文档 | 对应交付项 |
| --- | --- |
| `docs/软件需求规格说明书.md`（或 docx） | 8.2 软件需求规格说明书 |
| `docs/架构与数据模型说明.md` | 架构说明、ER 图 / 数据模型说明 |
| `docs/路由接口清单.md` | 接口 / 路由清单 |
| `docs/需求-Issue-测试追踪矩阵.xlsx` | 需求、Issue 与测试用例追踪矩阵 |
| `docs/需求决策记录.md` | 关键需求决策记录 |
| `docs/功能与权限测试记录.md` | 8.3 功能与权限测试记录 |
| `docs/性能测试报告.md` | 8.3 性能测试报告 |
| `docs/备份恢复演练记录.md` | 8.3 备份恢复演练记录 |
| `docs/已知问题与未完成需求清单.md` | 8.3 已知问题和未完成需求清单 |
| `CHANGELOG.md` | 8.2 版本变更记录 |

## 交付与版本

- 使用 Git Tag 和 Release 标记可验收版本，并附 Release Notes。
- 课程平台如需压缩包，从对应 Release 导出；不得包含 `.git`、虚拟环境、运行数据库、真实上传材料或秘密配置。
- 演示数据使用虚构信息，不得使用真实学生、卖家或管理员的敏感材料。

## 第一版范围（P0 / P1 / P2）

- **P0**：注册登录、资料与身份审核、商品发布、浏览检索、咨询沟通、成交双方确认、下架与审核、业务审计。
- **P1**：商品图片、商品内聊天、推荐位调整、服务评价、站内通知、统计概览。
- **P2（后续扩展，不在第一版验收阻断项）**：自动推荐匹配、证件联网核验、短信/微信通知、统一身份认证、跨区域管理员、统计数据导出。

## 角色

- **卖家**：发布并管理本人闲置商品，回复咨询并标记成交。
- **买家**：浏览检索商品、咨询卖家并确认成交。
- **管理员**：审核用户、维护基础数据、处理举报、违规下架与推荐位管理。
- **系统维护者**：部署、备份、恢复与排查系统问题，不等同于业务管理员。
