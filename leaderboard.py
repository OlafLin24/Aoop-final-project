import os

class Leaderboard:
    def __init__(self, filename='leaderboard.txt', max_entries=5):
        """初始化高分榜"""
        self.filename = filename
        self.max_entries = max_entries
        self.scores = self.load_scores()

    def load_scores(self):
        """讀取高分榜"""
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            scores = [line.strip().split(',') for line in file.readlines()]
            return [(name, int(score)) for name, score in scores]

    def save_scores(self):
        """保存高分榜"""
        with open(self.filename, 'w') as file:
            for name, score in self.scores:
                file.write(f"{name},{score}\n")

    def add_score(self, name, score):
        """新增分數並更新高分榜"""
        self.scores.append((name, score))
        self.scores = sorted(self.scores, key=lambda x: x[1], reverse=True)[:self.max_entries]
        self.save_scores()

    def get_scores(self):
        """獲取當前高分榜"""
        return self.scores
