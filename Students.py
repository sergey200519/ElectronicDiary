from functions import get_homeworks, get_teacher_by_id, table, get_homeworks_from_json, write_homeworks_to_json
from Base import Base

class Student(Base):
    commannds = {
            0: "Посмотреть Д/З",
            1: "Сдать Д/З"
        }

    def view_homework(self):
        homeworks = get_homeworks(self.user[self.id]['group'])
        headers = {"id": "ID", "from": "Учитель", "subject": "Предмет", "homework": "Задание", "deadline": "Срок выполнения", "student_completed": "Статус"}
        temp = []
        for item in homeworks:
            for key, value in item.items():
                teacher = get_teacher_by_id(value["from"])
                temp.append({
                    "id": key,
                    "from": teacher["name"],
                    "subject": teacher["subject"],
                    "homework": value["homework"],
                    "deadline": value["deadline"],
                    "student_completed": "Сдано" if self.id in value["students_completed"] else "Не сдано"
                })
        print(table(headers, temp))

    def make_homework(self, homework_id):
        temp_hw = get_homeworks_from_json()
        if temp_hw.get(homework_id) is None:
            print('Такой работы нет')
        elif self.id not in temp_hw[homework_id]["students_completed"] and temp_hw[homework_id]["to_group"] == self.user[self.id]["group"] :
            temp_hw[homework_id]["students_completed"].append(self.id)
        else:
            print('Ошибка при сдаче ДЗ')        
        write_homeworks_to_json(temp_hw)


    def do_command(self, command):
        if command in [str(item) for item in self.commannds.keys()]:
            if command == "0":
                self.view_homework()
            elif command == "1":
                self.make_homework(input("Введите id работы: "))
        else:
            print("Invalid command")