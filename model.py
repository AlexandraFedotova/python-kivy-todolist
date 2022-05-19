import json


class Task:
    def __init__(self, name, description, is_done=False):
        self.__name = name
        self.__description = description
        self.__is_done = is_done

    def get_name(self):
        return str(self.__name)

    def set_name(self, new_name):
        self.__name = new_name

    def get_description(self):
        return self.__description

    def set_description(self, new_description):
        self.__description = new_description

    def is_done(self):
        return self.__is_done

    def mark_done(self):
        self.__is_done = True

    def mark_undone(self):
        self.__is_done = False

    def show_task(self):
        description = "Task name: " + self.__name + ", is done: " + str(self.__is_done) + \
                      ", task description: " + self.__description
        return description

    def get_task_data(self):
        data_task = {
            "name": self.__name,
            "description": self.__description,
            "is_done": self.__is_done,
        }
        return data_task


class Notebook:
    def __init__(self):
        self.__tasks = []

    def is_task(self, task):
        result = False
        if type(task) is Task:
            result = True
        return result

    def add_task(self, task):
        if self.is_task(task):
            self.__tasks.append(task)

    def get_task_by_name(self, name_of_required_task):
        for task in self.__tasks:
            task_name = task.get_name()
            if task_name == name_of_required_task:
                return task
        return None

    def remove_task_by_name(self, name_of_required_task):
        task = self.get_task_by_name(name_of_required_task)
        if self.is_task(task):
            self.__tasks.remove(task)

    def get_tasks(self):
        return self.__tasks

    def mark_task_done(self, name_of_required_task):
        task = self.get_task_by_name(name_of_required_task)
        if self.is_task(task):
            task.mark_done()

    def mark_task_undone(self, name_of_required_task):
        task = self.get_task_by_name(name_of_required_task)
        if self.is_task(task):
           task.mark_undone()

    def set_task_description(self, name_of_required_task, new_description):
        task = self.get_task_by_name(name_of_required_task)
        if self.is_task(task):
            task.set_description(new_description)

    def set_task_name(self, name_of_required_task, new_name):
        task = self.get_task_by_name(name_of_required_task)
        if self.is_task(task):
            task.set_name(new_name)

    # добавить обработку ошибок
    def write_tasks_in_file(self, filename='tasks.txt'):
        data = []
        for task in self.__tasks:
            data.append(task.get_task_data())

        file = open(filename, mode='w', encoding='utf-8')
        json.dump(data, file)
        file.close()
        return True

    # Добавить обработку ошибок
    def read_tasks_from_file(self, filename='tasks.txt'):
        file = open(filename, mode='r', encoding='utf-8')
        data = json.load(file)
        file.close()

        for task_info in data:
            task_name = task_info.get('name')
            task_description = task_info.get('description')
            task_is_done = task_info.get('is_done')
            self.add_task(Task(name=task_name, description=task_description, is_done=task_is_done))
        return True


if __name__ == "__main__":
    notebook = Notebook()

    for i in range(0, 10):
        notebook.add_task(Task(name='Task {number}'.format(number=i),
                               description='It`s {number} task.'.format(number=i)))
    tasks = notebook.get_tasks()

    for task in tasks:
        print(task.show_task())

    notebook.write_tasks_in_file()
