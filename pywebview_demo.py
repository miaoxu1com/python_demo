import webview


class API:
    def say_hello(self):
        print("Hello from Python!")

    def get_message(self):
        return "This message is from Python."

    def open_file(self):
        file_path = window.create_file_dialog(webview.OPEN_DIALOG)
        print("Selected file:", file_path)

if __name__ == '__main__':
    api = API()
    window = webview.create_window('pywebviewExample', 'template/index.html', js_api=api)
    webview.start()
