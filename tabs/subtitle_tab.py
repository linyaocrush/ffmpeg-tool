import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QTextEdit, QGroupBox, QRadioButton, QButtonGroup, QComboBox, QSlider, QProgressBar
from PyQt5.QtCore import QProcess

class SubtitleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 文件选择区域
        file_group = QGroupBox("文件选择")
        file_layout = QVBoxLayout()
        
        # 视频文件选择
        video_layout = QHBoxLayout()
        self.video_path_edit = QLineEdit()
        video_button = QPushButton("选择视频文件")
        video_button.clicked.connect(self.select_video_file)
        video_layout.addWidget(QLabel("视频文件:"))
        video_layout.addWidget(self.video_path_edit)
        video_layout.addWidget(video_button)
        
        # 字幕文件选择
        subtitle_layout = QHBoxLayout()
        self.subtitle_path_edit = QLineEdit()
        subtitle_button = QPushButton("选择字幕文件")
        subtitle_button.clicked.connect(self.select_subtitle_file)
        subtitle_layout.addWidget(QLabel("字幕文件:"))
        subtitle_layout.addWidget(self.subtitle_path_edit)
        subtitle_layout.addWidget(subtitle_button)
        
        # 输出文件选择
        output_layout = QHBoxLayout()
        self.output_path_edit = QLineEdit()
        output_button = QPushButton("选择输出位置")
        output_button.clicked.connect(self.select_output_file)
        output_layout.addWidget(QLabel("输出目录:"))
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(output_button)
        
        # 自定义输出文件名和格式
        custom_output_layout = QHBoxLayout()
        self.output_name_edit = QLineEdit()
        self.output_name_edit.setPlaceholderText("输出文件名 (不含扩展名)")
        self.output_format_combo = QComboBox()
        # 支持的格式列表
        self.all_formats = ["mp4", "mkv", "avi", "mov", "flv", "wmv", "webm", "mpeg", "mpg"]
        self.hard_subtitle_formats = ["mp4", "mkv", "avi", "mov", "flv", "wmv", "webm", "mpeg", "mpg"]
        self.soft_subtitle_formats = ["mp4", "mkv", "mov"]
        self.output_format_combo.addItems(self.hard_subtitle_formats)
        custom_output_layout.addWidget(QLabel("文件名:"))
        custom_output_layout.addWidget(self.output_name_edit)
        custom_output_layout.addWidget(QLabel("格式:"))
        custom_output_layout.addWidget(self.output_format_combo)
        
        file_layout.addLayout(video_layout)
        file_layout.addLayout(subtitle_layout)
        file_layout.addLayout(output_layout)
        file_layout.addLayout(custom_output_layout)
        file_group.setLayout(file_layout)
        
        # 操作按钮区域
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始合成")
        self.start_button.clicked.connect(self.start_muxing)
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addStretch()
        
        # 日志输出区域
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        
        # 字幕类型选择
        subtitle_type_group = QGroupBox("字幕类型")
        subtitle_type_layout = QHBoxLayout()
        self.hard_subtitle_radio = QRadioButton("硬字幕")
        self.soft_subtitle_radio = QRadioButton("软字幕")
        self.hard_subtitle_radio.setChecked(True)  # 默认选择硬字幕
        
        subtitle_type_layout.addWidget(self.hard_subtitle_radio)
        subtitle_type_layout.addWidget(self.soft_subtitle_radio)
        subtitle_type_group.setLayout(subtitle_type_layout)
        
        # 连接字幕类型选择信号
        self.hard_subtitle_radio.toggled.connect(self.on_subtitle_type_changed)
        self.soft_subtitle_radio.toggled.connect(self.on_subtitle_type_changed)
        
        # 硬字幕编码选项
        self.encoding_options_group = QGroupBox("硬字幕编码选项")
        encoding_options_layout = QVBoxLayout()
        
        # CPU/GPU编码选择
        processing_layout = QHBoxLayout()
        processing_layout.addWidget(QLabel("处理方式:"))
        self.cpu_radio = QRadioButton("CPU")
        self.gpu_radio = QRadioButton("GPU")
        self.cpu_radio.setChecked(True)
        processing_layout.addWidget(self.cpu_radio)
        processing_layout.addWidget(self.gpu_radio)
        processing_layout.addStretch()
        
        # GPU品牌选择
        self.gpu_brand_layout = QHBoxLayout()
        self.gpu_brand_layout.addWidget(QLabel("GPU品牌:"))
        self.gpu_brand_combo = QComboBox()
        self.gpu_brand_combo.addItems(["NVIDIA", "AMD", "Intel"])
        self.gpu_brand_layout.addWidget(self.gpu_brand_combo)
        self.gpu_brand_layout.addStretch()
        self.gpu_brand_layout_widget = QWidget()
        self.gpu_brand_layout_widget.setLayout(self.gpu_brand_layout)
        self.gpu_brand_layout_widget.setVisible(False)  # 默认隐藏
        
        # CPU线程数
        self.threads_layout = QHBoxLayout()
        self.threads_layout.addWidget(QLabel("线程数:"))
        self.threads_combo = QComboBox()
        self.threads_combo.addItems(["默认", "1", "2", "4", "8", "16"])
        self.threads_layout.addWidget(self.threads_combo)
        self.threads_layout.addStretch()
        
        # 编码方式
        codec_layout = QHBoxLayout()
        codec_layout.addWidget(QLabel("编码器:"))
        self.codec_combo = QComboBox()
        # 所有支持的编码器
        self.all_codecs = [
            "libx264", "libx265", "mpeg4", "libvpx-vp9", "libaom-av1", 
            "h264_nvenc", "hevc_nvenc", "h264_amf", "hevc_amf", 
            "h264_qsv", "hevc_qsv", "h264_videotoolbox", "hevc_videotoolbox"
        ]
        # CPU编码器
        self.cpu_codecs = ["libx264", "libx265", "mpeg4", "libvpx-vp9", "libaom-av1"]
        # GPU编码器
        self.gpu_codecs = {
            "NVIDIA": ["h264_nvenc", "hevc_nvenc"],
            "AMD": ["h264_amf", "hevc_amf"],
            "Intel": ["h264_qsv", "hevc_qsv"]
        }
        self.codec_combo.addItems(self.cpu_codecs)
        codec_layout.addWidget(self.codec_combo)
        codec_layout.addStretch()
        
        # 帧率
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("帧率:"))
        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["原始", "24", "25", "30", "60"])
        fps_layout.addWidget(self.fps_combo)
        fps_layout.addStretch()
        
        # 码率控制
        bitrate_layout = QHBoxLayout()
        bitrate_layout.addWidget(QLabel("码率控制:"))
        self.bitrate_combo = QComboBox()
        self.bitrate_combo.addItems(["CRF", "CBR", "VBR", "ABR"])
        bitrate_layout.addWidget(self.bitrate_combo)
        bitrate_layout.addStretch()
        
        # CRF值
        self.crf_layout = QHBoxLayout()
        self.crf_layout.addWidget(QLabel("CRF值:"))
        self.crf_slider = QSlider(Qt.Horizontal)
        self.crf_slider.setRange(0, 51)
        self.crf_slider.setValue(23)
        self.crf_slider.setTickInterval(1)
        self.crf_slider.setTickPosition(QSlider.TicksBelow)
        self.crf_value_label = QLabel("23")
        self.crf_layout.addWidget(self.crf_slider)
        self.crf_layout.addWidget(self.crf_value_label)
        self.crf_layout.addStretch()
        self.crf_slider.valueChanged.connect(self.update_crf_value)
        
        # 码率值
        self.bitrate_value_layout = QHBoxLayout()
        self.bitrate_value_layout.addWidget(QLabel("码率(Kbps):"))
        self.bitrate_value_edit = QLineEdit()
        self.bitrate_value_edit.setPlaceholderText("例如: 2000")
        self.bitrate_value_layout.addWidget(self.bitrate_value_edit)
        self.bitrate_value_layout.addStretch()
        self.bitrate_value_layout_widget = QWidget()
        self.bitrate_value_layout_widget.setLayout(self.bitrate_value_layout)
        self.bitrate_value_layout_widget.setVisible(False)  # 默认隐藏
        
        encoding_options_layout.addLayout(processing_layout)
        encoding_options_layout.addWidget(self.gpu_brand_layout_widget)
        encoding_options_layout.addLayout(self.threads_layout)
        encoding_options_layout.addLayout(codec_layout)
        encoding_options_layout.addLayout(fps_layout)
        encoding_options_layout.addLayout(bitrate_layout)
        # 包装CRF控件到Widget用于可见性控制
        self.crf_layout_widget = QWidget()
        self.crf_layout_widget.setLayout(self.crf_layout)
        encoding_options_layout.addWidget(self.crf_layout_widget)
        encoding_options_layout.addWidget(self.bitrate_value_layout_widget)

        # 最小码率
        self.min_bitrate_layout = QHBoxLayout()
        self.min_bitrate_layout.addWidget(QLabel("最小码率(Kbps):"))
        self.min_bitrate_edit = QLineEdit()
        self.min_bitrate_edit.setPlaceholderText("例如: 1000")
        self.min_bitrate_layout.addWidget(self.min_bitrate_edit)
        self.min_bitrate_layout.addStretch()
        self.min_bitrate_layout_widget = QWidget()
        self.min_bitrate_layout_widget.setLayout(self.min_bitrate_layout)
        self.min_bitrate_layout_widget.setVisible(False)
        encoding_options_layout.addWidget(self.min_bitrate_layout_widget)

        # 最大码率
        self.max_bitrate_layout = QHBoxLayout()
        self.max_bitrate_layout.addWidget(QLabel("最大码率(Kbps):"))
        self.max_bitrate_edit = QLineEdit()
        self.max_bitrate_edit.setPlaceholderText("例如: 4000")
        self.max_bitrate_layout.addWidget(self.max_bitrate_edit)
        self.max_bitrate_layout.addStretch()
        self.max_bitrate_layout_widget = QWidget()
        self.max_bitrate_layout_widget.setLayout(self.max_bitrate_layout)
        self.max_bitrate_layout_widget.setVisible(False)
        encoding_options_layout.addWidget(self.max_bitrate_layout_widget)

        # 缓冲区大小
        self.bufsize_layout = QHBoxLayout()
        self.bufsize_layout.addWidget(QLabel("缓冲区大小(Kbps):"))
        self.bufsize_edit = QLineEdit()
        self.bufsize_edit.setPlaceholderText("例如: 2000")
        self.bufsize_layout.addWidget(self.bufsize_edit)
        self.bufsize_layout.addStretch()
        self.bufsize_layout_widget = QWidget()
        self.bufsize_layout_widget.setLayout(self.bufsize_layout)
        self.bufsize_layout_widget.setVisible(False)
        encoding_options_layout.addWidget(self.bufsize_layout_widget)

        self.encoding_options_group.setLayout(encoding_options_layout)
        self.encoding_options_group.setVisible(True)  # 默认显示，后续根据选择调整
        
        # 连接信号
        self.cpu_radio.toggled.connect(self.on_processing_type_changed)
        self.gpu_radio.toggled.connect(self.on_processing_type_changed)
        self.gpu_brand_combo.currentIndexChanged.connect(self.on_gpu_brand_changed)
        self.bitrate_combo.currentIndexChanged.connect(self.on_bitrate_mode_changed)
        
        # 初始化UI状态
        self.on_processing_type_changed()
        # 确保在初始化UI状态前创建所有控件
        self.on_bitrate_mode_changed()
        
        # 添加到主布局
        layout.addWidget(file_group)
        layout.addWidget(subtitle_type_group)
        layout.addWidget(self.encoding_options_group)
        layout.addLayout(button_layout)
        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("QProgressBar { height: 30px; border-radius: 8px; background-color: #f5f5f7; border: 1px solid #d2d2d7; } QProgressBar::chunk { background-color: #0071e3; border-radius: 6px; }")
        layout.addWidget(self.progress_bar)
        layout.addWidget(QLabel("日志输出:"))
        layout.addWidget(self.log_output)
        
        self.setLayout(layout)
        
    def select_video_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi *.mkv *.mov)")
        if file_path:
            self.video_path_edit.setText(file_path)
        
    def select_subtitle_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择字幕文件", "", "字幕文件 (*.srt *.ass)")
        if file_path:
            self.subtitle_path_edit.setText(file_path)
        
    def select_output_file(self):
        # 使用getExistingDirectory来选择目录而不是文件
        directory = QFileDialog.getExistingDirectory(self, "选择输出目录", "")
        if directory:
            self.output_path_edit.setText(directory)
        
    def start_muxing(self):
        video_path = self.video_path_edit.text()
        subtitle_path = self.subtitle_path_edit.text()
        output_dir = self.output_path_edit.text()
        
        # 检查输入文件是否存在
        if not os.path.exists(video_path):
            self.log_output.append("错误: 视频文件不存在")
            return
        
        if not os.path.exists(subtitle_path):
            self.log_output.append("错误: 字幕文件不存在")
            return
        
        if not output_dir:
            self.log_output.append("错误: 请选择输出目录")
            return
        
        # 生成输出文件路径
        # 如果用户没有自定义文件名，则使用默认命名规则
        if self.output_name_edit.text().strip():
            base_name = self.output_name_edit.text().strip()
        else:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            subtitle_type = "hard" if self.hard_subtitle_radio.isChecked() else "soft"
            base_name = f"{base_name}_{subtitle_type}_sub"
        
        # 获取用户选择的输出格式
        output_format = self.output_format_combo.currentText()
        output_path = os.path.join(output_dir, f"{base_name}.{output_format}")
        
        # 收集编码选项
        encoding_options = {
            'codec': self.codec_combo.currentText(),
            'processing_type': 'CPU' if self.cpu_radio.isChecked() else 'GPU',
            'threads': self.threads_combo.currentText(),
            'fps': self.fps_combo.currentText(),
            'bitrate_mode': self.bitrate_combo.currentText(),
            'crf_value': self.crf_slider.value(),
            'bitrate_value': self.bitrate_value_edit.text().strip(),
            'min_bitrate': self.min_bitrate_edit.text().strip(),
            'max_bitrate': self.max_bitrate_edit.text().strip(),
            'bufsize': self.bufsize_edit.text().strip()
        }

        # 验证编码选项
        from utils.video_encoder import VideoEncoder
        validation_errors = VideoEncoder.validate_encoding_options(encoding_options)
        if validation_errors:
            for error in validation_errors:
                self.log_output.append(f"错误: {error}")
            return

        # 构建转码命令
        subtitle_type = 'hard' if self.hard_subtitle_radio.isChecked() else 'soft'
        command = VideoEncoder.build_transcode_command(
            video_path=video_path,
            subtitle_path=subtitle_path,
            output_path=output_path,
            subtitle_type=subtitle_type,
            encoding_options=encoding_options
        )
        
        # 执行FFmpeg命令
        self.log_output.append(f"执行命令: {' '.join(command)}")
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        # 重置进度条
        self.progress_bar.setValue(0)
        self.total_duration = None
        self.process.start('ffmpeg', command[1:])
        
    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode('utf-8')
        self.log_output.append(stdout)
        
    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode('utf-8')
        self.log_output.append(stderr)

        # 解析FFmpeg进度信息
        if not hasattr(self, 'total_duration'):
            self.total_duration = None

        for line in stderr.split('\n'):
            # 解析总时长
            if not self.total_duration and 'Duration:' in line:
                try:
                    duration_str = line.split('Duration: ')[1].split(',')[0].strip()
                    h, m, s = duration_str.split(':')
                    s, ms = s.split('.')
                    self.total_duration = int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000
                except (IndexError, ValueError):
                    pass

            # 解析当前时间
            if 'time=' in line:
                try:
                    time_str = line.split('time=')[1].split()[0]
                    h, m, s = time_str.split(':')
                    s, ms = s.split('.')
                    current_time = int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000

                    if self.total_duration and self.total_duration > 0:
                        progress = (current_time / self.total_duration) * 100
                        self.progress_bar.setValue(int(min(progress, 100)))
                except (IndexError, ValueError):
                    pass
        
    def process_finished(self):
        self.log_output.append("字幕合成完成!")
        
    def on_subtitle_type_changed(self):
        # 根据字幕类型更新支持的格式列表
        if self.hard_subtitle_radio.isChecked():
            supported_formats = self.hard_subtitle_formats
            # 显示硬字幕编码选项
            self.encoding_options_group.setVisible(True)
        else:
            supported_formats = self.soft_subtitle_formats
            # 隐藏硬字幕编码选项
            self.encoding_options_group.setVisible(False)
            
        # 更新下拉框中的格式列表
        current_format = self.output_format_combo.currentText()
        self.output_format_combo.clear()
        self.output_format_combo.addItems(supported_formats)
        
        # 如果当前选择的格式在新的支持列表中，则保持选择
        if current_format in supported_formats:
            index = self.output_format_combo.findText(current_format)
            if index >= 0:
                self.output_format_combo.setCurrentIndex(index)
                
    def on_processing_type_changed(self):
        # 根据处理方式更新编码器列表
        if self.cpu_radio.isChecked():
            # 显示CPU相关选项
            self.gpu_brand_layout_widget.setVisible(False)
            self.threads_layout.itemAt(1).widget().setVisible(True)  # 显示线程数选择
            
            # 更新编码器列表为CPU编码器
            current_codec = self.codec_combo.currentText()
            self.codec_combo.clear()
            self.codec_combo.addItems(self.cpu_codecs)
            
            # 如果当前选择的编码器在CPU编码器中，则保持选择
            if current_codec in self.cpu_codecs:
                index = self.codec_combo.findText(current_codec)
                if index >= 0:
                    self.codec_combo.setCurrentIndex(index)
        else:
            # 显示GPU相关选项
            self.gpu_brand_layout_widget.setVisible(True)
            self.threads_layout.itemAt(1).widget().setVisible(False)  # 隐藏线程数选择
            
            # 更新编码器列表为当前GPU品牌的编码器
            self.on_gpu_brand_changed()
            
    def update_crf_value(self, value):
        self.crf_value_label.setText(str(value))

    def on_gpu_brand_changed(self):
        # 根据GPU品牌更新编码器列表
        brand = self.gpu_brand_combo.currentText()
        if brand in self.gpu_codecs:
            current_codec = self.codec_combo.currentText()
            self.codec_combo.clear()
            self.codec_combo.addItems(self.gpu_codecs[brand])
            
            # 如果当前选择的编码器在新列表中，则保持选择
            if current_codec in self.gpu_codecs[brand]:
                index = self.codec_combo.findText(current_codec)
                if index >= 0:
                    self.codec_combo.setCurrentIndex(index)
                    
    def on_bitrate_mode_changed(self):
        bitrate_mode = self.bitrate_combo.currentText()
        if bitrate_mode == "CRF":
            self.crf_layout_widget.setVisible(True)
            self.bitrate_value_layout_widget.setVisible(False)
            self.min_bitrate_layout_widget.setVisible(False)
            self.max_bitrate_layout_widget.setVisible(False)
            self.bufsize_layout_widget.setVisible(False)
        else:
            self.crf_layout_widget.setVisible(False)
            self.bitrate_value_layout_widget.setVisible(True)
            
            # 根据不同码率模式显示相应参数
            if bitrate_mode == "CBR":
                self.min_bitrate_layout_widget.setVisible(True)
                self.max_bitrate_layout_widget.setVisible(True)
                self.bufsize_layout_widget.setVisible(True)
            elif bitrate_mode == "VBR":
                self.min_bitrate_layout_widget.setVisible(False)
                self.max_bitrate_layout_widget.setVisible(True)
                self.bufsize_layout_widget.setVisible(True)
            elif bitrate_mode == "ABR":
                self.min_bitrate_layout_widget.setVisible(True)
                self.max_bitrate_layout_widget.setVisible(True)
                self.bufsize_layout_widget.setVisible(True)
            else:
                self.min_bitrate_layout_widget.setVisible(False)
                self.max_bitrate_layout_widget.setVisible(False)
                self.bufsize_layout_widget.setVisible(False)