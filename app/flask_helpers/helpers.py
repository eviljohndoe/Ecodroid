import subprocess


def shell(cmd, strip=True, silent=False):
    if not silent:
        print '> ' + cmd
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    if process.wait() == 0:
        if strip:
            return process.communicate()[0].rstrip()
        return process.communicate()[0]
    return ''


class Device(object):
    _adb = None
    imei = None
    serial = None

    def __init__(self, app=None, sn=None):
        self.app = app
        if app is not None:
            self.init_app(app)
            if sn is not None:
                self._adb = app.config['ADB'] + ' -s ' + str(sn) + ' '
        # self._adb = app.config['ADB'] + ' '
        # if sn is not None:
        #    self._adb = app.config['ADB'] + ' -s ' + str(sn) + ' '
        #    self.serial = sn

    def init_app(self, app):
        """Set up this instance for use with *app*, if no app was passed to
        the constructor.
        """
        self.app = app
        self._adb = self.app.config['ADB'] + ' '

    def set_serial(self, sn):
        self.serial = sn
        self._adb = self.app.config['ADB'] + ' '
        if sn is not None:
            self._adb = self.app.config['ADB'] + ' -s ' + str(sn) + ' '

    def detect(self):
        self.set_serial(None)
        return shell(self._adb + "devices | grep -v List | cut -f 1")

    def adb(self, cmd, silent=False):
        return shell(self._adb + str(cmd), True, silent)

    def shell(self, cmd, silent=False):
        return self.adb('shell ' + str(cmd), silent)

    def getIMEI(self):
        imei = self.shell("service call iphonesubinfo 1 | awk -F \"\'\" \'{print $2}\' | sed \'s/[^0-9A-F]*//g\'")
        return imei.replace('\n', '')

    def installPackage(self, path):
        shell(self._adb + 'install -r ' + str(path))
