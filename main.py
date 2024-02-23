import struct
import os
from pprint import pprint


def read_wav_header(filepath):
    with open(filepath, "rb") as file:
        riff, size, fformat = struct.unpack('4sI4s', file.read(12))
        if riff != b'RIFF' or fformat != b'WAVE':
            print("This is not a valid WAV file.")
            return

        # Read next chunk
        while True:
            subchunk2ID, subchunk2Size = struct.unpack('4sI', file.read(8))
            if subchunk2ID == b'fmt ':
                fmt_size, audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = struct.unpack('IHHIIHH', file.read(20))
                print(
                    f"Format: {audio_format}, Channels: {num_channels}, Sample Rate: {sample_rate}, Byte Rate: {byte_rate}, Block Align: {block_align}, Bits per Sample: {bits_per_sample}")
                break
            else:
                file.seek(subchunk2Size, 1)  # Skip to next chunk if not 'fmt '


def check_file_start(filepath, length=1024 * 20):
    with open(filepath, "rb") as file:
        data = file.read(length)
        return data


# data_start = check_file_start('Agt_Truth_Skill_1_Start_SP3_01.wav')
# data_start = check_file_start('SCRATCH_BASS_01.wav')

def add_wav_header(filepath, output_filepath, channels=1, sample_rate=48000, bits_per_sample=24):
    # 计算文件大小和数据块大小
    file_size = os.path.getsize(filepath) + 36  # 文件总大小加上头部大小，减去RIFF和WAVE标识符大小
    data_size = file_size - 44  # 减去WAV头部的固定大小

    # 构造WAV头部信息
    wav_header = b'RIFF' + (file_size - 8).to_bytes(4, byteorder='little') + b'WAVE' + \
                 b'fmt ' + (16).to_bytes(4, byteorder='little') + (1).to_bytes(2, byteorder='little') + \
                 (channels).to_bytes(2, byteorder='little') + (sample_rate).to_bytes(4, byteorder='little') + \
                 (sample_rate * channels * bits_per_sample // 8).to_bytes(4, byteorder='little') + \
                 (channels * bits_per_sample // 8).to_bytes(2, byteorder='little') + \
                 (bits_per_sample).to_bytes(2, byteorder='little') + \
                 b'data' + (data_size).to_bytes(4, byteorder='little')

    # 读取原始音频数据并将其与WAV头部合并写入新文件
    with open(filepath, 'rb') as original_file:
        audio_data = original_file.read()

    with open(output_filepath, 'wb') as new_file:
        new_file.write(wav_header)
        new_file.write(audio_data)


add_wav_header('SNARE top 57.15_18.wav', 'SNARE top 57.15_18_repaired.wav')


def get_wav_in_folder(folder_path):
    wav_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".wav"):
                # 获取文件完整路径
                file_path = os.path.join(root, file)
                # 获取去除尾缀的文件名
                file_name = os.path.splitext(file)[0]
                wav_list.append([file_path, file_name])

    return wav_list


def repair_wav_files(wav_list, repaired_folder_path):
    for index, wav in enumerate(wav_list):
        print(f"Processing {index + 1}/{len(wav_list)}: {wav[1]}")
        add_wav_header(wav[0], os.path.join(repaired_folder_path, f"{wav[1]}_repaired.wav"))


def main():
    broken_folder_path = r"D:\dvatiOFF\Tools\General\repairwav\Wav Files From Jeremy\Wav Files From Jeremy\Leader_Deleter Audio Files"
    repaired_folder_path = r"D:\dvatiOFF\Tools\General\repairwav\Wav Files From Jeremy\Wav Files From Jeremy\Leader_Deleter Audio Files-Repaired"
    repair_wav_files(get_wav_in_folder(broken_folder_path), repaired_folder_path)


if __name__ == "__main__":
    main()
