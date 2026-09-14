from main import get_simhash, hamming_distance, calc_similarity

def test_same_text():
    """相同文本：海明距离=0，相似度=1.0"""
    s1 = "人工智能"
    h1 = get_simhash(s1)
    h2 = get_simhash(s1)
    assert hamming_distance(h1, h2) == 0
    assert calc_similarity(0) == 1.0

def test_diff_text():
    """不同文本相似度在0~1区间"""
    h1 = get_simhash("篮球运动")
    h2 = get_simhash("雨后山林")
    dist = hamming_distance(h1, h2)
    sim = calc_similarity(dist)
    assert 0 <= sim <= 1.0

def test_simhash_stable():
    txt = "计算机系统结构课程作业"
    hash_a = get_simhash(txt)
    hash_b = get_simhash(txt)
    assert hash_a == hash_b
