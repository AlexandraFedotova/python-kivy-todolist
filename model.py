import datetime
import json
import time


class Task:
    # todo: add descriptions
    def __init__(self, name, description, is_done=False, category='Base'):
        self.__id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.__name = str(name).strip()
        self.__description = str(description).strip()
        self.__is_done = is_done if type(is_done) is bool else False
        self.__category = str(category).strip()

    def get_id(self):
        return self.__id

    def set_id(self, new_id):
        self.__id = str(new_id).strip()

    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        self.__name = str(new_name).strip()

    def get_description(self):
        return self.__description

    def set_description(self, new_description):
        self.__description = str(new_description).strip()

    def is_done(self):
        return self.__is_done

    def mark_done(self):
        self.__is_done = True

    def mark_undone(self):
        self.__is_done = False

    def get_category(self):
        return self.__category

    def set_category(self, new_category):
        self.__category = str(new_category).strip()

    def show_task(self):
        description = "Task id: " + self.__id + ", task name: " + self.__name + ", is done: " + str(self.__is_done) + \
                      ", task description: " + self.__description + ", task category: " + \
                        self.__category
        return description

    def get_task_data(self):
        data_task = {
            "id"         : self.__id,
            "name"       : self.__name,
            "description": self.__description,
            "is_done"    : self.__is_done,
            "category"   : self.__category
        }
        return data_task


