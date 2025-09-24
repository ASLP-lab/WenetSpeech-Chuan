import os
from tqdm import tqdm  # 进度条库


# 定义文件路径
emotion_file_path = '/home/work_nfs14/yhdai/workspace/Wenetspeech_Dialect/tools/domain_data/data/emotion_results.txt'  # 第一个文件路径，包含wav路径和情感标签
age_gender_file_path = '/home/work_nfs14/yhdai/workspace/Wenetspeech_Dialect/tools/domain_data/data/gender_age.txt'  # 第二个文件路径，包含key、年龄和性别信息
text_file_path = '/home/work_nfs14/yhdai/workspace/Wenetspeech_Dialect/WSC_demopage/raw/samples_text'  # 第三个文件路径，包含key和其他信息
output_file_path = '/home/work_nfs14/yhdai/workspace/Wenetspeech_Dialect/WSC_demopage/raw/samples_text_emo_age_gender'  # 输出的新文件路径

# Step 1: 读取第一个文件并创建情感标签映射
emotion_map = {}
with open(emotion_file_path, 'r') as file_1:
    for line in file_1:
        parts = line.strip().split('|')
        if len(parts) == 3:
            key, _, emotion = parts
            emotion_map[key] = emotion

# Step 2: 读取第二个文件并创建年龄和性别映射
age_gender_map = {}
with open(age_gender_file_path, 'r') as file_2:
    for line in file_2:
        parts = line.strip().split('|')
        if len(parts) == 5:  # 假设第二个文件是按照 5 部分切分
            key, _, age, gender = parts[0], parts[1], parts[3], parts[4]
            age_gender_map[key] = (age, gender)

# Step 3: 读取第三个文件，匹配情感、年龄、性别并写入新文件
with open(text_file_path, 'r') as file_3, open(output_file_path, 'w') as output_file:
    lines = file_3.readlines()  # 一次性读取所有内容
    total_lines = len(lines)
    
    for i, line in tqdm(enumerate(lines), total=total_lines, desc="Processing", unit="line"):
        parts = line.strip().split('|||')
        if len(parts) >= 2:
            key_and_info = parts[0].split()
            key = key_and_info[2]  # 提取key部分 (例如: 'sc0000006_36680_44180')
            
            # 查找匹配的情感标签
            emotion = emotion_map.get(key, 'Unknown')  # 默认情感为 'Unknown'，如果没有找到
            
            # 查找匹配的年龄和性别
            age, gender = age_gender_map.get(key, ('Unknown', 'Unknown'))  # 默认值为 'Unknown'
            
            # 写入新的文件（原内容 + 匹配的情感标签、年龄、性别）
            new_line = f"{line.strip()} ||| emotion={emotion} ||| age={age} ||| gender={gender}\n"
            output_file.write(new_line)
    
    print(f"处理完成，输出文件：{output_file_path}")

