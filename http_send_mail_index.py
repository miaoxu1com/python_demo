import webview

from http_send_mail import login_email
from http_send_mail import send_mail


def read_cookies(window):
    cookies = window.get_cookies()
    for c in cookies:
        print(c.output())


class API:
    email_url = ""

    def send_email(self, send_email_url):
        self.email_url = send_email_url
        send_mail(self.email_url)
        return f"流水成功发送到{self.email_url}"

    def open_email(self):
        session = login_email(self.email_url)
        cookie_strings = []
        for cookie in session.cookies:
            cookie_string = f"{cookie.name}={cookie.value}; domain={cookie.domain}; path={cookie.path}; secure;"
            if cookie.has_nonstandard_attr('HttpOnly'):
                cookie_string += ' HttpOnly'
            cookie_strings.append(cookie_string)
        cooks = '; '.join(cookie_strings)
        print(cooks)
        return cooks


if __name__ == '__main__':
    api = API()
    window = webview.create_window('邮箱发送', 'template/index.html', width=800, height=350, resizable=False,
                                   js_api=api)
    webview.start(debug=True, private_mode=False, http_server=True, http_port=13377)
