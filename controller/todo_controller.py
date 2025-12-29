import sys
from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget, QInputDialog, QMessageBox, QDialog
from sqlalchemy.orm import Session
from datetime import datetime
from view.todo_app_ui import ToDoAppUI
from model.task_manager import TaskManager
from model.engine import Session, engine
from controller.new_task import NewTask
from view.form_adaptation import FormAdaptation

class ToDoController:
    def __init__(self): 
        self.db_session = Session(engine)
        self.task_manager = TaskManager
        self.app = QApplication(sys.argv)
        self.view = ToDoAppUI()
        self.get_all()
        self.connect_signals()
        self.refresh_tasks()
        self.view.show()

    def get_all(self, status = None):
        print("Searching for all tasks...")
        return TaskManager.list_task(self.db_session)
    
    def send_exclusion(self, id):
        print("Starting exclusion process")
        if id:
            TaskManager.exclude_task(id, self.db_session)
        
        self.refresh_tasks()
        return print("Tarefa excluída com sucesso")
    
    def handle_add_task(self):
        text_ = self.view.task_input.text()

        try:
            if not text_:
                return
            
            new_task = NewTask(
                description=text_,
                complete=False
            )

            self.task_manager.add_task(self.db_session, new_task)
            self.view.task_input.clear()
            self.refresh_tasks()
        except Exception as e:
            self.view.show_message_box(QMessageBox.Icon.Critical,"Error", f"{e}")
            self.db_session.rollback()

    def refresh_tasks(self, filter_dict=None):
        self.view.todo_list_widget.clear()

        try:
            if filter_dict:
                lst_tasks = self.task_manager.filter_task(self.db_session, filter_dict)
            else:
                lst_tasks: list = self.task_manager.list_task(self.db_session)
                # ativas = len([t for t in lst_tasks if not t.complete])
                # self.view.active_count_label.setText(f"{ativas} tarefas ativas")
                todas_as_tasks = self.task_manager.list_task(self.db_session)
                ativas = len([t for t in todas_as_tasks if not t.complete])
                self.view.active_count_label.setText(f"{ativas} tarefas ativas")

            for l in lst_tasks:
                check_b, edit_b, remove_b, task_lbl, list_items = self.view.add_task_item(l.task, l.complete, str(l.created_at))

                check_b.clicked.connect(
                    lambda _, id_atual = l.id, status_atual = l.complete: self.handle_toggle_task(id_atual, status_atual)
                )

                edit_b.clicked.connect(
                    lambda _, id_atual=l.id: self.handle_edit(id_atual)
                )

                remove_b.clicked.connect(
                    lambda _, id_atual=l.id: self.send_exclusion(id_atual)
                )

            self.view.show_message_box(QMessageBox.Icon.Information, "Items carregados com sucesso", "success")
        except Exception as e:
            self.view.show_message_box(QMessageBox.Icon.Critical,"Error", f"{e}")
            return None
        
    def connect_signals(self):
        self.view.add_button.clicked.connect(
            lambda: self.handle_add_task()
        )
        def aplicar_filtro(filtro, btn_clicado):
            self.view.filter_all.setChecked(False)
            self.view.filter_active.setChecked(False)
            self.view.filter_completed.setChecked(False)
            btn_clicado.setChecked(True)
            self.refresh_tasks(filtro)

        self.view.filter_all.clicked.connect(lambda: aplicar_filtro(None, self.view.filter_all))
        self.view.filter_active.clicked.connect(lambda: aplicar_filtro({"complete": False}, self.view.filter_active))
        self.view.filter_completed.clicked.connect(lambda: aplicar_filtro({"complete": True}, self.view.filter_completed))

    def handle_edit(self, task_id):
        if task_id:
            try:
                tasks = self.task_manager.filter_task(self.db_session, {"id": task_id})
                
                if tasks:
                    t = tasks[0]
                    dialogo = FormAdaptation(self.view, t.task, t.description)

                    print("Abrindo diálogo...")
                    if dialogo.exec():
                        data = dialogo.get_values()
                        success = self.task_manager.update_task(self.db_session, task_id, **data)
                        
                        if success == True:
                            self.refresh_tasks()
                            self.view.show_message_box(QMessageBox.Icon.Information, "Success", "operação concluída com sucesso")
            except Exception as e:
                self.view.show_message_box(QMessageBox.Icon.Critical, "Errors", f"{e}")

    def handle_toggle_task(self, task_id, current_status):
        if task_id:
            try:
                updt_task = self.task_manager.update_task(self.db_session, task_id, complete = not current_status)
                if updt_task == True:
                    self.refresh_tasks()

            except Exception as e:
                self.view.show_message_box(QMessageBox.Icon.Critical, "Errors", f"{e}")