#!/usr/bin/env python3

import sys

try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
except ImportError:
    sys.exit('ERROR: It seems like you are not running Python 3. '
             'This script only works with Python 3!')

main_doc = '''
<!doctype html>
<html><body>
<h1>SEC Community</h1>
<h2>Exiting security vulnerabilities and more 8082a!</h2>
<h3>User Lookup</h3>
Please enter a query string:
<form method="get">
    <input type="text" name="lookup" value="">
    <input type="submit" name="send" value="OK">
</form>
{result}
</body></html>
'''

users = ['Werner Foo', 'Hans Bar', 'Arno Nym', 'Ein Tester', 'Chris Sitescripting', 'Mai Eskuel', 'B. Nutzer',
         'Noch Wer']


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_dict = urlparse(self.path)  # parse URL string into dictionary
        get_dict = parse_qs(url_dict.query)  # select query string from URL dictionary

        self.send_response(200)
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        self.send_header('X-XSS-Protection', '0')  # disables XSS protection in the browser

        self.end_headers()

        result = ''
        if 'lookup' in get_dict:
            lookup = get_dict['lookup'][0]
            result = f'<h3>Search Results for {lookup}</h3>'
            for user in users:
                if user.lower().find(lookup.lower()) >= 0:
                    result += f'{user}<br>'

        output = main_doc.format(result=result)
        self.wfile.write(bytes(output, 'UTF-8'))


if __name__ == '__main__':
    server = HTTPServer(('', 8082), MyHandler)
    print("Starting web server on http://localhost:8082/")
    server.serve_forever()
