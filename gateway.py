import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import Flask, send_file, current_app, send_from_directory
from datetime import datetime
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'uploads/')
UPLOAD_FOLDER = "uploads"
EXTENSION_HEADER = {
    'txt': 'text/plain',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
}


class NewsGatewayService:
    name = 'news_gateway'
    news_rpc = RpcProxy('news_service')
    session_rpc = RpcProxy('session_service')

    @http('POST', '/login')
    def login_account(self, request):
        req = request.json
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            login = self.news_rpc.login(req['username'], req['password'])

            if int(login['status_code']) == 200:
                username = {
                    'username': req['username']
                }
                session_id = self.session_rpc.set_session_data(username)
                response = Response(json.dumps(login['response'], indent=4))
                response.set_cookie('sessionID', session_id)

                return response
            else:
                return int(login['status_code']), (json.dumps(login['response'], indent=4))
        else:
            return 400, json.dumps({"status": "error", "message": "Log Out First!"}, indent=4)

    @http('GET', '/logout')
    def logout_account(self, request):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            logout = self.session_rpc.delete_session('sessionID')
            response = Response(json.dumps(logout, indent=4))
            response.delete_cookie('sessionID')

            return response

    @http('GET', '/news')
    def get_all_news(self, request):
        news = self.news_rpc.get_all_news()
        return int(news['status_code']), (json.dumps(news['response'], indent=4))

    @http('GET', '/news/<int:news_id>')
    def get_news(self, request, news_id):
        news = self.news_rpc.get_news(news_id)
        return int(news['status_code']), (json.dumps(news['response'], indent=4))

    @http('DELETE', '/news/<int:news_id>')
    def delete_news(self, request, news_id):
        news = self.news_rpc.delete_news(news_id)
        return int(news['status_code']), (json.dumps(news['response'], indent=4))

    @http('POST', '/news/add')
    def uploads(self, request):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            date = datetime.today().strftime('%Y-%m-%d')
            news = self.news_rpc.add_news(request.form['content'], date)

            if news['status_code'] == 200:
                app = Flask(__name__)
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                f = request.files.getlist('file')
                for files in f:
                    file_type = (files.filename).split('.')[-1]
                    filename = ''.join(
                        e for e in files.filename if e.isalnum()).replace(file_type, '')
                    file_name = str(
                        hash(str(news['id_news']))) + '_' + filename + '.' + file_type
                    upload = self.news_rpc.upload_files(
                        file_name, news['id_news'])

                    filename = secure_filename(file_name)
                    files.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))

                return 200,  json.dumps({"status": "success", "message": "News added successfully!"}, indent=4)
            else:
                return 404,  json.dumps({"status": "error", "message": "Create new content!"}, indent=4)

    @http('PUT', '/news/edit/content/<int:news_id>')
    def edit_content_news(self, request, news_id):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            news = self.news_rpc.edit_content_news(
                news_id, request.form['content'])
            return int(news['status_code']), (json.dumps(news['response'], indent=4))

    @http('PUT', '/news/add/files/<int:news_id>')
    def edit_file_news(self, request, news_id):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            news = self.news_rpc.get_news(news_id)

            if news['status_code'] == 200:
                app = Flask(__name__)
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                f = request.files.getlist('file')
                for files in f:
                    file_type = (files.filename).split('.')[-1]
                    filename = (''.join(
                        e for e in files.filename if e.isalnum())).replace(file_type, '')

                    file_name = str(
                        hash(str(news_id))) + '_' + filename + '.' + file_type
                    add_file = self.news_rpc.upload_files(
                        file_name, news_id)

                    filename = secure_filename(file_name)
                    files.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))

                return 200,  json.dumps({"status": "success", "message": "Files added to news successfully!"}, indent=4)
            else:
                return int(news['status_code']), (json.dumps(news['response'], indent=4))

    @http('DELETE', '/file/<int:file_id>')
    def delete_file(self, request, file_id):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            news = self.news_rpc.delete_file(file_id)
            return int(news['status_code']), (json.dumps(news['response'], indent=4))

    @http('GET', '/file/<int:file_id>')
    def download_file(self, request, file_id):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            news = self.news_rpc.download_file(file_id)

            if news['status_code'] == 200:
                response = news['response']
                filename = response['filename']

                response = Response(
                    open(UPLOADS_PATH + '/' + filename, 'rb').read())
                file_type = filename.split('.')[-1]

                response.headers['Content-Type'] = EXTENSION_HEADER[file_type]
                response.headers['Content-Disposition'] = 'attachment; filename={}'.format(
                    filename)

                return response
            else:
                return int(news['status_code']), (json.dumps(news['response'], indent=4))
