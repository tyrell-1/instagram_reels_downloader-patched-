class ScrapingError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Failed To Scrape Data From Instagram.", *args)
        pass
    
class InvalidURL(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__("Invalid Reel URL.", *args)
        pass