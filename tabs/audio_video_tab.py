from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QRadioButton, QGroupBox, QButtonGroup)
import os
import subprocess
from utils.video_encoder import VideoEncoder

class AudioVideoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # 操作选项
        option_group = QGroupBox("操作选项")
        option_layout = QVBoxLayout()
        
        self.extract_radio = QRadioButton("从视频提取音频")
        self.merge_radio = QRadioButton("合并视频和音频")
        self.extract_radio.setChecked(True)
        
        self.option_btn_group = QButtonGroup()
        self.option_btn_group.addButton(self.extract_radio, 0)
        self.option_btn_group.addButton(self.merge_radio, 1)
        
        option_layout.addWidget(self.extract_radio)
        option_layout.addWidget(self.merge_radio)
        option_group.setLayout(option_layout)
        layout.addWidget(option_group)
        
        # 视频文件选择
        video_layout = QHBoxLayout()
        video_layout.addWidget(QLabel("视频文件:"))
        self.video_path = QLineEdit()
        video_btn = QPushButton("浏览")
        video_btn.clicked.connect(self.browse_video)
        video_layout.addWidget(self.video_path)
        video_layout.addWidget(video_btn)
        layout.addLayout(video_layout)
        
        # 音频文件选择（合并时使用）
        self.audio_layout = QHBoxLayout()
        self.audio_layout.addWidget(QLabel("音频文件:"))
        self.audio_path = QLineEdit()
        audio_btn = QPushButton("浏览")
        audio_btn.clicked.connect(self.browse_audio)
        self.audio_layout.addWidget(self.audio_path)
        self.audio_layout.addWidget(audio_btn)
        self.audio_path.setEnabled(False)
        audio_btn.setEnabled(False)
        layout.addLayout(self.audio_layout)
        
        # 连接单选按钮事件
        self.extract_radio.toggled.connect(self.toggle_audio_input)
        
        # 输出文件选择
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出文件:"))
        self.output_path = QLineEdit()
        output_btn = QPushButton("浏览")
        output_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(output_btn)
        layout.addLayout(output_layout)
        
        # 处理按钮
        self.process_btn = QPushButton("开始处理")
        self.process_btn.clicked.connect(self.process)
        layout.addWidget(self.process_btn)
        
        self.setLayout(layout)
        
    def toggle_audio_input(self, checked):
        enable = self.merge_radio.isChecked()
        self.audio_path.setEnabled(enable)
        self.audio_layout.itemAt(2).widget().setEnabled(enable)
        
    def browse_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi *.mkv)")
        if path:
            self.video_path.setText(path)
            if not self.output_path.text():
                self.output_path.setText(os.path.splitext(path)[0] + "_output.mp4")
                
    def browse_audio(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择音频文件", "", "音频文件 (*.mp3 *.wav *.aac)")
        if path:
            self.audio_path.setText(path)
            
    def browse_output(self):
        path, _ = QFileDialog.getSaveFileName(self, "保存输出文件", "", "输出文件 (*.mp4 *.mp3)")
        if path:
            self.output_path.setText(path)
            
    def process(self):
        video_path = self.video_path.text()
        output_path = self.output_path.text()
        
        if not video_path or not output_path:
            return
            
        if self.extract_radio.isChecked():
            # 提取音频
            cmd = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'copy', output_path]
        else:
            # 合并音视频
            audio_path = self.audio_path.text()
            if not audio_path:
                return
            cmd = ['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'copy', output_path]
            
        # 执行命令
        VideoEncoder.run_ffmpeg_command(cmd)