"""Main GUI window using PySide6 with pandas-powered QTableView."""
import sys
import os
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                               QPushButton, QTableView, QProgressBar, QLabel, QFileDialog, 
                               QSplitter, QMessageBox, QTabWidget)
from PySide6.QtCore import QAbstractTableModel, Qt, Signal
from PySide6.QtGui import QFont
from typing import Optional
import numpy as np

# Local imports
from ..processors.log_processor import LogProcessor
from ..exporters.excel_exporter import ExcelExporter

class PandasModel(QAbstractTableModel):
    """Model for displaying pandas DataFrame in QTableView."""
    def __init__(self, dataframe: pd.DataFrame = pd.DataFrame()):
        super().__init__()
        self._dataframe = dataframe
    
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            value = self._dataframe.iloc[index.row(), index.column()]
            return str(value)
        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter | Qt.AlignLeft
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])
            return str(self._dataframe.index[section])
        return None
    
    def rowCount(self, parent=None):
        return len(self._dataframe)
    
    def columnCount(self, parent=None):
        return len(self._dataframe.columns)
    
    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe
    
    @dataframe.setter
    def dataframe(self, df: pd.DataFrame):
        self._dataframe = df
        self.layoutChanged.emit()

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VISOR SEEKER GRAFICO - Log Processor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Core objects
        self.processor = LogProcessor()
        self.exporter = ExcelExporter()
        self.raw_model = PandasModel()
        self.cleaned_model = PandasModel()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        self.load_btn = QPushButton("📁 Cargar Logs")
        self.load_btn.clicked.connect(self.load_file)
        self.process_btn = QPushButton("🔄 Procesar Datos")
        self.process_btn.clicked.connect(self.process_data)
        self.export_btn = QPushButton("📊 Exportar Excel")
        self.export_btn.clicked.connect(self.export_excel)
        
        buttons_layout.addWidget(self.load_btn)
        buttons_layout.addWidget(self.process_btn)
        buttons_layout.addWidget(self.export_btn)
        layout.addLayout(buttons_layout)
        
        # Tab for previews
        self.tabs = QTabWidget()
        self.raw_view = QTableView()
        self.raw_view.setModel(self.raw_model)
        self.raw_view.setAlternatingRowColors(True)
        self.raw_view.setFont(QFont("Consolas", 9))
        self.cleaned_view = QTableView()
        self.cleaned_view.setModel(self.cleaned_model)
        self.cleaned_view.setAlternatingRowColors(True)
        self.cleaned_view.setFont(QFont("Consolas", 9))
        
        self.tabs.addTab(self.raw_view, "Datos Crudos")
        self.tabs.addTab(self.cleaned_view, "Datos Limpios")
        layout.addWidget(self.tabs)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Status label
        self.status_label = QLabel("Listo para cargar archivo de logs.")
        layout.addWidget(self.status_label)
        
        self.file_path: Optional[str] = None
    
    def load_file(self):
        """Load log file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo de logs", "", "CSV files (*.csv *.txt);;All files (*)"
        )
        if not file_path:
            return
        
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.status_label.setText("Cargando archivo...")
        QApplication.processEvents()
        
        try:
            self.file_path = file_path
            self.raw_model.dataframe = self.processor.parse_file(file_path)
            self.progress.setValue(50)
            self.status_label.setText(f"Cargados {len(self.raw_model.dataframe)} filas.")
            self.tabs.setCurrentWidget(self.raw_view)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error cargando archivo:\n{str(e)}")
            self.status_label.setText("Error al cargar archivo.")
        finally:
            self.progress.setValue(100)
            self.progress.setVisible(False)
    
    def process_data(self):
        """Process and clean data."""
        if self.processor.raw_df is None:
            QMessageBox.warning(self, "Advertencia", "Carga un archivo primero.")
            return
        
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.status_label.setText("Procesando datos...")
        QApplication.processEvents()
        
        try:
            self.cleaned_model.dataframe = self.processor.clean_data(self.processor.raw_df)
            self.progress.setValue(100)
            self.status_label.setText(f"Datos limpios: {len(self.cleaned_model.dataframe)} filas.")
            self.tabs.setCurrentWidget(self.cleaned_view)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error procesando:\n{str(e)}")
        finally:
            self.progress.setVisible(False)
    
    def export_excel(self):
        """Export to Excel."""
        if self.processor.cleaned_df is None:
            QMessageBox.warning(self, "Advertencia", "Procesa los datos primero.")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Excel", "seeker_logs_processed.xlsx", "Excel files (*.xlsx)"
        )
        if not output_path:
            return
        
        try:
            self.progress.setVisible(True)
            self.progress.setValue(0)
            self.status_label.setText("Exportando a Excel...")
            QApplication.processEvents()
            
            self.exporter.export(self.processor.cleaned_df, output_path)
            self.progress.setValue(100)
            self.status_label.setText(f"Exportado a {output_path}")
            QMessageBox.information(self, "Éxito", "Archivo Excel creado con dashboard.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exportando:\n{str(e)}")
        finally:
            self.progress.setVisible(False)
