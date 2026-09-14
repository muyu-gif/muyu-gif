import sys
import hashlib
import re

def get_hash(text: str) -> int:
    """对字符串做md5哈希，返回整数"""
    return int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16)

def simhash(text: str, hash_bits=64) -> int:
    """生成文本的simhash值"""
    # 清洗文本：去掉标点、空白符
    words = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', text)
    if not words:
        return 0
    # 初始化权重向量
    v = [0] * hash_bits
    for word in words:
        h = get_hash(word)
        for i in range(hash_bits):
            bit = (h >> i) & 1
            if bit == 1:
                v[i] += 1
            else:
                v[i] -= 1
    # 生成指纹
    fingerprint = 0
    for i in range(hash_bits):
        if v[i] > 0:
            fingerprint |= (1 << i)
    return fingerprint

def hamming_distance(hash1: int, hash2: int) -> int:
    """计算两个哈希的汉明距离"""
    return bin(hash1 ^ hash2).count('1')

def calc_similarity(text1: str, text2: str) -> float:
    """计算文本重复率，返回0~1之间浮点数"""
    if len(text1.strip()) == 0 and len(text2.strip()) == 0:
        return 1.0
    if len(text1.strip()) == 0 or len(text2.strip()) == 0:
        return 0.0
    h1 = simhash(text1)
    h2 = simhash(text2)
    dist = hamming_distance(h1, h2)
    similarity = 1 - dist / 64
    return similarity

def main():
    # 判断命令行参数数量
    if len(sys.argv) != 4:
        print("参数错误！使用方法：python main.py 原文路径 抄袭文件路径 输出文件路径")
        sys.exit(1)
    orig_path = sys.argv[1]
    copy_path = sys.argv[2]
    out_path = sys.argv[3]
    try:
        with open(orig_path, 'r', encoding='utf-8') as f:
            orig_text = f.read()
        with open(copy_path, 'r', encoding='utf-8') as f:
            copy_text = f.read()
    except FileNotFoundError:
        print("错误：找不到指定文件")
        sys.exit(2)
    except Exception as e:
        print(f"读取文件出错：{e}")
        sys.exit(3)

    # 计算重复率
    rate = calc_similarity(orig_text, copy_text)
    # 写入文件，保留2位小数
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"{rate:.2f}")

if __name__ == "__main__":
    main()
