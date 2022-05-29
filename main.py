from kivy.metrics import dp
from kivy.uix.widget import WidgetException
from kivymd.app import MDApp
from model import *
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineRightIconListItem, OneLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu


class MainApp(ScreenManager):
    pass


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None
    check = ObjectProperty()

    def set_icon(self):
        self.check.active = True
        check_list = self.check.get_widgets(self.check.group)
        for item in check_list:
            if item != self.check:
                item.active = False

    def __init__(self, text, **kwargs):
        super(ItemConfirm, self).__init__(**kwargs)
        self.text = text


class CategoryItem(OneLineRightIconListItem):
    def __init__(self, category_name, **kwargs):
        super(CategoryItem, self).__init__(**kwargs)
        self.text = category_name


class CategoriesListScreen(MDScreen):
    categories_list = ObjectProperty()
    dialog = None
    objApp = None

    def close_dialog(self, obj=None):
        try:
            self.dialog.dismiss()
        except Exception:
            print('dialog dismiss failed')

    def create_category(self, obj=None):
        objApp = MDApp.get_running_app()
        if self.text_field.text.strip() == '':
            self.text_field.hint_text = 'Ведите название категории!'
        else:
            self.objApp.notebook.create_category(category_name=self.text_field.text)
            self.objApp.notebook.write_tasks_in_file(self.objApp.path_to_data)
            self.set_categories_list()
            self.close_dialog()

    def delete_category(self, obj=None):
        objApp = MDApp.get_running_app()
        category_for_transfer_tasks_from_deleted_category = ''
        for item in self.items:
            if item.check.active is True:
                category_for_transfer_tasks_from_deleted_category = item.text
        if category_for_transfer_tasks_from_deleted_category == "Без переноса задач":
            category_for_transfer_tasks_from_deleted_category = None
        try:
            self.objApp.notebook.remove_category(name_of_required_category=self.category_for_deleting,
                                     name_of_category_to_transfer_tasks_from_deleted=category_for_transfer_tasks_from_deleted_category)
            self.objApp.notebook.write_tasks_in_file(self.objApp.path_to_data)
            self.set_categories_list()
            self.close_dialog()
        except Exception:
            print('Error with deleting category')

    def show_dialog_create_category(self):
        close_button = MDFlatButton(text='Закрыть окно', on_release=self.close_dialog)
        create_button = MDFlatButton(text='Создать категорию', on_release=self.create_category)
        content = MDBoxLayout(orientation='vertical', size_hint_y=None, height='50sp')
        self.text_field = MDTextField(hint_text='Название категории')
        content.add_widget(self.text_field)
        self.dialog = MDDialog(
            title='Создание категории',
            type="custom",
            content_cls=content,
            buttons=[close_button, create_button],
        )
        self.dialog.open()

    def show_dialog_delete_category(self, instance):
        self.objApp = MDApp.get_running_app()
        self.category_for_deleting = instance.text
        self.items = [ItemConfirm(text='Без переноса задач')]
        for category_name in self.objApp.notebook.get_categories_list():
            if category_name != self.category_for_deleting:
                self.items.append(ItemConfirm(text=category_name))
        self.items[0].set_icon()

        close_button = MDFlatButton(text='Закрыть окно', on_release=self.close_dialog)
        remove_button = MDFlatButton(text='Удалить категорию', on_release=self.delete_category)

        self.dialog = MDDialog(
            title='Удалить категорию "{name}"?'.format(name=instance.text),
            type="confirmation",
            items=self.items,
            buttons=[close_button, remove_button]
        )
        self.dialog.open()

    def set_categories_list(self):
        self.objApp = MDApp.get_running_app()
        self.categories_list.clear_widgets()
        for category_name in self.objApp.notebook.get_categories_list():
            self.categories_list.add_widget(CategoryItem(category_name))

    def __init__(self, **kwargs):
        super(CategoriesListScreen, self).__init__(**kwargs)


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
            print('dialog dismiss failed')

    def rename_category(self, obj=None):
        self.objApp = MDApp.get_running_app()
        current_category_name = self.category
        new_category_name = self.text_field.text
        self.objApp.notebook.rename_category(name_of_required_category=current_category_name,
                                 new_category_name=new_category_name)
        self.objApp.notebook.write_tasks_in_file(self.objApp.path_to_data)
        self.toolbar.title = new_category_name
        self.close_dialog()

    def create_task(self, obj=None):
        self.objApp = MDApp.get_running_app()
        if self.text_field_name.text.strip() == '':
            self.text_field_name.hint_text = 'Введите название задачи'
        else:
            new_task = Task(name=self.text_field_name.text, description=self.text_field_description.text,
                            category=self.category)
            self.objApp.notebook.add_task(new_task)
            self.objApp.notebook.write_tasks_in_file(self.objApp.path_to_data)
            self.set_tasks_list(self.category)
            self.text_field_name.text = ''
            self.text_field_description.text = ''

    def delete_task(self, obj=None):
        self.objApp = MDApp.get_running_app()
        try:
            self.objApp.notebook.remove_task_by_id(id_of_required_task=self.id_task_for_deleting)
            self.objApp.notebook.write_tasks_in_file(self.objApp.path_to_data)
            self.set_tasks_list(category=self.category)
            self.close_dialog()
        except Exception:
            print('Error with deleting task')

    def set_task_state(self, instance):
        self.objApp = MDApp.get_running_app()
        checkbox_state = instance.checkbox.state
        task_id = instance.task_id
        if checkbox_state == 'down':
            self.objApp.notebook.mark_task_done(task_id)
        else:
            self.objApp.notebook.mark_task_undone(task_id)
        self.objApp.notebook.write_tasks_in_file(self.objApp.path_to_data)
        self.set_tasks_list(self.category)

    def show_rename_category_dialog(self, obj=None):
        close_button = MDFlatButton(text='Закрыть окно', on_release=self.close_dialog)
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
        close_button = MDFlatButton(text='Закрыть окно', on_release=self.close_dialog)
        self.create_button = MDFlatButton(text='Создать', on_release=self.create_task)
        content = MDBoxLayout(orientation='vertical', size_hint_y=None, height='150sp')
        self.text_field_name = MDTextField(hint_text='Имя задачи', write_tab=False)
        self.text_field_description = MDTextField(hint_text='Описание задачи', multiline=True, max_height='100sp')
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
        close_button = MDFlatButton(text='Закрыть окно', on_release=self.close_dialog)
        remove_button = MDFlatButton(text='Удалить задачу', on_release=self.delete_task)
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

        for task_item in self.objApp.notebook.get_tasks_from_category(category):
            # task_item - task id
            task = self.objApp.notebook.get_task_by_id(id_of_required_task=task_item)
            self.task_list.add_widget(TaskItem(task_id=task_item,
                                               task_name=task.get_name(),
                                               task_description=task.get_description(),
                                               task_is_done=task.is_done()))

    def __init__(self, **kwargs):
        super(TasksInCategoryScreen, self).__init__(**kwargs)
        self.category = ''


