from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling
import json
import os
from datetime import datetime

UPLOAD_FOLDER = "/uploads/"


class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def login(self, username, password):
        result = {}
        response = {}
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM `user` WHERE username = %s AND password = %s"
        cursor.execute(sql, [username, password])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            response['status'] = 'success'
            response['message'] = 'Login Success!'
            result['status_code'] = 200
        else:
            response['status'] = 'error'
            response['message'] = 'Your Username and Password are Not Defined!'
            result['status_code'] = 404

        cursor.close()
        result['response'] = response
        return result

    def get_all_news(self):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `news` n WHERE is_deleted = 0 AND ABS(DATEDIFF(created_date, CURRENT_DATE)) < 31"
        cursor.execute(sql)
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count > 0:
            result['status_code'] = 200
            response['status'] = "success"
            response['data'] = []
            cursor.execute(sql)
            for row in cursor.fetchall():
                sql2 = "SELECT * FROM `files` f JOIN `news` n ON f.id_news = n.id WHERE n.id = %s AND f.is_deleted = 0"
                cursor.execute(sql2, [row[0]])
                files = []
                for row2 in cursor.fetchall():
                    files.append(
                        {"id_file": row2[0], "filename": row2[1]})

                response['data'].append(
                    {"id_news": row[0], "content": row[1], "files": files})
        else:
            result['status_code'] = 404
            response['status'] = "error"
            response['message'] = 'There are still no news'

        cursor.close()
        result['response'] = response
        return result

    def get_news(self, news_id):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `news` WHERE id = %s AND is_deleted = 0 AND ABS(DATEDIFF(created_date, CURRENT_DATE)) < 31"
        cursor.execute(sql, [int(news_id)])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            result['status_code'] = 200
            response['status'] = "success"
            response['id_news'] = row[0][0]
            response['content'] = row[0][1]
            response['files'] = []

            sql2 = "SELECT * FROM `files` f JOIN `news` n ON f.id_news = n.id WHERE n.id = %s AND f.is_deleted = 0"
            cursor.execute(sql2, [row[0][0]])
            for row2 in cursor.fetchall():
                response['files'].append(
                    {"id_file": row2[0], "filename": row2[1]})
        else:
            result['status_code'] = 404
            response['status'] = "error"
            response['message'] = 'News not found'

        cursor.close()
        result['response'] = response
        return result

    def delete_news(self, news_id):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `news` WHERE id = %s AND is_deleted = 0 AND ABS(DATEDIFF(created_date, CURRENT_DATE)) < 31"
        cursor.execute(sql, [int(news_id)])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            sql2 = "UPDATE `files` SET `is_deleted` = 1 WHERE id_news = %s"
            cursor.execute(sql2, [int(news_id)])
            self.connection.commit()
            sql3 = "UPDATE `news` SET `is_deleted` = 1 WHERE id = %s"
            cursor.execute(sql3, [int(news_id)])
            self.connection.commit()

            result['status_code'] = 200
            response['status'] = "success"
            response['message'] = 'News deleted successfully'
        else:
            result['status_code'] = 404
            response['status'] = "error"
            response['message'] = 'News not found'

        cursor.close()
        result['response'] = response
        return result

    def delete_file(self, file_id):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `files` WHERE id = %s AND is_deleted = 0"
        cursor.execute(sql, [int(file_id)])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            sql2 = "UPDATE `files` SET `is_deleted` = 1 WHERE id = %s"
            cursor.execute(sql2, [int(file_id)])
            self.connection.commit()

            result['status_code'] = 200
            response['status'] = "success"
            response['message'] = 'File deleted successfully'
        else:
            result['status_code'] = 404
            response['status'] = "error"
            response['message'] = 'File not found'

        cursor.close()
        result['response'] = response
        return result

    # def delete_news(self, news_id):
    #     result = {}
    #     response = {}
    #     cursor = self.connection.cursor()
    #     sql = "SELECT * FROM `news` WHERE id = %s"
    #     cursor.execute(sql, [int(news_id)])
    #     row = cursor.fetchall()
    #     row_count = cursor.rowcount

    #     if row_count == 1:
    #         sql2 = "SELECT * FROM `files` WHERE id_news = %s"
    #         cursor.execute(sql2, [int(news_id)])

    #         for row2 in cursor.fetchall():
    #             sql3 = "DELETE FROM `files` WHERE id = %s"
    #             cursor.execute(sql3, [int(row2[0])])
    #             self.connection.commit()

    #             os.remove(UPLOAD_FOLDER + row2[1])

    #         # self.connection.commit()
    #         sql4 = "DELETE FROM `news` WHERE id = %s"
    #         cursor.execute(sql4, [int(news_id)])
    #         self.connection.commit()

    #         result['status_code'] = 200
    #         response['status'] = "success"
    #         response['message'] = 'News deleted successfully'
    #     else:
    #         result['status_code'] = 404
    #         response['status'] = "error"
    #         response['message'] = 'News not found'

    #     cursor.close()
    #     result['response'] = response
    #     return result

    def add_news(self, content, date):
        result = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `news` WHERE description = %s AND is_deleted = 0"
        cursor.execute(sql, [content])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            result['status_code'] = 404
            result['status'] = "error"
            result['message'] = 'Create new content!'
        else:
            sql2 = "INSERT INTO `news`(`id`, `description`, `created_date`) VALUES (NULL, %s, %s)"
            cursor.execute(sql2, [content, date])
            self.connection.commit()

            sql3 = "SELECT * FROM `news` WHERE description = %s"
            cursor.execute(sql3, [content])
            row2 = cursor.fetchone()

            result['status_code'] = 200
            result['status'] = "success"
            result['id_news'] = row2[0]

        cursor.close()
        return result

    def upload_files(self, filename, news_id):
        result = {}
        cursor = self.connection.cursor()
        sql = "INSERT INTO `files`(`id`, `filepath`, `id_news`) VALUES (NULL, %s, %s)"
        cursor.execute(sql, [filename, int(news_id)])
        self.connection.commit()

        result['status_code'] = 200
        result['status'] = "success"
        cursor.close()
        return result

    def edit_content_news(self, news_id, content):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `news` WHERE id = %s AND is_deleted = 0 AND ABS(DATEDIFF(created_date, CURRENT_DATE)) < 31"
        cursor.execute(sql, [int(news_id)])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            sql = "UPDATE `news` SET `description`= %s WHERE id = %s"
            cursor.execute(sql, [content, int(news_id)])
            self.connection.commit()

            result['status_code'] = 200
            response['status'] = "success"
            response['message'] = 'Content edited successfully'
        else:
            result['status_code'] = 404
            response['status'] = "error"
            response['message'] = 'News not found'

        cursor.close()
        result['response'] = response
        return result

    def download_file(self, file_id):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT f.* FROM `files` f JOIN news n ON n.id = f.id_news WHERE f.id = %s AND n.is_deleted = 0 AND f.is_deleted = 0 AND ABS(DATEDIFF(created_date, CURRENT_DATE)) < 31"
        cursor.execute(sql, [int(file_id)])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            result['status_code'] = 200
            response['status'] = "success"
            response['filename'] = row[0][1]
        else:
            result['status_code'] = 404
            response['status'] = "error"
            response['message'] = 'File not found'

        cursor.close()
        result['response'] = response
        return result


class DatabaseProvider(DependencyProvider):

    connection_pool = None

    def setup(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='127.0.0.1',
                database='soa_news_board',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
