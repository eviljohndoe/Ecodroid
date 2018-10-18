class Url:
    app = None
    request = None

    def __init__(self, app, request):
        self.app = app
        self.request = request

    def create_url(self):
        print("test")