from main import calc_similarity

def test_same_text():
    # 完全相同文本
    sim = calc_similarity("人工智能", "人工智能")
    assert sim >= 0.9

def test_diff_text():
    # 完全无关文本
    sim = calc_similarity("人工智能", "篮球足球")
    assert sim <= 0.2

def test_part_text():
    # 部分相似文本
    sim = calc_similarity("今天天气晴朗适合学习", "今天天气晴朗适合看书")
    assert 0.4 <= sim <= 0.9