class Notebook:
    # todo: add descriptions
    # todo: check types
    # todo: add - str(something).strip() to every important property
    def __init__(self):
        self.__tasks = []
        self.__categories_names = []
        self.__tasks_ids_in_categories = {}

    def is_task(self, obj):
        result = False
        if type(obj) is Task:
            result = True
        return result

    def create_category(self, category_name):
        category_name = str(category_name).strip()
        if category_name not in self.__categories_names and not "":
            print('category creation: ' + category_name)
            self.__categories_names.append(category_name)
            self.__tasks_ids_in_categories[category_name] = []
        print(self.__categories_names)

    def get_categories_list(self):
        return self.__categories_names

    def get_tasks_from_category(self, name_of_required_category):
        print("-----------------------------------")
        print('get tasks from category')
        # todo: add tasks sorting
        tasks = []
        name_of_required_category = str(name_of_required_category).strip()
        print('name of required category ' + name_of_required_category)
        if name_of_required_category in self.__categories_names:
            print(self.__tasks_ids_in_categories[name_of_required_category])
            for task_id in self.__tasks_ids_in_categories[name_of_required_category]:
                print(task_id)
                task = self.get_task_by_id(task_id)
                if self.is_task(task):
                    tasks.append(task)
        print("==============================")
        return tasks

    def set_task_category(self, id_of_required_task, name_of_required_category):
        print("-----------------------------------")
        print('set_task_category')
        name_of_required_category = str(name_of_required_category).strip()
        id_of_required_task = str(id_of_required_task).strip()

        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
            old_category = task.get_category()
            if old_category == name_of_required_category:
                return
            task.set_category(name_of_required_category)
            self.__tasks_ids_in_categories[old_category].remove(id_of_required_task)
            self.create_category(name_of_required_category)
            self.__tasks_ids_in_categories[name_of_required_category].append(id_of_required_task)
        print("\nSet task " + id_of_required_task + " with name " + task.get_name() + " to category " + name_of_required_category)
        print(self.__categories_names)
        print(self.__tasks_ids_in_categories)
        print("==============================")

    def rename_category(self, name_of_required_category, new_category_name):
        name_of_required_category = str(name_of_required_category).strip()

        tasks = self.get_tasks_from_category(name_of_required_category)
        for task in tasks:
            self.set_task_category(task.get_id(), new_category_name)

        self.__tasks_ids_in_categories.pop(name_of_required_category)
        self.__categories_names.remove(name_of_required_category)
        if new_category_name not in self.__categories_names:
            self.__categories_names.append(new_category_name)
            self.__tasks_ids_in_categories[new_category_name] = []

    def remove_category(self, name_of_required_category, name_of_category_to_transfer_tasks_from_deleted=None):
        name_of_required_category = str(name_of_required_category).strip()
        name_of_category_to_transfer_tasks_from_deleted = str(name_of_category_to_transfer_tasks_from_deleted).strip()

        self.__categories_names.remove(name_of_required_category)
        self.__tasks_ids_in_categories.pop(name_of_required_category)
        tasks = self.get_tasks_from_category(name_of_required_category)

        if name_of_category_to_transfer_tasks_from_deleted is None:
            print('name of category to transfer tasks from deleted is None ')
            for task in tasks:
                self.remove_task_by_id(task.get_id())
        else:
            print('name of category to transfer tasks from deleted is ' + name_of_category_to_transfer_tasks_from_deleted)
            for task in tasks:
                self.set_task_category(task.get_id(), name_of_category_to_transfer_tasks_from_deleted)

    def add_task(self, task):
        if self.is_task(task):
            self.__tasks.append(task)
            task_id = task.get_id()
            task_category = task.get_category()
            self.create_category(task_category)
            self.__tasks_ids_in_categories[task_category].append(task_id)

    #def get_task_by_name(self, name_of_required_task):
    #    name_of_required_task = str(name_of_required_task).strip()
    #    for task in self.__tasks:
    #        task_name = task.get_name()
    #        if task_name == name_of_required_task:
    #            return task
    #    return None

    def get_task_by_id(self, id_of_required_task):
        print("----------------------")
        id_of_required_task = str(id_of_required_task).strip()
        print('get task by id ' + id_of_required_task)
        for task in self.__tasks:
            task_id = task.get_id()
            print('task ' + task.get_name() + " task id " + task_id)
            if task_id == id_of_required_task:
                return task
        return None

    def remove_task_by_id(self, id_of_required_task):
        print('Remove task by id: ' + id_of_required_task)

        id_of_required_task = str(id_of_required_task).strip()
        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
            print('Obj is a task ')
            task_id = task.get_id()
            task_category = task.get_category()
            self.__tasks.remove(task)
            self.__tasks_ids_in_categories[task_category].remove(task_id)

    #def remove_task_by_name(self, name_of_required_task):
    #    name_of_required_task = str(name_of_required_task).strip()
    #    task = self.get_task_by_name(name_of_required_task)
    #    if self.is_task(task):
    #        task_name = task.get_name()
    #        task_category = task.get_category()
    #        self.__tasks.remove(task)  # removing task from tasks list
    #        self.__tasks_ids_in_categories[task_category].remove(task_name)  # removing task from list tasks in category
    #        # todo? add checking is task list in this category empty, and maybe delete this category

    def get_tasks(self):
        return self.__tasks

    def mark_task_done(self, id_of_required_task):
        id_of_required_task = str(id_of_required_task).strip()
        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
            task.mark_done()

    #def mark_task_done(self, name_of_required_task):
    #    name_of_required_task = str(name_of_required_task).strip()
    #    task = self.get_task_by_name(name_of_required_task)
    #    if self.is_task(task):
    #        task.mark_done()

    def mark_task_undone(self, id_of_required_task):
        id_of_required_task = str(id_of_required_task).strip()
        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
           task.mark_undone()

    #def mark_task_undone(self, name_of_required_task):
    #    name_of_required_task = str(name_of_required_task).strip()
    #    task = self.get_task_by_name(name_of_required_task)
    #    if self.is_task(task):
    #       task.mark_undone()

    def set_task_name(self, id_of_required_task, new_name):
        id_of_required_task = str(id_of_required_task).strip()
        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
            task.set_name(new_name)

    #def set_task_name(self, name_of_required_task, new_name):
    #    name_of_required_task = str(name_of_required_task).strip()
    #    task = self.get_task_by_name(name_of_required_task)
    #    if self.is_task(task):
    #        task.set_name(new_name)
    #        task_category = task.get_category()
    #        self.__tasks_ids_in_categories[task_category].remove(name_of_required_task)
    #        self.__tasks_ids_in_categories[task_category].append(new_name)

    #def set_task_description(self, name_of_required_task, new_description):
    #    name_of_required_task = str(name_of_required_task).strip()
    #    task = self.get_task_by_name(name_of_required_task)
    #    if self.is_task(task):
    #        task.set_description(new_description)

    def set_task_description(self, id_of_required_task, new_description):
        id_of_required_task = str(id_of_required_task).strip()
        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
            task.set_description(new_description)

    # todo: add error handling
    # todo? add writing category list, for opportunity of existing empty category
    def write_tasks_in_file(self, filename='tasks.txt'):
        data = []
        for task in self.__tasks:
            data.append(task.get_task_data())

        file = open(filename, mode='w', encoding='utf-8')
        json.dump(data, file)
        file.close()
        return True

    # todo: Add error handling
    # todo? add reading category list, for opportunity of existing empty category
    def read_tasks_from_file(self, filename='tasks.txt'):
        file = open(filename, mode='r', encoding='utf-8')
        data = json.load(file)
        file.close()

        if data == "":
            return True

        for task_info in data:
            task_id = task_info.get('id')
            task_name = task_info.get('name')
            task_description = task_info.get('description')
            task_is_done = task_info.get('is_done')
            task_category = task_info.get('category')
            task = Task(name=task_name, description=task_description,
                        is_done=task_is_done, category=task_category)
            task.set_id(task_id)
            self.add_task(task)
        return True

    def show_notebook(self):
        print('-------------------begin of notebook--------------')
        counter = 0
        for category in self.__categories_names:
            print('-------------' + category + '------------------')
            tasks = self.get_tasks_from_category(category)
            counter += len(tasks)
            for task in tasks:
                print(task.show_task())
        print("\ncount of tasks in notebook: " + str(len(self.__tasks)) +
              "\ncounter: " + str(counter))
        print("-------------------end of notebook----------------")


if __name__ == "__main__":
    notebook = Notebook()

    print('-------------------1----------------------')

    for i in range(0, 10):
        notebook.add_task(Task(name='Task {number}'.format(number=str(i)),
                               description='It`s {number} task.'.format(number=str(i))))
        time.sleep(2)

    notebook.create_category('Test')
    test_task_1 = Task(name = 'Test task one', description= 'Tests it is important part of developing', category='  Test ')
    notebook.show_notebook()
