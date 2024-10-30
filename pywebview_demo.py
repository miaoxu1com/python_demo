import webview

# https://pywebview.flowrl.com/examples/save_file_dialog.html
#　https://syaofox.github.io/p/%E5%8D%95%E8%BD%BB%E9%87%8F%E7%9A%84gui%E7%BC%96%E7%A8%8Bpywebview/
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