class TaskOnlyScreen(MDScreen):
    task_name = ObjectProperty()
    task_description = ObjectProperty()
    task_is_done = ObjectProperty()
    task_category = ObjectProperty()
    toolbar = ObjectProperty()

    objApp = None

    def allow_task_editing(self):
        self.toolbar.right_action_items = [['close', lambda x: self.cancel_changes()],['check', lambda x: self.edit_task()]]
        self.task_name.disabled = False
        self.task_description.disabled = False
        self.task_category.disabled = False

    def edit_task(self):
        self.toolbar.right_action_items = [["pencil-outline", lambda x: self.allow_task_editing()]]
        self.task_name.disabled = True
        self.task_description.disabled = True
        self.task_category.disabled = True
        self.set_name()
        self.set_description()
        self.set_category()

    def cancel_changes(self):
        self.objApp = MDApp.get_running_app()
        self.toolbar.right_action_items = [["pencil-outline", lambda x: self.allow_task_editing()]]
        self.task_name.disabled = True
        self.task_description.disabled = True
        self.task_category.disabled = True
        task = self.objApp.notebook.get_task_by_id(self.task_id)
        self.task_name.text = task.get_name()
        self.task_description.text = task.get_description()
        self.task_category.text = task.get_category()

    def set_name(self):
        self.objApp = MDApp.get_running_app()
        new_task_name = self.task_name.text.strip()
        old_task_name = self.objApp.notebook.get_task_by_id(id_of_required_task=self.task_id).get_name()
        if new_task_name != old_task_name:
            self.objApp.notebook.set_task_name(id_of_required_task=self.task_id,
                                   new_name=new_task_name)
            self.objApp.notebook.write_tasks_in_file(self.objApp.path_to_data)
            self.toolbar.title = new_task_name

    def set_description(self):
        self.objApp = MDApp.get_running_app()
        new_task_description = self.task_description.text.strip()
        old_task_description = self.objApp.notebook.get_task_by_id(id_of_required_task=self.task_id).get_description()
        if new_task_description != old_task_description:
            self.objApp.notebook.set_task_description(id_of_required_task=self.task_id,
                                          new_description=new_task_description)
            self.objApp.notebook.write_tasks_in_file(self.objApp.path_to_data)

    def set_is_done(self):
        self.objApp = MDApp.get_running_app()
        is_done = self.task_is_done.active
        if is_done:
            self.objApp.notebook.mark_task_done(id_of_required_task=self.task_id)
        else:
            self.objApp.notebook.mark_task_undone(id_of_required_task=self.task_id)
        self.objApp.notebook.write_tasks_in_file(self.objApp.path_to_data)

    def set_category(self):
        self.objApp = MDApp.get_running_app()
        new_category = self.task_category.text
        old_category = self.objApp.notebook.get_task_by_id(self.task_id).get_category()

        if new_category != old_category:
            self.objApp.notebook.set_task_category(id_of_required_task=self.task_id,
                                       name_of_required_category=new_category)
            self.objApp.notebook.write_tasks_in_file(self.objApp.path_to_data)

    def show_category_menu(self):
        try:
            self.category_menu.open()
        except WidgetException:
            print('Menu is already open')
        finally:
            pass

    def build(self, instance):
        self.objApp = MDApp.get_running_app()
        self.task_id = instance.task_id
        task_name = instance.text
        task_description = instance.secondary_text
        task_is_done = True if instance.checkbox.state == 'down' else False
        task_category = self.objApp.notebook.get_task_by_id(self.task_id).get_category()
        self.toolbar.title = task_name
        self.task_name.text = task_name
        self.task_description.text = task_description
        self.task_is_done.active = task_is_done
        self.task_category.text = task_category

    def __init__(self, instance, **kwargs):
        super(TaskOnlyScreen, self).__init__(**kwargs)
        self.objApp = MDApp.get_running_app()
        self.task_id = ''
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": category_name,
                "height": dp(50),
                "on_release": lambda x=category_name: self.set_item(x)
            } for category_name in self.objApp.notebook.get_categories_list()
        ]
        self.category_menu = MDDropdownMenu(
            caller=self.task_category,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.build(instance)

    def set_item(self, text_item):
        self.task_category.text = text_item
        try:
            self.category_menu.dismiss()
        except Exception:
            print('menu is already dismissed')


class MyApp(MDApp):
    dialog = None
    notebook = None

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

    def show_tasks_in_categories_screen(self, category):
        self.current_category = category
        self.set_screen('tasksInCategory')

    def on_start(self):
        self.categoriesListScreen.set_categories_list()

    def on_stop(self):
        self.notebook.write_tasks_in_file(self.path_to_data)

    def __init__(self, **kwargs):
        self.screen_manager = None
        self.categoriesListScreen = None
        self.tasksInCategoryScreen = None
        self.current_category = 'Base'
        self.path_to_data = 'data/tasks.txt'
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        self.notebook = Notebook()
        self.notebook.read_tasks_from_file(self.path_to_data)
        self.title = "Task list"
        self.screen_manager = MainApp()
        self.categoriesListScreen = self.screen_manager.get_screen('categoriesList')
        self.tasksInCategoryScreen = self.screen_manager.get_screen('tasksInCategory')


        return self.screen_manager


if __name__ == "__main__":
    MyApp().run()
