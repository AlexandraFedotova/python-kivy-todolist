from kivymd.app import MDApp
from model import *
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.list import TwoLineIconListItem

from kivy.core.window import Window

Window.size = (350, 622)

notebook = Notebook()


class MainApp(ScreenManager):
    pass


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


class TaskCreationScreen(MDScreen):
    button_task_creation = ObjectProperty()
    textfield_task_name = ObjectProperty()
    textfield_task_description = ObjectProperty()

    def create_task(self):
        task_name = self.textfield_task_name.text
        task_description = self.textfield_task_description.text
        notebook.add_task(Task(name=task_name, description=task_description))

        self.textfield_task_name.set_text(self, text='')
        self.textfield_task_description.set_text(self, text='')
        self.button_task_creation.disabled = True

    def __init__(self, **kwargs):
        super(TaskCreationScreen, self).__init__(**kwargs)


class TaskListScreen(MDScreen):
    task_list = ObjectProperty()

    def set_tasks_list(self):
        self.task_list.clear_widgets()

        for task_item in notebook.get_tasks():
            self.task_list.add_widget(TaskItem(task_name=task_item.get_name(),
                                               task_description=task_item.get_description(),
                                               task_is_done=task_item.is_done()))

    def delete_item(self, instance):
        task_name = instance.task_item.text
        notebook.remove_task_by_name(task_name)
        self.set_tasks_list()

    def __init__(self, **kwargs):
        super(TaskListScreen, self).__init__(**kwargs)


class TaskOnlyScreen(MDScreen):
    task_name = ObjectProperty()
    task_description = ObjectProperty()
    task_is_done = ObjectProperty()

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

    def remove_task(self):
        notebook.remove_task_by_name(self.task_name_history)

    def build(self, instance):
        self.task_name_history = instance.text
        task_description = instance.secondary_text
        task_is_done = True if instance.checkbox.state == 'down' else False
        self.task_name.text = self.task_name_history
        self.task_description.text = task_description
        self.task_is_done.active = task_is_done

    def __init__(self, instance, **kwargs):
        super(TaskOnlyScreen, self).__init__(**kwargs)
        self.task_name_history = ""
        self.build(instance)


class MyApp(MDApp):
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
            self.set_screen('taskList')
            self.screen_manager.remove_widget(screen)

    def remove_task(self, instance):
        task_name = instance.task_name.text
        notebook.remove_task_by_name(task_name)
        self.remove_task_only_screen()

    def on_start(self):
        self.taskListScreen.set_tasks_list()

    def on_stop(self):
        notebook.write_tasks_in_file()

    def __init__(self, **kwargs):
        self.screen_manager = None
        self.taskListScreen = None
        self.taskCreationScreen = None
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        notebook.read_tasks_from_file()
        self.title = "Task list"
        self.screen_manager = MainApp()
        self.taskListScreen = self.screen_manager.get_screen('taskList')
        self.taskCreationScreen = self.screen_manager.get_screen('taskCreation')

        return self.screen_manager


if __name__ == "__main__":
    MyApp().run()
