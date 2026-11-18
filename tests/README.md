# 测试目录说明

## 后端测试

- 位置：各应用目录下的 `tests.py` 或 `tests/` 包。
- 运行：

```bash
python manage.py test
```

- 覆盖范围：正常流程、边界输入、非法状态转移、越权访问、竞争写入。

## 前端测试

- 位置：`tests/js/`。
- 运行：

```bash
node --test tests/js/register.test.cjs
```

> 仅当相关命令适用于当前代码时执行；新增前端测试时同步更新质量门禁命令。

## 质量门禁（合并前至少运行）

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
node --test tests/js/register.test.cjs
```

## 测试记录

功能与权限测试记录见 `../docs/功能与权限测试记录.md`；性能指标见 `../docs/性能测试报告.md`。
