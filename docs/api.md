# 接口文档

基础地址：`http://127.0.0.1:5000`

## 认证接口

### POST /api/login

请求体：

```json
{
  "username": "admin",
  "password": "admin123"
}
```

### POST /api/logout

- 退出当前会话

## 算法与说明

### GET /api/algorithms

- 返回平台算法列表

### GET /api/algorithm_docs

- 返回算法说明（用途/输入/输出/场景）

## 上传接口

### POST /api/upload/image

- form-data: `file=<图片文件>`

### POST /api/upload/video

- form-data: `file=<视频文件>`

## 算法运行接口

### POST /api/run/yolo
### POST /api/run/segmentation
### POST /api/run/mnist
### POST /api/run/super_resolution
### POST /api/run/action_recognition
### POST /api/run/texture_style

请求体：

```json
{
  "file_path": "上传接口返回的本地绝对路径"
}
```

返回字段：

- `success`：是否成功
- `algorithm`：算法 key
- `output_url`：输出文件访问地址
- `result_text`：结果说明
- `extra_output_url`：可选，额外输出（例如分割掩码）

## 记录与日志

### GET /api/history

- 返回历史测试记录

### GET /api/logs

- 返回系统日志
