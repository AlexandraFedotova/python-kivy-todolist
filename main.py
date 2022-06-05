import os

from kivy.lang import Builder
from kivymd.app import MDApp
from model import *


from py_view.TaskOnlyScreen import TaskOnlyScreen
from py_view.TasksInCategoryScreen import TasksInCategoryScreen
from py_view.CategoriesListScreen import CategoriesListScreen
from py_view.MainApp import MainApp


class MyApp(MDApp, Notebook):
    dialog = None
    #notebook = None

    def set_screen(self, screen_name):
        if self.screen_manager.has_screen(screen_name):
            self.screen_manager.current = screen_name

    def create_task_only_screen(self, instance):
        if not self.screen_manager.has_screen('taskOnly'):
            self.screen_manager.add_widget(TaskOnlyScreen(name='taskOnly', instance=instance))
        self.set_screen('taskOnly')

    def remove_task_only_screen(self):
        if self.screen_manager.has_screen('taskOnly'):
            screen = self.screen_manager.get_screen('taskOnly')
            screen.edit_task()
            self.set_screen('tasksInCategory')
            self.screen_manager.remove_widget(screen)

    def show_tasks_in_categories_screen(self, category):
        self.current_category = category
        self.set_screen('tasksInCategory')

    def on_start(self):
        self.categoriesListScreen.set_categories_list()

    def on_stop(self):
        self.write_tasks_in_file(self.path_to_data)

    def __init__(self, **kwargs):
        self.screen_manager = None
        self.categoriesListScreen = None
        self.tasksInCategoryScreen = None
        self.current_category = 'Base'
        self.path_to_data = 'data/tasks.txt'
        super(MyApp, self).__init__(**kwargs)

    def loadAllKvFiles(self, directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            kv_file = os.path.join(directory_kv_files, kv_file)
            if os.path.isfile(kv_file):
                Builder.load_file(kv_file)

    def build(self):
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.theme_style = "Light"

        #self.notebook = Notebook()
        self.loadAllKvFiles(os.path.join(self.directory, 'kv_view'))
        self.read_tasks_from_file(self.path_to_data)
        self.title = "Список задач"
        self.icon = "./data/images/logo.png"

        self.screen_manager = MainApp()
        self.categoriesListScreen = self.screen_manager.get_screen('categoriesList')
        self.tasksInCategoryScreen = self.screen_manager.get_screen('tasksInCategory')

        return self.screen_manager


if __name__ == "__main__":
    MyApp().run()
