import jieba
import hashlib

def get_tokens(text: str):
    """分词，过滤空白字符"""
    words = jieba.lcut(text)
    tokens = [w.strip() for w in words if w.strip()]
    return tokens

def simhash(tokens, hash_bits=64):
    """计算simhash指纹"""
    v = [0] * hash_bits
    for token in tokens:
        h = hashlib.sha256(token.encode('utf-8')).digest()
        h_int = int.from_bytes(h, byteorder='big')
        h_int = h_int & ((1 << hash_bits) - 1)
        for i in range(hash_bits):
            bit = (h_int >> i) & 1
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

def hamming_distance(fp1, fp2):
    """计算汉明距离"""
    return bin(fp1 ^ fp2).count('1')

def calc_similarity(fp1, fp2):
    """根据汉明距离计算相似度"""
    dist = hamming_distance(fp1, fp2)
    return 1.0 - dist / 64.0

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    import sys
    if len(sys.argv) != 4:
        print("用法: python main.py 原文文件 待查文件 输出结果文件")
        sys.exit(1)
    ori_path = sys.argv[1]
    test_path = sys.argv[2]
    out_path = sys.argv[3]

    text_ori = read_file(ori_path)
    text_test = read_file(test_path)

    tokens_ori = get_tokens(text_ori)
    tokens_test = get_tokens(text_test)

    fp_ori = simhash(tokens_ori)
    fp_test = simhash(tokens_test)

    similarity = calc_similarity(fp_ori, fp_test)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"{similarity:.2%}")

if __name__ == "__main__":
    main()
