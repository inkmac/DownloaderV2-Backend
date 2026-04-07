import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, TypeVar, Generic

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QDialogButtonBox,
    QSpinBox, QCheckBox, QWidget
)

T = TypeVar('T')

class SchemaField(ABC, Generic[T]):
    def __init__(self, key: str, label: str, default: T):
        self.key = key
        self.label = label
        self.default = default

    @abstractmethod
    def create_widget(self) -> QWidget:
        pass

    @abstractmethod
    def get_value(self) -> T:
        pass

    @abstractmethod
    def set_value(self, value: T):
        pass


class BoolField(SchemaField[bool]):
    def __init__(self, key: str, label: str, default: bool = False):
        super().__init__(key, label, default)
        self.widget: QCheckBox | None = None

    def create_widget(self) -> QCheckBox:
        self.widget = QCheckBox()
        self.widget.setChecked(self.default)
        return self.widget

    def get_value(self) -> bool:
        if self.widget is None:
            raise RuntimeError("Widget not created yet")
        return self.widget.isChecked()

    def set_value(self, value: bool):
        if self.widget is None:
            raise RuntimeError("Widget not created yet")
        self.widget.setChecked(value)


class IntField(SchemaField[int]):
    def __init__(self, key: str, label: str, default: int = 0, min_val: int = -1000000, max_val: int = 1000000):
        super().__init__(key, label, default)
        self.min = min_val
        self.max = max_val
        self.widget: QSpinBox | None = None

    def create_widget(self) -> QSpinBox:
        self.widget = QSpinBox()
        self.widget.setRange(self.min, self.max)
        self.widget.setValue(self.default)
        return self.widget

    def get_value(self) -> int:
        if self.widget is None:
            raise RuntimeError("Widget not created yet")
        return self.widget.value()

    def set_value(self, value: int):
        if self.widget is None:
            raise RuntimeError("Widget not created yet")
        self.widget.setValue(value)


class SettingsDialog(QDialog):
    def __init__(self, fields: list[SchemaField]):
        super().__init__()
        self.setWindowTitle("设置")
        self.fields = fields

        self.setMinimumWidth(250)

        layout = QVBoxLayout()
        form = QFormLayout()

        for field in fields:
            widget = field.create_widget()
            form.addRow(field.label, widget)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_settings(self) -> dict[str, Any]:
        result = {}
        for field in self.fields:
            result[field.key] = field.get_value()
        return result

    def save_to_file(self, path: Path):
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)

        settings = self.get_settings()

        with path.open('w', encoding='utf-8') as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)  # type: ignore[arg-type]

    def load_from_file(self, path: Path):
        if not path.exists():
            return

        with path.open('r', encoding='utf-8') as file:
            settings = json.load(file)

        for field in self.fields:
            if field.key in settings:
                field.set_value(settings[field.key])