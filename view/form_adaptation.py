from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox

class FormAdaptation(QDialog):
    def __init__(self, parent=None,text_input = "", desc_input = ""):
        super().__init__(parent)
        text_input = text_input
        desc_input = desc_input

        self.setWindowTitle("Editar tarefa: ")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Título da Tarefa:"))
        self.text_input = QLineEdit()
        self.text_input.setText(text_input)
        layout.addWidget(self.text_input)

        layout.addWidget(QLabel("Descrição: "))
        self.desc_input = QLineEdit()
        self.desc_input.setText(desc_input)
        layout.addWidget(self.desc_input)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(
            self.accept
        )
        self.buttons.rejected.connect(
            self.reject
        )
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_values(self):
        return {
            "task": self.text_input.text(),
            "description": self.desc_input.text() 
        }