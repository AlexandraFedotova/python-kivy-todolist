from kivymd.app import MDApp
from model import *
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.list import TwoLineIconListItem, OneLineRightIconListItem, OneLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.core.window import Window

Window.size = (350, 622)

notebook = Notebook()


class MainApp(ScreenManager):
    pass


class CategoryItem(OneLineRightIconListItem):
    def __init__(self, category_name, **kwargs):
        super(CategoryItem, self).__init__(**kwargs)
        self.text = category_name


class CategoriesListScreen(MDScreen):
    categories_list = ObjectProperty()
    dialog = None

    def delete_category(self, obj=None):
        try:
            notebook.remove_category(name_of_required_category=self.category_for_deleting)
            self.set_categories_list()
            self.close_dialog()
        except Exception:
            print('Error with deleting category')

    def show_dialog_delete_category(self, instance):
        self.category_for_deleting = instance.text
        close_button = MDFlatButton(text='CLOSE', on_release=self.close_dialog)
        remove_button = MDFlatButton(text='REMOVE', on_release=self.delete_category)
        self.dialog = MDDialog(
            title='Удалить категорию?',
            text=instance.text,
            buttons=[close_button, remove_button]
        )
        self.dialog.open()

    def show_dialog_create_category(self):
        close_button = MDFlatButton(text='CLOSE', on_release=self.close_dialog)
        self.create_button = MDFlatButton(text='CREATE', on_release=self.create_category)
        content = MDBoxLayout(orientation='vertical', size_hint_y=None, height='50sp')
        self.text_field = MDTextField(hint_text='category name')
        content.add_widget(self.text_field)
        self.dialog = MDDialog(
            title='Create category',
            type="custom",
            #size_hint=(0.8, 1),
            content_cls=content,
            buttons=[close_button, self.create_button],
        )
        self.dialog.open()

    def close_dialog(self, obj=None):
        try:
            self.dialog.dismiss()
        except Exception:
            print('dialog dismiss failed ')

    def create_category(self, obj=None):
        if self.text_field.text.strip() == '':
            self.text_field.hint_text = 'Plese enter a category name!'
        else:
            notebook.create_category(category_name=self.text_field.text)
            self.set_categories_list()
            self.close_dialog()

    def set_categories_list(self):
        self.categories_list.clear_widgets()
        for category_name in notebook.get_categories_list():
            self.categories_list.add_widget(CategoryItem(category_name))

    def __init__(self, **kwargs):
        super(CategoriesListScreen, self).__init__(**kwargs)


class TaskCreationScreen(MDScreen):
    button_task_creation = ObjectProperty()
    textfield_task_name = ObjectProperty()
    textfield_task_description = ObjectProperty()

    def create_task(self, category):
        task_name = self.textfield_task_name.text
        task_description = self.textfield_task_description.text
        notebook.add_task(Task(name=task_name, description=task_description, category=category))

        self.textfield_task_name.set_text(self, text='')
        self.textfield_task_description.set_text(self, text='')
        self.button_task_creation.disabled = True
        notebook.show_notebook()

    def __init__(self, **kwargs):
        super(TaskCreationScreen, self).__init__(**kwargs)


class TaskItem(TwoLineIconListItem):
    checkbox = ObjectProperty()

    def checkbox_action(self):
        checkbox_state = self.checkbox.state
        if checkbox_state == 'down':
            notebook.mark_task_done(self.text)
        else:
            notebook.mark_task_undone(self.text)

    def __init__(self, task_name, task_description, task_is_done, **kwargs):
        super(TaskItem, self).__init__(**kwargs)
        self.text = task_name
        self.secondary_text = task_description
        self.checkbox.state = 'normal' if task_is_done is False else 'down'


class TasksInCategoryScreen(MDScreen):
    task_list = ObjectProperty()
    toolbar = ObjectProperty()

    def set_tasks_list(self, category):
        self.toolbar.title= category
        self.task_list.clear_widgets()

        for task_item in notebook.get_tasks_from_category(category):
        #  for task_item in notebook.get_tasks():
            self.task_list.add_widget(TaskItem(task_name=task_item.get_name(),
                                               task_description=task_item.get_description(),
                                               task_is_done=task_item.is_done()))
        notebook.show_notebook()

    def __init__(self, **kwargs):
        super(TasksInCategoryScreen, self).__init__(**kwargs)


class TaskOnlyScreen(MDScreen):
    task_name = ObjectProperty()
    task_description = ObjectProperty()
    task_is_done = ObjectProperty()
    task_category = ObjectProperty()

    def set_name(self):
        new_task_name = self.task_name.text
        if new_task_name != self.task_name_history:
            notebook.set_task_name(self.task_name_history, new_task_name)
            self.task_name_history = new_task_name

    def set_description(self):
        new_task_description = self.task_description.text
        notebook.set_task_description(self.task_name_history, new_task_description)

    def set_is_done(self):
        is_done = self.task_is_done.active
        if is_done:
            notebook.mark_task_done(self.task_name_history)
        else:
            notebook.mark_task_undone(self.task_name_history)

    # todo - сделать какую-нибудь конечную проверку категории, а не сразу менять? 
    def set_category(self):
        print('set category')
        new_category = self.task_category.text
        notebook.set_task_category(self.task_name_history, new_category)

    def build(self, instance):
        self.task_name_history = instance.text
        task_description = instance.secondary_text
        task_is_done = True if instance.checkbox.state == 'down' else False
        task_category = notebook.get_task_by_name(self.task_name_history).get_category()
        print(notebook.get_task_by_name(self.task_name_history).show_task())
        print("category " + task_category)
        self.task_name.text = self.task_name_history
        self.task_description.text = task_description
        self.task_is_done.active = task_is_done
        self.task_category.text = task_category

    def __init__(self, instance, **kwargs):
        super(TaskOnlyScreen, self).__init__(**kwargs)
        self.task_name_history = ""
        self.build(instance)


class MyApp(MDApp):
    dialog = None

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
            self.set_screen('tasksInCategory')
            self.screen_manager.remove_widget(screen)

    def remove_task(self, instance):
        task_name = instance.task_name.text
        notebook.remove_task_by_name(task_name)
        self.remove_task_only_screen()
        notebook.show_notebook()

    def show_tasks_in_categories_screen(self, category):
        self.current_category = category
        self.set_screen('tasksInCategory')
        print(self.current_category)

    def on_start(self):
        self.categoriesListScreen.set_categories_list()
        #self.tasksInCategoryScreen.set_tasks_list(self.current_category)

    def on_stop(self):
        notebook.write_tasks_in_file()

    def __init__(self, **kwargs):
        self.screen_manager = None
        self.categoriesListScreen = None
        self.tasksInCategoryScreen = None
        self.taskCreationScreen = None
        self.current_category = 'Base'
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        notebook.read_tasks_from_file()
        self.title = "Task list"
        self.screen_manager = MainApp()
        self.categoriesListScreen = self.screen_manager.get_screen('categoriesList')
        self.tasksInCategoryScreen = self.screen_manager.get_screen('tasksInCategory')
        self.taskCreationScreen = self.screen_manager.get_screen('taskCreation')

        return self.screen_manager


if __name__ == "__main__":
    MyApp().run()
