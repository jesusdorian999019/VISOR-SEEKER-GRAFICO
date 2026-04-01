# VISOR SEEKER GRAFICO - Log Processor

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.5%2B-orange)](https://pypi.org/project/PySide6/)
[![pandas](https://img.shields.io/badge/pandas-2.0%2B-green)](https://pypi.org/project/pandas/)
[![openpyxl](https://img.shields.io/badge/openpyxl-3.1%2B-purple)](https://pypi.org/project/openpyxl/)

Herramienta profesional en Python con interfaz gráfica para procesar logs de Seeker y exportarlos a Excel con dashboard.

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone <repo-url>
   cd VISOR-SEEKER-GRAFICO
   ```

2. Crea entorno virtual (recomendado):
   ```bash
   python -m venv venv
   # Windows
   venv\\Scripts\\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Uso

1. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

2. Carga un archivo de logs (CSV-like con campos: OS, Platform, CPU Cores, etc.)
3. Revisa vista previa de datos crudos
4. Procesa datos (limpieza automática)
5. Revisa datos limpios
6. Exporta a Excel (con dashboard de gráficos)

## 📁 Estructura del Proyecto

```
.
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
├── TODO.md                # Progreso de desarrollo
├── example_logs.csv       # Ejemplo de logs
└── src/
    ├── __init__.py
    ├── gui/
    │   ├── __init__.py
    │   └── main_window.py # Interfaz gráfica
    ├── processors/
    │   ├── __init__.py
    │   └── log_processor.py # Procesamiento de datos
    └── exporters/
        ├── __init__.py
        └── excel_exporter.py # Exportación Excel
```

## 🧪 Ejemplo

Usa `example_logs.csv` para probar. El Excel generado tendrá:
- Hoja **Data**: Tabla limpia con estilos
- Hoja **Dashboard**: Gráficos (OS, ISP, Ciudades Top-10)

## 🔧 Características

- ✅ Interfaz profesional PySide6
- ✅ Parseo robusto de logs Seeker
- ✅ Limpieza automática (NA → NaN, split resolución)
- ✅ Exportación Excel con gráficos automáticos
- ✅ Vista previa interactiva
- ✅ Manejo de errores
- ✅ Código limpio PEP8 + type hints

## 📄 Licencia

MIT License
