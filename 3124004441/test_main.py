from main import get_simhash, hamming_distance, calc_similarity

def test_same_text():
    """相同文本相似度为1"""
    s1 = "人工智能"
    h1 = get_simhash(s1)
    h2 = get_simhash(s1)
    assert hamming_distance(h1, h2) == 0
    assert calc_similarity(0) == 1.0

def test_diff_text():
    """完全不同文本"""
    h1 = get_simhash("篮球运动")
    h2 = get_simhash("雨后山林")
    dist = hamming_distance(h1, h2)
    sim = calc_similarity(dist)
    assert 0 <= sim <= 1.0
