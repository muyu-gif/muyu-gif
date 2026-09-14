import jieba

def get_simhash(text: str, hash_bits=64) -> int:
    """
    计算文本的64位SimHash值，返回整数
    """
    if not text.strip():
        return 0
    
    # 分词
    words = jieba.lcut(text)
    # 初始化权重数组
    v = [0] * hash_bits
    
    for word in words:
        # 简单hash得到单词hash值
        word_hash = hash(word) & ((1 << hash_bits) - 1)
        for i in range(hash_bits):
            bit = (word_hash >> i) & 1
            if bit == 1:
                v[i] += 1
            else:
                v[i] -= 1
    # 生成最终simhash
    simhash_val = 0
    for i in range(hash_bits):
        if v[i] > 0:
            simhash_val |= (1 << i)
    return simhash_val


def calc_similarity(text1: str, text2: str) -> float:
    """
    计算两段文本相似度，返回0~1之间小数
    """
    h1 = get_simhash(text1)
    h2 = get_simhash(text2)
    # 整数异或，统计汉明距离
    xor = h1 ^ h2
    hamming_dist = bin(xor).count("1")
    # 相似度换算
    similarity = 1 - (hamming_dist / 64.0)
    return similarity


if __name__ == "__main__":
    # 本地测试示例
    s1 = "我爱人工智能"
    s2 = "我爱机器学习"
    print(calc_similarity(s1, s2))
