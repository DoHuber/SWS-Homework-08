#!/usr/bin/env python3

import sys
import secrets

try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    from http import cookies
except ImportError:
    sys.exit('ERROR: It seems like you are not running Python 3. '
             'This script only works with Python 3!')

login_form_doc = '''
<!doctype html>
<html><body>
{message}
<form method="post" action="/login">
    User: <input name="user">
    <br>
    Password: <input name="pass" type="password">
<br>
<input type="submit" value="go">
</form>
<small>Hint: Username alice, Password bob.</small>
</body></html>
'''

logged_in_doc = '''
<!doctype html>
<html lang="en">
<body>
{message}
<br>
<form method="post" action="/logout">
    <input type="submit" value="Log out"><br>
    <input type="hidden" name="logout" value="true">
</form>
</body>
</html>'''

sessions = {}


class MyHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.close_connection = True

    # Changes the session id (sid), namely by replacing the current sid with a new, random one.
    # In order to do this, the following is done: a new sid is generated, after which
    # the session is copied to the session dictionary under the new sid
    # After that, the session information at the old sid is deleted, and a header to make the client
    # set a new cookie is sent.
    def change_session_id(self):
        sid = self.get_or_create_session()
        new_sid = secrets.token_urlsafe()
        sessions[new_sid] = sessions[sid]
        del sessions[sid]
        self.send_header('Set-Cookie', 'sid=' + new_sid)

    def get_or_create_session(self):
        cookie_dict = cookies.SimpleCookie(self.headers['Cookie'])

        if 'sid' in cookie_dict:
            sid = cookie_dict['sid'].value

        if 'sid' not in cookie_dict or sid not in sessions:
            sid = secrets.token_urlsafe()  # generate some random token
            self.send_header('Set-Cookie', 'sid=' + sid)
            sessions[sid] = {}  # the session is initially empty

        return sid

    def do_GET(self):
        self.send_response(200)
        sid = self.get_or_create_session()
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        self.end_headers()

        if 'username' in sessions[sid]:
            message = "Welcome! You are logged in as " + sessions[sid]['username']
            output = logged_in_doc.format(message=message)
        else:
            message = 'Not logged in.'
            output = login_form_doc.format(message=message)

        self.wfile.write(bytes(output, 'UTF-8'))

    def do_POST(self):
        content_length = self.headers['Content-Length']
        body = self.rfile.read(int(content_length))
        qs_dict = parse_qs(str(body, 'UTF-8'))

        if 'logout' not in qs_dict and qs_dict['user'][0] == 'alice' and qs_dict['pass'][0] == 'bob':
            # login was successful, redirect user to first page.
            self.send_response(303)  # redirection status code "See Other"
            sid = self.get_or_create_session()
            self.send_header('Content-Type', 'text/html;charset=utf-8')
            sessions[sid]['username'] = 'alice'
            self.send_header('Location', '/')
            self.change_session_id()
            self.end_headers()
        elif qs_dict['logout'][0] == 'true':
            # Logout button was pressed, goodbye, user!
            self.send_response(303)
            sid = self.get_or_create_session()
            sessions[sid] = {}
            self.send_header('Content-Type', 'text/html;charset=utf-8')
            self.send_header('Location', '/')
            self.change_session_id()
            self.end_headers()
        else:
            # wrong credentials, show form again
            self.send_response(200)
            self.send_header('Content-Type', 'text/html;charset=utf-8')
            self.end_headers()
            message = 'Wrong credentials.'
            output = login_form_doc.format(message=message)
            self.wfile.write(bytes(output, 'UTF-8'))


if __name__ == '__main__':
    server = HTTPServer(('', 8081), MyHandler)
    server.serve_forever()
