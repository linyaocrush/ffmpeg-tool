# FFmpeg Tool - 专业视频处理工具

一个基于 Python 和 PyQt5 开发的现代化 FFmpeg 图形界面工具，专为视频创作者设计，提供简洁直观的操作界面，让复杂的视频处理变得简单易用。

## 🌟 功能特性

### 🎬 视频转码
- **格式转换**：支持 MP4、MKV、AVI、MOV 等多种视频格式互转
- **编码优化**：H.264、H.265 等主流编码格式支持
- **画质调节**：自定义分辨率、比特率、帧率等参数
- **批量处理**：支持批量视频文件转码，提高工作效率
- **预设配置**：内置常用设备预设（手机、平板、Web等）

### 📝 字幕合成
- **字幕嵌入**：支持 SRT、ASS 等字幕格式嵌入视频
- **样式定制**：可自定义字幕字体、大小、颜色、位置
- **实时预览**：字幕效果实时预览，所见即所得
- **多语言支持**：完美支持中文、英文等多语言字幕
- **时间轴调整**：精确控制字幕显示时间

### 🎨 现代化界面
- **简洁设计**：融合 Apple 设计风格与 Windows 11 美学
- **响应式布局**：完美适配不同屏幕尺寸
- **深色模式**：支持浅色/深色主题切换
- **操作反馈**：清晰的视觉反馈和状态提示

## 🚀 快速开始

### 系统要求
- **操作系统**：Windows 10/11、macOS 10.14+、Linux Ubuntu 18.04+
- **Python**：3.7 或更高版本
- **FFmpeg**：系统需预装 FFmpeg

### 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/your-username/ffmpeg-tool.git
cd ffmpeg-tool
```

#### 2. 安装依赖
```bash
pip install -r requirements.txt
```

#### 3. 运行应用
```bash
python main.py
```

### FFmpeg 安装

#### Windows
1. 访问 [FFmpeg 官网](https://ffmpeg.org/download.html)
2. 下载 Windows 版本
3. 解压到任意目录
4. 将 FFmpeg 添加到系统 PATH

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

## 📖 使用指南

### 视频转码
1. 打开应用，切换到"视频转码"标签页
2. 点击"选择文件"添加要转码的视频
3. 选择输出格式和质量预设
4. 点击"开始转码"开始处理
5. 查看进度条了解处理状态

### 字幕合成
1. 切换到"字幕合成"标签页
2. 选择视频文件和字幕文件
3. 调整字幕样式（字体、大小、颜色、位置）
4. 预览字幕效果
5. 点击"开始合成"生成带字幕的视频

## 🛠️ 开发环境搭建

### 开发依赖
```bash
pip install -r requirements-dev.txt
```

### 项目结构
```
ffmpeg-tool/
├── main.py              # 主程序入口
├── requirements.txt     # 依赖列表
├── tabs/               # 功能模块
│   ├── subtitle_tab.py    # 字幕合成功能
│   └── video_transcode_tab.py  # 视频转码功能
├── utils/              # 工具模块
│   └── video_encoder.py   # 视频编码工具
└── README.md          # 项目说明
```

### 技术栈
- **GUI框架**：PyQt5
- **视频处理**：FFmpeg
- **样式设计**：QSS样式表
- **打包工具**：PyInstaller

## 🔧 高级配置

### 自定义预设
可以在 `utils/video_encoder.py` 中添加自定义的转码预设：

```python
CUSTOM_PRESETS = {
    'my_custom_preset': {
        'video_codec': 'libx264',
        'video_bitrate': '2000k',
        'audio_codec': 'aac',
        'audio_bitrate': '128k'
    }
}
```

### 样式定制
修改 `main.py` 中的样式表来自定义界面主题：

```css
/* 自定义按钮样式 */
QPushButton {
    background-color: #your-color;
    border-radius: your-radius;
}
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- 遵循 PEP 8 Python 编码规范
- 添加必要的注释和文档字符串
- 确保代码通过测试

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [FFmpeg](https://ffmpeg.org/) - 强大的多媒体处理框架
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - 跨平台 GUI 框架
- [Python](https://www.python.org/) - 优雅的编程语言

## 📞 联系方式

- **项目地址**：[GitHub](https://github.com/linyao_crush/ffmpeg-tool)
- **问题反馈**：[Issues](https://github.com/linyao_crush/ffmpeg-tool/issues)

---

<div align="center">
  <p>⭐ 如果这个项目对你有帮助，请给个 Star！</p>
</div>