# 测试说明文档

## 1. 测试目标

- 验证登录流程是否可用
- 验证算法列表接口返回正常
- 验证图片上传 + YOLO 推理基本流程可用

## 2. 测试命令

```bash
pytest tests -q
```

## 3. 当前自动化测试覆盖

- `tests/test_api.py::test_login_and_algorithms`
- `tests/test_api.py::test_upload_and_run_yolo`

## 4. 建议扩展测试

- 视频上传与动作识别接口测试
- 异常文件格式上传测试
- 未登录访问接口测试
- 历史记录与日志分页测试
