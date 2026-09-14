import unittest
import os
from main import get_tokens, simhash, hamming_distance, calc_similarity, read_file

class TestPaperCheck(unittest.TestCase):
    # 1.普通相同文本
    def test_same_text(self):
        t1 = "今天是星期天，天气晴，今天晚上我要去看电影。"
        t2 = "今天是星期天，天气晴，今天晚上我要去看电影。"
        tokens1 = get_tokens(t1)
        tokens2 = get_tokens(t2)
        fp1 = simhash(tokens1)
        fp2 = simhash(tokens2)
        sim = calc_similarity(fp1, fp2)
        self.assertEqual(sim, 1.0)

    # 2.样例：轻微改写
    def test_slight_modify(self):
        t1 = "今天是星期天，天气晴，今天晚上我要去看电影。"
        t2 = "今天是周天，天气晴朗，我晚上要去看电影。"
        tokens1 = get_tokens(t1)
        tokens2 = get_tokens(t2)
        fp1 = simhash(tokens1)
        fp2 = simhash(tokens2)
        sim = calc_similarity(fp1, fp2)
        self.assertGreater(sim, 0.6)

    #3.完全无关文本
    def test_total_diff(self):
        t1 = "人工智能"
        t2 = "篮球足球"
        tokens1 = get_tokens(t1)
        tokens2 = get_tokens(t2)
        fp1 = simhash(tokens1)
        fp2 = simhash(tokens2)
        sim = calc_similarity(fp1, fp2)
        self.assertLess(sim,0.3)

    #4.空文本
    def test_empty_string(self):
        t1 = ""
        tokens1 = get_tokens(t1)
        self.assertEqual(len(tokens1),0)

    #5.只有标点
    def test_only_punctuation(self):
        t1 = "，。！？；："
        tokens1 = get_tokens(t1)
        self.assertEqual(len(tokens1),0)

    #6.原文长，抄袭版短
    def test_long_short(self):
        t1 = "今天是星期天，天气晴，今天晚上我要去看电影，吃完晚饭出门。"
        t2 = "今天晚上我要去看电影"
        tokens1 = get_tokens(t1)
        tokens2 = get_tokens(t2)
        fp1 = simhash(tokens1)
        fp2 = simhash(tokens2)
        sim = calc_similarity(fp1, fp2)
        self.assertGreater(sim,0.2)

    #7.只有单个词语
    def test_single_word(self):
        t1 = "计算机"
        t2 = "计算机"
        tokens1 = get_tokens(t1)
        tokens2 = get_tokens(t2)
        fp1 = simhash(tokens1)
        fp2 = simhash(tokens2)
        self.assertEqual(calc_similarity(fp1,fp2),1.0)

    #8.文本带换行
    def test_line_break(self):
        t1 = "今天是星期天\n天气晴"
        t2 = "今天是星期天，天气晴"
        tokens1 = get_tokens(t1)
        tokens2 = get_tokens(t2)
        fp1 = simhash(tokens1)
        fp2 = simhash(tokens2)
        self.assertAlmostEqual(calc_similarity(fp1,fp2),1.0)

    #9.文件读取正常
    def test_read_file(self):
        with open("tmp_test.txt","w",encoding="utf-8") as f:
            f.write("测试文件读取")
        content = read_file("tmp_test.txt")
        self.assertEqual(content,"测试文件读取")
        os.remove("tmp_test.txt")

    #10.不存在的文件（异常）
    def test_file_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            read_file("not_exist_1234.txt")

if __name__ == '__main__':
    unittest.main()
