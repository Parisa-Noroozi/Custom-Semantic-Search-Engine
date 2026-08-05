class SearchResponse:

    def __init__(self):

        self.query = None

        self.results = []

        self.total_results = 0

        self.search_time = 0

        self.corrected_query = ""

        self.expanded_query = []

        self.intents = []

        self.created_at = None