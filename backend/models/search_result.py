class SearchResult:

    def __init__(self, title, content, score):

        self.title = title

        self.content = content

        self.score = score

        self.rank = ""

        self.matched_keywords = []

        self.source = ""