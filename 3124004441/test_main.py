from main import calc_similarity

def test_same_text():
    """完全相同文本，相似度接近1"""
    a = "今天天气不错"
    b = "今天天气不错"
    sim = calc_similarity(a, b)
    assert sim > 0.95

def test_part_text():
    """部分相似文本"""
    a = "今天天气不错适合出门"
    b = "今天天气不错适合散步"
    sim = calc_similarity(a, b)
    assert 0.6 < sim < 0.95

def test_diff_text():
    """完全不同文本"""
    a = "苹果香蕉水果"
    b = "汽车火车交通工具"
    sim = calc_similarity(a, b)
    assert sim < 0.6
