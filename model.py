import datetime
import json


class Task:
    # todo: add descriptions
    def __init__(self, name, description, is_done=False, category='Base'):
        self.__name = str(name).strip()
        self.__description = str(description).strip()
        self.__is_done = is_done if type(is_done) is bool else False
        self.__category = str(category).strip()

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
        description = "Task name: " + self.__name + ", is done: " + str(self.__is_done) + \
                      ", task description: " + self.__description + ", task category: " + \
                      self.__category
        return description

    def get_task_data(self):
        data_task = {
            "name": self.__name,
            "description": self.__description,
            "is_done": self.__is_done,
            "category": self.__category
        }
        return data_task


class Notebook:
    # todo: add descriptions
    # todo: check types
    # todo: add - str(something).strip() to every important property
    def __init__(self):
        self.__tasks = {}
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
            self.__categories_names.append(category_name)
            self.__tasks_ids_in_categories[category_name] = []

    def get_categories_list(self):
        return self.__categories_names

    def get_tasks_from_category(self, name_of_required_category):
        # todo: add tasks sorting
        name_of_required_category = str(name_of_required_category).strip()
        tasks = {}
        tasks_done = {}
        if name_of_required_category in self.__categories_names:
            for task_id in self.__tasks_ids_in_categories[name_of_required_category]:
                task = self.get_task_by_id(task_id)
                if self.is_task(task):
                    if task.is_done() is True:
                        tasks_done[task_id] = task
                    else:
                        tasks[task_id] = task
        tasks.update(tasks_done)
        return tasks  # dict

    def set_task_category(self, id_of_required_task, name_of_required_category):
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

    def rename_category(self, name_of_required_category, new_category_name):
        name_of_required_category = str(name_of_required_category).strip()
        new_category_name = str(new_category_name).strip()

        tasks = self.get_tasks_from_category(name_of_required_category)  # dict
        for task in tasks:
            self.set_task_category(task, new_category_name)

        self.__tasks_ids_in_categories.pop(name_of_required_category)
        self.__categories_names.remove(name_of_required_category)
        if new_category_name not in self.__categories_names:
            self.__categories_names.append(new_category_name)
            self.__tasks_ids_in_categories[new_category_name] = []

    def remove_category(self, name_of_required_category, name_of_category_to_transfer_tasks_from_deleted=None):
        name_of_required_category = str(name_of_required_category).strip()
        name_of_category_to_transfer_tasks_from_deleted = str(name_of_category_to_transfer_tasks_from_deleted).strip()

        tasks = self.get_tasks_from_category(name_of_required_category)
        if name_of_category_to_transfer_tasks_from_deleted == 'None':
            for task in tasks:
                self.remove_task_by_id(task)
        else:
            for task in tasks:
                self.set_task_category(task, name_of_category_to_transfer_tasks_from_deleted)
        self.__categories_names.remove(name_of_required_category)
        self.__tasks_ids_in_categories.pop(name_of_required_category)

    def add_task(self, task, task_id=None):
        if self.is_task(task):
            if task_id is None:
                task_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            self.__tasks[task_id] = task
            task_category = task.get_category()
            self.create_category(task_category)
            self.__tasks_ids_in_categories[task_category].append(task_id)

    def get_task_by_id(self, id_of_required_task):
        id_of_required_task = str(id_of_required_task).strip()
        task = self.__tasks.get(id_of_required_task)
        return task

    def remove_task_by_id(self, id_of_required_task):
        id_of_required_task = str(id_of_required_task).strip()
        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
            task_category = task.get_category()
            self.__tasks.pop(id_of_required_task)
            self.__tasks_ids_in_categories[task_category].remove(id_of_required_task)

    def get_tasks(self):
        return self.__tasks

    def get_tasks_array(self):
        return self.__tasks.values()

    def mark_task_done(self, id_of_required_task):
        id_of_required_task = str(id_of_required_task).strip()
        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
            task.mark_done()

    def mark_task_undone(self, id_of_required_task):
        id_of_required_task = str(id_of_required_task).strip()
        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
            task.mark_undone()

    def set_task_name(self, id_of_required_task, new_name):
        id_of_required_task = str(id_of_required_task).strip()
        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
            task.set_name(new_name)

    def set_task_description(self, id_of_required_task, new_description):
        id_of_required_task = str(id_of_required_task).strip()
        task = self.get_task_by_id(id_of_required_task)
        if self.is_task(task):
            task.set_description(new_description)

    # todo: add error handling
    # todo? add writing category list, for opportunity of existing empty category
    def write_tasks_in_file(self, filename='tasks.txt'):
        data = {"categories_names": self.__categories_names, "tasks_ids_in_categories": self.__tasks_ids_in_categories}

        data_tasks = {}
        for task_id in self.__tasks:
            task = self.get_task_by_id(task_id)
            data_tasks[task_id] = task.get_task_data()
        data["tasks"] = data_tasks

        file = open(filename, mode='w', encoding='utf-8')
        json.dump(data, file)
        file.close()
        return True

    def show_notebook(self):
        print('-------------------begin of notebook--------------')
        print('categories names: ' + str(self.__categories_names))
        print('ids in cats: ' + str(self.__tasks_ids_in_categories))
        counter = 0
        for category in self.__categories_names:
            print('-------------' + category + '------------------')
            tasks = self.get_tasks_from_category(category).values()
            counter += len(tasks)
            for task in tasks:
                print(task.show_task())
        print("\ncount of tasks in notebook: " + str(len(self.__tasks)) +
              "\ncounter: " + str(counter))
        print("-------------------end of notebook----------------")

    # todo: Add error handling
    # todo? add reading category list, for opportunity of existing empty category
    def read_tasks_from_file(self, filename='tasks.txt'):
        try:
            file = open(filename, mode='r', encoding='utf-8')
            data = json.load(file)
            file.close()
        except Exception:
            print("Error with tasks reading")
            return False

        if data == "":
            return True

        categories_names = data.get('categories_names')
        tasks_ids_in_categories = data.get('tasks_ids_in_categories')

        tasks_info = data.get('tasks')

        for task_id in tasks_info:
            task_id = task_id
            task_info = tasks_info[task_id]
            task_name = task_info.get('name')
            task_description = task_info.get('description')
            task_is_done = task_info.get('is_done')
            task_category = task_info.get('category')
            task = Task(name=task_name, description=task_description, is_done=task_is_done, category=task_category)
            self.add_task(task, task_id)

        if self.__categories_names != categories_names:
            for category_name in categories_names:
                self.create_category(category_name)
            for category_name in self.__categories_names:
                if category_name not in categories_names:
                    print("We have a big Error ")

        return True


if __name__ == "__main__":
    notebook = Notebook()
