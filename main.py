import sys
import traceback
import datetime
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from tabs.subtitle_tab import SubtitleTab
from tabs.video_transcode_tab import VideoTranscodeTab
from tabs.audio_video_tab import AudioVideoTab

class CustomApplication(QApplication):
    def notify(self, receiver, event):
        try:
            return super().notify(receiver, event)
        except Exception:
            log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'error.log')
            with open(log_path, 'a', encoding='utf-8') as f:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f'[{timestamp}] Qt事件异常:\n')
                traceback.print_exc(file=f)
                f.write('\n' + '-'*80 + '\n')
            sys.exit(1)

class FFmpegTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FFmpeg工具")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建标签页
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 设置全局样式表 - 融合Apple设计风格与Windows 11美学
        self.setStyleSheet("""
            /* 全局样式 */
            QWidget {
                background-color: #f5f5f7;
                color: #1d1d1f;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                font-size: 18px;
            }

            /* 标签页容器 */
            QTabWidget::pane {
                border: none;
                background-color: #ffffff;
                border-radius: 12px;
                margin: 10px;
            }

            /* 标签栏 */
            QTabBar::tab {
                background-color: transparent;
                color: #6e6e73;
                padding: 10px 20px;
                margin-right: 4px;
                border-radius: 8px;
                font-weight: 500;
            }

            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #1d1d1f;
            }

            QTabBar::tab:hover:!selected {
                background-color: rgba(0, 0, 0, 0.03);
            }

            /* 按钮样式 */
            QPushButton {
                background-color: #0071e3;
                color: white;
                border-radius: 8px;
                padding: 9px 20px;
                border: none;
                font-weight: 500;
            }

            QPushButton:hover {
                background-color: #0077ed;
            }

            QPushButton:pressed {
                background-color: #0066d6;
            }

            QPushButton:disabled {
                background-color: #d2d2d7;
                color: #ffffff;
            }

            /* 输入框样式 */
            QLineEdit {
                border: 1px solid #d2d2d7;
                border-radius: 8px;
                padding: 9px 12px;
                background-color: #ffffff;
            }

            QLineEdit:focus {
                border-color: #0071e3;
                outline: none;
            }

            /* 组合框样式 */
            QComboBox {
                border: 1px solid #d2d2d7;
                border-radius: 8px;
                padding: 9px 12px;
                background-color: #ffffff;
                min-width: 120px;
            }

            QComboBox:focus {
                border-color: #0071e3;
                outline: none;
            }

            /* 滑块样式 */
            QSlider::groove:horizontal {
                background-color: #d2d2d7;
                height: 4px;
                border-radius: 2px;
            }

            QSlider::handle:horizontal {
                background-color: #0071e3;
                width: 20px;
                height: 20px;
                margin: -8px 0;
                border-radius: 10px;
            }

            QSlider::handle:horizontal:hover {
                background-color: #0077ed;
            }

            /* 进度条样式 */
            QProgressBar {
                background-color: #f5f5f7;
                border: 1px solid #d2d2d7;
                border-radius: 8px;
                text-align: center;
                height: 30px;
                min-width: 300px;
            }

            QProgressBar::chunk {
                background-color: #0071e3;
                border-radius: 6px;
            }

            /* 分组框样式 */
            QGroupBox {
                border: 1px solid #d2d2d7;
                border-radius: 12px;
                padding: 16px;
                margin-top: 8px;
                background-color: #ffffff;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                color: #1d1d1f;
                font-weight: 500;
            }

            /* 文本编辑框样式 */
            QTextEdit {
                border: 1px solid #d2d2d7;
                border-radius: 8px;
                background-color: #ffffff;
                padding: 12px;
                transition: border-color 0.2s ease;
            }

            QTextEdit:focus {
                border-color: #0071e3;
                outline: none;
            }
        """)

        # 添加字幕标签页
        self.subtitle_tab = SubtitleTab()
        self.tabs.addTab(self.subtitle_tab, "字幕合成")

        # 添加视频转码标签页
        self.video_transcode_tab = VideoTranscodeTab()
        self.tabs.addTab(self.video_transcode_tab, "视频转码")

        # 添加音视频处理标签页
        self.audio_video_tab = AudioVideoTab()
        self.tabs.addTab(self.audio_video_tab, "音视频处理")

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'error.log')
    with open(log_path, 'a', encoding='utf-8') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'[{timestamp}] 未捕获的异常: {exc_type.__name__}\n')
        f.write(f'消息: {exc_value}\n')
        f.write('回溯信息:\n')
        traceback.print_tb(exc_traceback, file=f)
        f.write('\n' + '-'*80 + '\n')
    sys.exit(1)

sys.excepthook = handle_exception

if __name__ == "__main__":
    app = CustomApplication(sys.argv)
    window = FFmpegTool()
    window.show()
    sys.exit(app.exec_())