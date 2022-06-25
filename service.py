from nameko.rpc import rpc
from dependencies import database, session


class NewsService:

    name = 'news_service'
    database = database.DatabaseProvider()

    @rpc
    def login(self, username, password):
        news = self.database.login(username, password)
        return news

    @rpc
    def get_all_news(self):
        news = self.database.get_all_news()
        return news

    @rpc
    def get_news(self, news_id):
        news = self.database.get_news(news_id)
        return news

    @rpc
    def delete_news(self, news_id):
        news = self.database.delete_news(news_id)
        return news

    @rpc
    def add_news(self, content, date):
        news = self.database.add_news(content, date)
        return news

    @rpc
    def delete_file(self, file_id):
        file = self.database.delete_file(file_id)
        return file

    @rpc
    def upload_files(self, filename, news_id):
        news = self.database.upload_files(filename, news_id)
        return news

    @rpc
    def edit_content_news(self, news_id, content):
        news = self.database.edit_content_news(news_id, content)
        return news

    @rpc
    def download_file(self, file_id):
        news = self.database.download_file(file_id)
        return news


class SessionService:

    name = 'session_service'
    session_provider = session.SessionProvider()

    @rpc
    def set_session_data(self, username):
        session = self.session_provider.set_session_data(username)
        return session

    @rpc
    def delete_session(self, username):
        session = self.session_provider.delete_session(username)
        return session
