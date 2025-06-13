
# -*- coding: utf-8 -*-
import re
if __name__ == '__main__':
    link_pattern = r'(https?://\S+)'

    # 输入文件和输出文件路径
    input_file = '/Users/xiang/xiang/study/Python/selenium_python/xisai_book/doc/系统分析师考试全程指导.txt'
    output_file = '/Users/xiang/xiang/study/Python/selenium_python/xisai_book/doc/系统分析师考试全程指导_URL.txt'

    # 打开输入文件进行读取
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.readlines()

    # 处理每一行内容，查找并修改其中的链接
    modified_lines = []
    for line in content:
        modified_line = re.sub(link_pattern, r'![](\1)', line)
        modified_lines.append(modified_line.strip())  # 去除行尾的换行符并保存到列表

    # 在每行之间插入一个空行
    modified_lines_with_empty_lines = []
    for line in modified_lines:
        modified_lines_with_empty_lines.append(line)
        modified_lines_with_empty_lines.append('')  # 插入空行

    # 将修改后的内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(modified_lines_with_empty_lines).strip() + '\n')  # 使用join方法连接列表元素并写入文件

    print(f"文件处理完成，结果保存在 {output_file}")