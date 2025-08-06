import os

class VideoEncoder:
    @staticmethod
    def build_transcode_command(video_path, subtitle_path, output_path, subtitle_type, encoding_options):
        """
        构建视频转码的FFmpeg命令
        :param video_path: 输入视频路径
        :param subtitle_path: 字幕文件路径 (可为None)
        :param output_path: 输出文件路径
        :param subtitle_type: 字幕类型 ('hard' 或 'soft')
        :param encoding_options: 编码选项字典，包含以下键:
            - codec: 编码器
            - processing_type: 'CPU' 或 'GPU'
            - threads: 线程数
            - fps: 帧率
            - bitrate_mode: 码率控制模式
            - crf_value: CRF值
            - bitrate_value: 码率值
            - min_bitrate: 最小码率
            - max_bitrate: 最大码率
            - bufsize: 缓冲区大小
        :return: FFmpeg命令列表
        """
        command = ['ffmpeg', '-i', video_path]

        # 添加字幕处理
        if subtitle_type == 'hard' and subtitle_path:
            command.extend(['-vf', f'subtitles={subtitle_path}'])
        elif subtitle_type == 'soft' and subtitle_path:
            command.extend(['-i', subtitle_path])

        # 添加视频编码器
        command.extend(['-c:v', encoding_options['codec']])

        # 添加CPU线程数参数
        if encoding_options['processing_type'] == 'CPU':
            threads = encoding_options.get('threads')
            if threads and threads != '默认':
                command.extend(['-threads', threads])

        # 添加帧率参数
        fps = encoding_options.get('fps')
        if fps and fps != '原始':
            command.extend(['-r', fps])

        # 添加码率控制参数
        bitrate_mode = encoding_options.get('bitrate_mode', 'CRF')
        codec = encoding_options['codec']

        if bitrate_mode == 'CRF':
            crf_value = str(encoding_options.get('crf_value', 23))
            if codec.startswith(('libx264', 'libx265', 'libaom-av1')):
                command.extend(['-crf', crf_value])
            elif codec.startswith('libvpx-vp9'):
                command.extend(['-crf', crf_value, '-b:v', '0'])
            elif codec.startswith(('h264_nvenc', 'hevc_nvenc')):
                command.extend(['-cq', crf_value])
            elif codec.startswith(('h264_amf', 'hevc_amf')):
                command.extend(['-qp_i', crf_value, '-qp_p', crf_value, '-qp_b', crf_value])
            elif codec.startswith(('h264_qsv', 'hevc_qsv')):
                command.extend(['-q', crf_value])

        elif bitrate_mode in ['CBR', 'VBR', 'ABR']:
            bitrate_value = encoding_options.get('bitrate_value')
            if not bitrate_value:
                raise ValueError("码率值未设置")

            command.extend(['-b:v', f'{bitrate_value}k'])

            if bitrate_mode == 'CBR':
                min_bitrate = encoding_options.get('min_bitrate')
                max_bitrate = encoding_options.get('max_bitrate')
                bufsize = encoding_options.get('bufsize')
                if min_bitrate and max_bitrate and bufsize:
                    command.extend([
                        '-minrate', f'{min_bitrate}k',
                        '-maxrate', f'{max_bitrate}k',
                        '-bufsize', f'{bufsize}k'
                    ])
                if codec.startswith(('h264_amf', 'hevc_amf')):
                    command.extend(['-rc', 'cbr'])
                elif codec.startswith(('h264_qsv', 'hevc_qsv')):
                    command.extend(['-b_strategy', '0'])

            elif bitrate_mode == 'VBR':
                max_bitrate = encoding_options.get('max_bitrate')
                bufsize = encoding_options.get('bufsize')
                if max_bitrate and bufsize:
                    command.extend(['-maxrate', f'{max_bitrate}k', '-bufsize', f'{bufsize}k'])
                if codec.startswith(('h264_amf', 'hevc_amf')):
                    command.extend(['-rc', 'vbr_peak'])

            elif bitrate_mode == 'ABR':
                min_bitrate = encoding_options.get('min_bitrate')
                max_bitrate = encoding_options.get('max_bitrate')
                bufsize = encoding_options.get('bufsize')
                if min_bitrate and max_bitrate and bufsize:
                    command.extend([
                        '-minrate', f'{min_bitrate}k',
                        '-maxrate', f'{max_bitrate}k',
                        '-bufsize', f'{bufsize}k'
                    ])
                if codec.startswith(('h264_nvenc', 'hevc_nvenc', 'h264_amf', 'hevc_amf', 'h264_qsv', 'hevc_qsv')):
                    command.extend(['-rc', 'abr'])

        # 音频编码保持不变
        command.extend(['-c:a', 'copy'])

        # 软字幕处理
        if subtitle_type == 'soft' and subtitle_path:
            output_format = os.path.splitext(output_path)[1][1:].lower()
            if output_format == 'mp4':
                command.extend(['-c:s', 'mov_text'])
            elif output_format == 'mkv':
                command.extend(['-c:s', 'srt'])
            else:
                command.extend(['-c:s', 'copy'])

        # 输出文件
        command.append(output_path)

        return command

    @staticmethod
    def validate_encoding_options(encoding_options):
        """验证编码选项的有效性"""
        errors = []
        bitrate_mode = encoding_options.get('bitrate_mode', 'CRF')

        if bitrate_mode != 'CRF':
            if not encoding_options.get('bitrate_value'):
                errors.append("请设置码率值")

            if bitrate_mode == 'CBR' or bitrate_mode == 'ABR':
                if not encoding_options.get('min_bitrate'):
                    errors.append("请设置最小码率")

            if bitrate_mode in ['CBR', 'VBR', 'ABR']:
                if not encoding_options.get('max_bitrate'):
                    errors.append("请设置最大码率")
                if not encoding_options.get('bufsize'):
                    errors.append("请设置缓冲区大小")

        return errors