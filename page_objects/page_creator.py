from page_objects.main_page import MainPage


class PageCreator:
    def __init__(self, page, url):
        self.page = page
        self.url = url

    def main_page(self):
        return MainPage(self.page, self.url)
