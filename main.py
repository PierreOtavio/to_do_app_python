from controller.todo_controller import ToDoController
import sys

if __name__ == "__main__":
    controller = ToDoController()
    sys.exit(controller.app.exec())