from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.widget import WidgetException
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen


class TaskOnlyScreen(MDScreen):
    task_name = ObjectProperty()
    task_description = ObjectProperty()
    task_category = ObjectProperty()
    toolbar = ObjectProperty()
    edited = False

    objApp = None

    def allow_task_editing(self):
        if not self.edited:
            self.edited = True
            self.toolbar.right_action_items = [['close', lambda x: self.cancel_changes()]]

    def edit_task(self):
        self.toolbar.right_action_items = []
        self.set_name()
        self.set_description()
        self.set_category()
        self.edited = False

    def cancel_changes(self):
        self.objApp = MDApp.get_running_app()
        self.toolbar.right_action_items = []
        task = self.objApp.get_task_by_id(self.task_id)
        self.task_name.text = task.get_name()
        self.task_description.text = task.get_description()
        self.task_category.text = task.get_category()
        self.edited = False

    def set_name(self):
        self.objApp = MDApp.get_running_app()
        new_task_name = self.task_name.text.strip()
        old_task_name = self.objApp.get_task_by_id(id_of_required_task=self.task_id).get_name()
        if new_task_name != old_task_name:
            self.objApp.set_task_name(id_of_required_task=self.task_id,
                                      new_name=new_task_name)
            self.objApp.write_tasks_in_file(self.objApp.path_to_data)
            self.toolbar.title = new_task_name

    def set_description(self):
        self.objApp = MDApp.get_running_app()
        new_task_description = self.task_description.text.strip()
        old_task_description = self.objApp.get_task_by_id(id_of_required_task=self.task_id).get_description()
        if new_task_description != old_task_description:
            self.objApp.set_task_description(id_of_required_task=self.task_id,
                                             new_description=new_task_description)
            self.objApp.write_tasks_in_file(self.objApp.path_to_data)

    def set_is_done(self):
        self.objApp = MDApp.get_running_app()
        is_done = self.task_is_done.active
        if is_done:
            self.objApp.mark_task_done(id_of_required_task=self.task_id)
        else:
            self.objApp.mark_task_undone(id_of_required_task=self.task_id)
        self.objApp.write_tasks_in_file(self.objApp.path_to_data)

    def set_category(self):
        self.objApp = MDApp.get_running_app()
        new_category = self.task_category.text
        old_category = self.objApp.get_task_by_id(self.task_id).get_category()

        if new_category != old_category:
            self.objApp.set_task_category(id_of_required_task=self.task_id,
                                          new_category=new_category)
            self.objApp.write_tasks_in_file(self.objApp.path_to_data)

    def show_category_menu(self):
        self.allow_task_editing()
        try:
            self.category_menu.open()
        except WidgetException:
            print('Menu is already open')
        finally:
            pass

    def build(self, instance):
        self.objApp = MDApp.get_running_app()
        self.task_id = instance.task_id
        # task_is_done = True if instance.checkbox.state == 'down' else False
        task_name = instance.text
        task_description = instance.secondary_text
        task_category = self.objApp.get_task_by_id(self.task_id).get_category()
        self.toolbar.title = task_name
        self.task_name.text = task_name
        self.task_description.text = task_description
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
            } for category_name in self.objApp.get_categories_list()
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
