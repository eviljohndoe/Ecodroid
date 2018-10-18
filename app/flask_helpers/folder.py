import os
import shutil


class Folder:
    app = None

    def __init__(self, app):
        self.app = app

    def create_folder(self, directory):
        self.check_project_folder()
        folder = os.path.join(self.app.config['PROJECT_FOLDER'], directory)
        if os.path.exists(folder) is False:
            os.mkdir(folder)
        return folder

    def create_sub_folder(self, folder, sub_folder):
        self.check_project_folder()
        root_folder = os.path.join(self.app.config['PROJECT_FOLDER'], folder)
        if os.path.exists(root_folder) is False:
            os.mkdir(root_folder)
        _folder = os.path.join(root_folder, sub_folder)
        if os.path.exists(_folder) is False:
            os.mkdir(_folder)
        return _folder

    def check_project_folder(self):
        if os.path.exists(self.app.config['PROJECT_FOLDER']) is False:
            os.mkdir(self.app.config['PROJECT_FOLDER'])

    def rename_project(self, old_project, new_project):
        self.check_project_folder()
        old_project_folder = os.path.join(self.app.config['PROJECT_FOLDER'], old_project)
        new_project_folder = os.path.join(self.app.config['PROJECT_FOLDER'], new_project)
        if os.path.exists(old_project_folder) is False:
            self.create_folder(new_project_folder)
        else:
            os.rename(old_project_folder, new_project_folder)
        return new_project_folder

    def remove_project(self, project):
        self.check_project_folder()
        project_folder = os.path.join(self.app.config['PROJECT_FOLDER'], project)
        if os.path.exists(project_folder):
            shutil.rmtree(project_folder)

    def remove(self, file):
        if os.path.exists(file):
            os.remove(file)