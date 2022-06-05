from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from model import Task


class TaskItem(TwoLineAvatarIconListItem):
    checkbox = ObjectProperty()

    def __init__(self, task_id, task_name, task_description, task_is_done, **kwargs):
        super(TaskItem, self).__init__(**kwargs)
        self.task_id = task_id
        self.text = task_name
        self.secondary_text = task_description
        self.checkbox.state = 'normal' if task_is_done is False else 'down'


class TasksInCategoryScreen(MDScreen):
    task_list = ObjectProperty()
    toolbar = ObjectProperty()
    objApp = None

    dialog = None

    def close_dialog(self, obj=None):
        try:
            self.dialog.dismiss()
        except Exception:
             ('dialog dismiss failed')

    def rename_category(self, obj=None):
        self.objApp = MDApp.get_running_app()
        current_category_name = self.category
        new_category_name = self.text_field.text
        self.objApp.rename_category(name_of_required_category=current_category_name,
                                             new_category_name=new_category_name)
        self.objApp.write_tasks_in_file(self.objApp.path_to_data)
        self.toolbar.title = new_category_name
        self.close_dialog()

    def create_task(self, obj=None):
        self.objApp = MDApp.get_running_app()
        if self.text_field_name.text.strip() == '':
            self.text_field_name.hint_text = 'Введите название задачи'
        else:
            new_task = Task(name=self.text_field_name.text, description=self.text_field_description.text,
                            category=self.category)
            self.objApp.add_task(new_task)
            self.objApp.write_tasks_in_file(self.objApp.path_to_data)
            self.set_tasks_list(self.category)
            self.text_field_name.text = ''
            self.text_field_description.text = ''

    def delete_task(self, obj=None):
        self.objApp = MDApp.get_running_app()
        try:
            self.objApp.remove_task_by_id(id_of_required_task=self.id_task_for_deleting)
            self.objApp.write_tasks_in_file(self.objApp.path_to_data)
            self.set_tasks_list(category=self.category)
            self.close_dialog()
        except Exception:
            print('Error with deleting task')

    def set_task_state(self, instance):
        self.objApp = MDApp.get_running_app()
        checkbox_state = instance.checkbox.state
        task_id = instance.task_id
        if checkbox_state == 'down':
            self.objApp.mark_task_done(task_id)
        else:
            self.objApp.mark_task_undone(task_id)
        self.objApp.write_tasks_in_file(self.objApp.path_to_data)
        self.set_tasks_list(self.category)

    def show_rename_category_dialog(self, obj=None):
        close_button = MDFlatButton(text='Отмена', on_release=self.close_dialog)
        rename_button = MDFlatButton(text='Переименовать', on_release=self.rename_category)
        content = MDBoxLayout(orientation='vertical', size_hint_y=None, height='50sp')
        self.text_field = MDTextField(hint_text='Новое название категории')
        content.add_widget(self.text_field)
        self.dialog = MDDialog(
            title='Переименовать категорию',
            type="custom",
            content_cls=content,
            buttons=[close_button, rename_button],
        )
        self.dialog.open()

    def show_create_task_dialog(self, obj=None):
        close_button = MDFlatButton(text='Отмена', on_release=self.close_dialog)
        self.create_button = MDFlatButton(text='Создать', on_release=self.create_task)
        content = MDBoxLayout(orientation='vertical', size_hint_y=None, height='150sp')
        self.text_field_name = MDTextField(hint_text='Имя задачи', write_tab=False)
        self.text_field_description = MDTextField(hint_text='Описание задачи', multiline=True)
        self.text_field_description.max_height = self.text_field_description.minimum_height*3.5
        content.add_widget(self.text_field_name)
        content.add_widget(self.text_field_description)
        self.dialog = MDDialog(
            title='Создание задачи',
            type="custom",
            content_cls=content,
            buttons=[close_button, self.create_button],
        )
        self.dialog.open()

    def show_delete_task_dialog(self, instance):
        self.id_task_for_deleting = instance.task_id
        close_button = MDFlatButton(text='Отмена', on_release=self.close_dialog)
        remove_button = MDFlatButton(text='Удалить', on_release=self.delete_task)
        self.dialog = MDDialog(
            title='Удалить задачу?',
            text=instance.text,
            buttons=[close_button, remove_button]
        )
        self.dialog.open()
        pass

    def set_tasks_list(self, category):
        self.objApp = MDApp.get_running_app()
        self.category = category
        self.toolbar.title = category
        self.task_list.clear_widgets()

        for task_item in self.objApp.get_tasks_from_category(category):
            # task_item - task id
            task = self.objApp.get_task_by_id(id_of_required_task=task_item)
            self.task_list.add_widget(TaskItem(task_id=task_item,
                                               task_name=task.get_name(),
                                               task_description=task.get_description(),
                                               task_is_done=task.is_done()))

    def __init__(self, **kwargs):
        super(TasksInCategoryScreen, self).__init__(**kwargs)
        self.category = ''