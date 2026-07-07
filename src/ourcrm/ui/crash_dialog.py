from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CrashDialog(QDialog):
    def __init__(
        self,
        summary: str,
        full_traceback: str,
        log_path: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("OurCRM Encountered an Error")
        self._full_traceback = full_traceback

        layout = QVBoxLayout(self)

        summary_label = QLabel(summary)
        summary_label.setObjectName("crash_summary_label")
        summary_label.setWordWrap(True)
        layout.addWidget(summary_label)

        log_path_label = QLabel(f"Details saved to: {log_path}")
        log_path_label.setObjectName("crash_log_path_label")
        log_path_label.setWordWrap(True)
        layout.addWidget(log_path_label)

        copy_button = QPushButton("Copy Details")
        copy_button.setObjectName("crash_copy_details_btn")
        copy_button.clicked.connect(self._copy_details)
        layout.addWidget(copy_button)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    def _copy_details(self) -> None:
        QApplication.clipboard().setText(self._full_traceback)
