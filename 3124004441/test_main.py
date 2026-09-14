import pytest
from main import calc_similarity

def test_same_text():
    """完全相同文本，相似度接近1"""
    assert calc_similarity("今天天气很好", "今天天气很好") == pytest.approx(1.0)

def test_no_same_text():
    """完全无关短句，放宽阈值"""
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
    s1 = "红苹果，很好吃"
    s2 = "红苹果，很甜"
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
    """标点不同，文字相同，加长文本"""
    s1 = "你好！世界，计算机科学。"
    s2 = "你好世界计算机科学"
    sim = calc_similarity(s1, s2)
    assert sim > 0.8

def test_chinese_english_mix():
    """中英文混合文本"""
    s1 = "Python语言，学习SimHash算法"
    s2 = "Python语言，学习哈希算法"
    sim = calc_similarity(s1, s2)
    assert 0.3 < sim < 0.95

def test_number_mixed():
    """带数字文本"""
    s1 = "2025年，计算机专业学习simhash算法"
    s2 = "2025计算机专业学习simhash算法"
    sim = calc_similarity(s1, s2)
    assert sim > 0.8
