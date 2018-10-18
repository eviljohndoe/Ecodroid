import os
from werkzeug.utils import secure_filename


class Upload:
    app = None

    def __init__(self, app):
        self.app = app

    def upload(self, destination, ext_conf, files):
        if type(files) is list:
            file_names = []
            for _file in files:
                filename = self.upload_file(destination, self.app.config[ext_conf], _file)
                file_names.append(filename)
            return file_names
        else:
            filename = self.upload_file(destination, self.app.config[ext_conf], files)
            return filename

    def upload_file(self, destination, ext, file):
        # Check if the file is one of the allowed types/extensions
        if file and self.allowed_files(file.filename, ext):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload folder we setup
            file.save(os.path.join(destination, filename))
            return filename

    def allowed_files(self, filename, ext):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ext
