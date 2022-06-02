from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineRightIconListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


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
            if self.text_field.text.strip() in objApp.notebook.get_categories_list():
                self.text_field.hint_text = 'Такая категория уже есть!'
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
        close_button = MDFlatButton(text='Отмена', on_release=self.close_dialog)
        create_button = MDFlatButton(text='Создать', on_release=self.create_category)
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

        close_button = MDFlatButton(text='Отмена', on_release=self.close_dialog)
        remove_button = MDFlatButton(text='Удалить', on_release=self.delete_category)

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