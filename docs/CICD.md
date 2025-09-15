# CI/CD

(build)=
## `uv build`
在上传Python包之前，需要生成发行版包。这些是用户可以下载并安装到他们系统中的压缩归档文件。它们有两种类型：源代码（或sdist）归档和wheel格式的二进制包。`uv`支持使用`uv build`命令生成这两种包：

```bash
uv build
```

使用该命令后，将会打包`modern_python`的Python包，并将它们保存在`dist`目录中。

关于更细节的信息，请参考[此视频](https://www.bilibili.com/video/BV12NgLzhEKx?vd_source=189ac0e5f555cc7d23863c9d75a86118)。
## 将你的包上传到PyPI