import pytest
from main import calc_similarity

def test_same_text():
    """完全相同文本，相似度接近1"""
    assert calc_similarity("今天天气很好", "今天天气很好") == pytest.approx(1.0)

def test_no_same_text():
    """完全无关短句"""
    sim = calc_similarity("今天天气很好", "猫咪喜欢吃鱼")
    assert 0.3 < sim < 0.7

def test_both_empty():
    """两个都是空字符串"""
    assert calc_similarity("", "") == 1.0

def test_one_empty():
    """其中一个为空"""
    assert calc_similarity("", "测试文字") == 0.0

def test_part_same():
    """部分文字重合"""
    s1 = "红苹果，很好吃，富含维生素，适合日常食用"
    s2 = "红苹果，很甜，富含维生素，适合日常食用"
    sim = calc_similarity(s1, s2)
    assert 0.4 < sim < 0.95

def test_long_text_same():
    """长文本完全一致"""
    t1 = "信息技术发展迅速，人工智能改变生活。计算机科学与技术是热门专业。" * 5
    t2 = t1
    assert calc_similarity(t1, t2) == pytest.approx(1.0)

def test_long_text_diff():
    """长文本少量修改"""
    t1 = "信息技术发展迅速，人工智能改变生活。计算机科学与技术是热门专业。" *5
    t2 = t1.replace("人工智能", "大数据")
    sim = calc_similarity(t1, t2)
    assert 0.5 < sim < 0.95

def test_punctuation_diff():
    """标点不同，文字完全一样，仅去掉符号"""
    s1 = "你好！世界，计算机科学，simhash算法用于文本查重。"
    s2 = "你好世界计算机科学simhash算法用于文本查重"
    sim = calc_similarity(s1, s2)
    assert sim > 0.4

def test_chinese_english_mix():
    """中英文混合文本"""
    s1 = "Python语言，学习SimHash算法，用于论文查重系统"
    s2 = "Python语言，学习哈希算法，用于论文查重系统"
    sim = calc_similarity(s1, s2)
    assert 0.3 < sim < 0.95

def test_number_mixed():
    """带数字，仅标点差异，词语几乎相同"""
    s1 = "2025年，计算机专业学习simhash算法，实现论文相似度检测"
    s2 = "2025年计算机专业学习simhash算法，实现论文相似度检测"
    sim = calc_similarity(s1, s2)
    assert sim > 0.4
