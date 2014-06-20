import logging

class HTMLInjector:
    """ This class allows you to inject data into the response returned
    from the web server.
    """

    _instance = None

    @staticmethod
    def getInstance():
        if HTMLInjector._instance is None:
            HTMLInjector._instance = HTMLInjector()

        return HTMLInjector._instance

    def __init__(self):
        self.injection_code = []

    def setInjectionCode(self, code):
        self.injection_code.append(code)

    def inject(self, data):
        injection_code = ' '.join(self.injection_code)

        return data.replace('</body>', '%s</body>' % injection_code)
