import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox 
)
from PyQt6.QtCore import Qt, QSize 
from PyQt6.QtGui import QFont, QIcon 
COLOR_PRIMARY_BG = "#F4F6F8"
COLOR_CONTAINER_BG = "#FFFFFF"
COLOR_DARK_TEXT = "#2C3E50"
COLOR_ACCENT = "#2980B9" # Azul
COLOR_SUCCESS = "#2ECC71" # Verde
COLOR_DANGER = "#E74C3C" # Vermelho
COLOR_FADED = "#BDC3C7" # Cinza

def get_base_stylesheet():
    return f"""
        QWidget {{ background-color: {COLOR_PRIMARY_BG}; color: {COLOR_DARK_TEXT}; font-family: 'Segoe UI', 'Arial', sans-serif; }}
        QMainWindow {{ border: 1px solid {COLOR_FADED}; }}
        #MainContainer {{ background-color: {COLOR_CONTAINER_BG}; border-radius: 10px; padding: 20px; margin: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }}
    """

def get_input_and_button_stylesheet():
    return f"""
        QLineEdit {{ padding: 10px; border: 1px solid {COLOR_FADED}; border-radius: 5px; font-size: 16px; }}
        QPushButton#AddButton {{ background-color: {COLOR_ACCENT}; color: white; border-radius: 5px; padding: 10px 15px; font-size: 16px; font-weight: bold; min-width: 100px; }}
        QPushButton#AddButton:hover {{ background-color: #3498DB; }}
    """

def get_filter_button_stylesheet(): 
    return f"""
        QPushButton {{
            border: 1px solid {COLOR_FADED};
            border-radius: 5px;
            padding: 5px 10px;
            background-color: {COLOR_CONTAINER_BG};
            color: {COLOR_DARK_TEXT};
        }}
        QPushButton:checked {{
            background-color: {COLOR_ACCENT};
            color: white;
            border-color: {COLOR_ACCENT};
        }}
        QPushButton:hover {{
            background-color: #ECF0F1; /* Um leve hover */
        }}
        QPushButton:checked:hover {{
            background-color: #3498DB; /* Hover para botão checado */
        }}
    """

def get_list_stylesheet():
    return f"""
        QListWidget {{ border: none; background-color: {COLOR_CONTAINER_BG}; }}
        QListWidget::item {{ padding: 10px 0; border-bottom: 1px solid #ECF0F1; }}
        .task_text_active {{ color: {COLOR_DARK_TEXT}; font-size: 15px; }}
        .task_text_completed {{ color: {COLOR_FADED}; font-size: 15px; text-decoration: line-through; }} /* A decoração é apenas para intenção */
        QPushButton {{ border: none; padding: 5px; border-radius: 3px; font-size: 14px; }}
        QPushButton.remove_btn {{ color: {COLOR_DANGER}; background-color: transparent; }}
        QPushButton.remove_btn:hover {{ color: #C0392B; }}
    """

class ToDoAppUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do App")
        self.setGeometry(100, 100, 600, 700) 
        self.setStyleSheet(get_base_stylesheet()) 

        self.init_ui()

    def init_ui(self):
        main_container = QWidget()
        main_container.setObjectName("MainContainer")
        self.setCentralWidget(main_container)
        main_layout = QVBoxLayout(main_container)
        main_layout.setSpacing(15)

        # Título do App
        title_label = QLabel("Minhas Tarefas")
        title_font = QFont("Segoe UI", 28, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        main_layout.addWidget(title_label)

        input_layout = QHBoxLayout() 
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Adicionar nova tarefa...")
        self.task_input.setStyleSheet(get_input_and_button_stylesheet())
        
        self.add_button = QPushButton("Adicionar")
        self.add_button.setObjectName("AddButton") # Para CSS específico
        self.add_button.setStyleSheet(get_input_and_button_stylesheet())
        
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)
        main_layout.addLayout(input_layout)

        controls_layout = QHBoxLayout()
        
        self.active_count_label = QLabel("0 tarefas ativas")
        self.active_count_label.setFont(QFont("Segoe UI", 12))
        self.active_count_label.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold;")
        
        self.filter_all = QPushButton("Todas")
        self.filter_active = QPushButton("Ativas")
        self.filter_completed = QPushButton("Concluídas")
        
        self.filter_all.setCheckable(True)
        self.filter_all.setChecked(True) 
        self.filter_active.setCheckable(True)
        self.filter_completed.setCheckable(True)
        
        self.filter_all.setStyleSheet(get_filter_button_stylesheet())
        self.filter_active.setStyleSheet(get_filter_button_stylesheet())
        self.filter_completed.setStyleSheet(get_filter_button_stylesheet())
        
        controls_layout.addWidget(self.active_count_label)
        controls_layout.addStretch(1) 
        controls_layout.addWidget(self.filter_all)
        controls_layout.addWidget(self.filter_active)
        controls_layout.addWidget(self.filter_completed)
        
        main_layout.addLayout(controls_layout)

        self.todo_list_widget = QListWidget()
        self.todo_list_widget.setStyleSheet(get_list_stylesheet())
        main_layout.addWidget(self.todo_list_widget)

    def add_task_item(self, text, is_completed, date_str):
        
        list_item = QListWidgetItem(self.todo_list_widget)
        
        task_widget = QWidget()
        task_layout = QHBoxLayout(task_widget)
        task_layout.setContentsMargins(0, 5, 0, 5) 

        check_btn = QPushButton()
        check_btn.setFixedSize(QSize(24, 24))
        check_btn.setText("✔" if is_completed else "") # Texto condicional
        check_btn.setStyleSheet(
            f"color: {COLOR_SUCCESS}; border: none;" if is_completed else 
            f"color: {COLOR_FADED}; border: 1px solid {COLOR_FADED}; border-radius: 12px;"
        )
        task_layout.addWidget(check_btn)

        text_container = QVBoxLayout()
        task_label = QLabel(text)
        task_label.setFont(QFont("Segoe UI", 12))
        task_label.setStyleSheet(".task_text_completed" if is_completed else ".task_text_active")
        
        date_label = QLabel(f"Criada em: {date_str}")
        date_label.setFont(QFont("Segoe UI", 9))
        date_label.setStyleSheet(f"color: {COLOR_FADED};")
        
        text_container.addWidget(task_label)
        text_container.addWidget(date_label)
        task_layout.addLayout(text_container)
        task_layout.addStretch(1) 

        edit_btn = QPushButton("✏️")
        edit_btn.setStyleSheet(f"color: {COLOR_ACCENT}; background-color: transparent;")
        edit_btn.setFixedSize(QSize(30, 30))
        task_layout.addWidget(edit_btn)
        
        remove_btn = QPushButton("🗑️")
        remove_btn.setObjectName("remove_btn")
        remove_btn.setFixedSize(QSize(30, 30))
        task_layout.addWidget(remove_btn)

        list_item.setSizeHint(task_widget.sizeHint())
        self.todo_list_widget.setItemWidget(list_item, task_widget)

        return check_btn, edit_btn, remove_btn, task_label, list_item
    
    def show_message_box(self, icon, title, message):
        msg_box = QMessageBox(icon, title, message, QMessageBox.StandardButton.Ok, self)
        msg_box.exec()

    # @staticmethod
    # def receive_active_todo():


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoAppUI()
    window.show()
    sys.exit(app.exec())