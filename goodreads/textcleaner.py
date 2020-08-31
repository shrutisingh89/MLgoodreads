import re

class GoodreadsTextCleaner():

    @classmethod
    def clean_all(cls,text):
        text = GoodreadsTextCleaner.clean_html_tags(text)
        return GoodreadsTextCleaner.clean_extra_spaces(text)

    @classmethod
    def clean_html_tags(cls, text):
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        return re.sub(cleanr, '', str(text))

    @classmethod
    def clean_extra_spaces(cls, text):
        return ' '.join(text.split())