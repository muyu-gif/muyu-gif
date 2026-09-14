import sys
import jieba
import hashlib

def get_word_hash(word: str, bits=64):
    """使用md5生成固定64bit哈希，替代Python内置随机hash"""
    md5 = hashlib.md5(word.encode('utf-8')).digest()
    val = int.from_bytes(md5, byteorder="big") & ((1 << bits) - 1)
    return val

def get_simhash(text: str, hash_bits=64):
    """生成稳定SimHash指纹"""
    words = jieba.lcut(text)
    v = [0] * hash_bits
    for word in words:
        h = get_word_hash(word, hash_bits)
        for i in range(hash_bits):
            bit = (h >> i) & 1
            if bit == 1:
                v[i] += 1
            else:
                v[i] -= 1
    fingerprint = 0
    for i in range(hash_bits):
        if v[i] > 0:
            fingerprint |= (1 << i)
    return fingerprint

def hamming_distance(hash1: int, hash2: int):
    """计算两个指纹海明距离"""
    return bin(hash1 ^ hash2).count('1')

def calc_similarity(hd, bits=64):
    """海明距离转为相似度 0~1"""
    return 1.0 - hd / bits

def read_file(file_path):
    """读取文本文件，utf8"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败：{file_path}, 错误：{e}")
        sys.exit(1)

if __name__ == "__main__":
    print("程序启动！")
    if len(sys.argv) != 4:
        print("用法：python main.py 原文.txt 对比文本.txt 输出结果.txt")
        print("示例：python main.py orig.txt orig_0.8_add.txt ans.txt")
        sys.exit(0)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    out_path = sys.argv[3]

    text1 = read_file(file1_path)
    text2 = read_file(file2_path)

    hash1 = get_simhash(text1)
    hash2 = get_simhash(text2)
    dist = hamming_distance(hash1, hash2)
    sim = calc_similarity(dist)

    result_text = f"海明距离：{dist}\n文本相似度：{sim:.2f}"
    print(result_text)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(result_text)
    print(f"结果已写入：{out_path}")
