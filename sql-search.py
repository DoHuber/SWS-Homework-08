#!/usr/bin/env python3

import sys

try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
except ImportError:
    sys.exit('ERROR: It seems like you are not running Python 3. '
             'This script only works with Python 3!')
import sqlite3
from html import escape

DATABASE_FILE = 'sql-search.sqlite3'

main_doc = '''
<!doctype html>
<html><body>
<h1>SEC community</h1>
	Exiting security bugs and more!
	<h2>User Search</h2>
	Please enter a search string:
	<form method="get">
	    <input type="text" name="search" value="{search}" />
	    <input type="submit" name="send" value="OK" />
	</form>
{result}
</body></html>
'''

result_prefix = '''
<h2>Results</h2>
<table>
<tr><th>Username</th><th>Registered since...</th></tr>
'''

result_row = '''
<tr>
<td>{nick}</td>
<td>{regdate}</td>
</tr>
'''

result_suffix = '''
</table>
'''


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_dict = urlparse(self.path)  # parse URL string into dictionary
        get_dict = parse_qs(url_dict.query)  # select query string from URL dictionary

        self.send_response(200)
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        self.end_headers()

        search = ''
        result = ''
        if 'search' in get_dict:
            search = get_dict['search'][0]

            connection = sqlite3.connect(
                DATABASE_FILE)  # could also be replaced by a connection to a remote sql server, e.g., a mysql instance
            sql = f"SELECT nick, regdate FROM community_users3 WHERE nick LIKE '{search}'"
            print(f"Executing SQL: {sql}")
            res = connection.execute(sql)

            result = result_prefix
            for row in res:
                result += result_row.format(nick=row[0], regdate=row[1])

            result += result_suffix

        output = main_doc.format(result=result, search=escape(search))
        self.wfile.write(bytes(output, 'UTF-8'))


if __name__ == '__main__':
    server = HTTPServer(('', 8081), MyHandler)
    print("Starting web server on http://localhost:8081/")
    server.serve_forever()
