#!/usr/bin/env python3

import sys

try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    from html import escape
except ImportError:
    sys.exit('ERROR: It seems like you are not running Python 3. '
             'This script only works with Python 3!')

main_doc = '''
<!doctype html>
<html><body>
<h1>Bad Bank</h1>
<h2>Keeping your vulnerabilities safe!</h2>
<h3>Login</h3>
<form method="get" action='/login'>
    Username: <input type="text" name="uname" id="uname" value="{uname}"><br>
    Password: <input type="password" name="password" id="password"><br>
    <input type="submit" value="Login">
</form>
<h3>Become a Customer Now!</h3>
<form action="/customer" method="get">
    Your Name: <input type="text" name="name" value="Jane Doe" /><br />
    Your City: <input type="text" name="city" value="Rapid Vaults" /><br />
    ...<br />
    <input type="submit" value="Register now" />
</form>
</body></html>
'''

login_doc = '''
<!doctype html>
<html><body>
<h1>Bad Bank</h1>
<h2>Keeping your vulnerabilities safe!</h2>
<h3>ERROR</h3>
<p>Invalid username or password.</p>
<p><a href="/?uname={uname}">Go back</a></p>
</body></html>
'''

customer_doc = '''
<!doctype html>
<html><body>
<h1>Bad Bank</h1>
<h2>Keeping your vulnerabilities safe!</h2>
<h3>Sorry!</h3>
<p>We cannot take any more customers at the moment as our database is out of memory.</p>
</body></html>
'''


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_dict = urlparse(self.path)  # parse URL string into dictionary
        get_dict = parse_qs(url_dict.query)  # select query string from URL dictionary
        user_name = ''
        if 'uname' in get_dict:
            user_name = get_dict['uname'][0]

        self.send_response(200)
        self.send_header('Set-Cookie', 'safeid=verysecuresecretstring')
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        self.send_header('X-XSS-Protection', '0')  # disables XSS protection in the browser

        self.end_headers()

        path = url_dict.path

        if path == '/login':
            output = login_doc.format(uname=escape(user_name))
        elif path == '/customer':
            output = customer_doc
        else:
            output = main_doc.format(uname=user_name)

        self.wfile.write(bytes(output, 'UTF-8'))


if __name__ == '__main__':
    server = HTTPServer(('', 8081), MyHandler)
    print("Starting web server on http://localhost:8081/")
    server.serve_forever()
