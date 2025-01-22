import pandas as pd
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QFileDialog,
    QLineEdit,
    QListWidget,
    QColorDialog,
    QCheckBox,
    QFontDialog,
    QScrollArea,
    QGridLayout,
    QInputDialog,
    QDialog,
    QDialogButtonBox,
    QSpinBox,
    QDoubleSpinBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import plotly.graph_objects as go
from PyQt5.QtWebEngineWidgets import QWebEngineView
import numpy as np


class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráfico Personalizado")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 11pt;
            }
            QPushButton {
                border: 1px solid #b0b0b0;
                border-radius: 4px;
                padding: 5px;
                min-height: 25px;
            }
            QLineEdit {
                border: 1px solid #b0b0b0;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox {
                border: 1px solid #b0b0b0;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget {
                border: 1px solid #b0b0b0;
                border-radius: 4px;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        # Layout principal
        main_layout = QHBoxLayout()
        
        # Painel de controle (lado esquerdo)
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_layout.setSpacing(10)
        
        # Upload do arquivo
        upload_layout = QHBoxLayout()
        self.file_button = QPushButton("Upload")
        self.file_button.clicked.connect(self.upload_file)
        upload_layout.addWidget(self.file_button)
        control_layout.addLayout(upload_layout)
        
        # Tipo de gráfico
        graph_type_layout = QHBoxLayout()
        graph_type_layout.addWidget(QLabel("Tipo de Gráfico"))
        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems([
            "Pontos",
            "Linhas",
            "Barras",
            "Barras Empilhadas",
            "Barras Horizontais",
            "Área",
            "Área Empilhada",
            "Setores",
            "Rosca",
            "Histograma",
            "Violino",
            "Caixa",
            "Dispersão 3D",
            "Bolhas",
            "Radar",
            "Heatmap"
        ])
        self.graph_type_combo.currentTextChanged.connect(self.update_graph)
        graph_type_layout.addWidget(self.graph_type_combo)
        control_layout.addLayout(graph_type_layout)
        
        # Cores, Formas e Legendas
        color_section = QVBoxLayout()
        color_header = QHBoxLayout()
        color_header.addWidget(QLabel("Cor, Forma e Legenda"))
        self.add_color_button = QPushButton("Adicionar")
        self.add_color_button.clicked.connect(self.add_color_and_symbol)
        self.edit_color_button = QPushButton("Editar")
        self.edit_color_button.clicked.connect(self.edit_color_and_symbol)
        self.remove_color_button = QPushButton("Remover")
        self.remove_color_button.clicked.connect(self.remove_color_and_symbol)
        color_header.addWidget(self.add_color_button)
        color_header.addWidget(self.edit_color_button)
        color_header.addWidget(self.remove_color_button)
        color_section.addLayout(color_header)
        
        # Lista de cores e símbolos
        self.items_list = QListWidget()
        self.items_list.setMinimumHeight(100)
        color_section.addWidget(self.items_list)
        control_layout.addLayout(color_section)
        
        # Botões de texto
        text_buttons_layout = QGridLayout()
        self.title_button = QPushButton("Título")
        self.title_button.clicked.connect(self.configure_title)
        self.legend_button = QPushButton("Legenda")
        self.legend_button.clicked.connect(self.configure_legend)
        self.x_axis_button = QPushButton("Eixo X")
        self.x_axis_button.clicked.connect(lambda: self.configure_axis('x'))
        self.y_axis_button = QPushButton("Eixo Y")
        self.y_axis_button.clicked.connect(lambda: self.configure_axis('y'))
        
        text_buttons_layout.addWidget(self.title_button, 0, 0)
        text_buttons_layout.addWidget(self.legend_button, 0, 1)
        text_buttons_layout.addWidget(self.x_axis_button, 0, 2)
        text_buttons_layout.addWidget(self.y_axis_button, 0, 3)
        control_layout.addLayout(text_buttons_layout)
        
        # Limites
        limits_layout = QGridLayout()
        limits_layout.addWidget(QLabel("Limites:"), 0, 0)
        limits_layout.addWidget(QLabel("X"), 1, 0)
        limits_layout.addWidget(QLabel("Y"), 2, 0)
        
        self.xmin_input = QLineEdit()
        self.xmax_input = QLineEdit()
        self.ymin_input = QLineEdit()
        self.ymax_input = QLineEdit()
        
        limits_layout.addWidget(self.xmin_input, 1, 1)
        limits_layout.addWidget(self.xmax_input, 1, 2)
        limits_layout.addWidget(self.ymin_input, 2, 1)
        limits_layout.addWidget(self.ymax_input, 2, 2)
        
        control_layout.addLayout(limits_layout)
        
        # Barras de erro (única checkbox que permanece)
        self.error_bar_checkbox = QCheckBox("Barras de Erro")
        self.error_bar_checkbox.stateChanged.connect(self.update_graph)
        control_layout.addWidget(self.error_bar_checkbox)
        
        # Estilo
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("Estilo"))
        self.style_combo = QComboBox()
        self.style_combo.addItems([
            "plotly",
            "plotly_white",
            "plotly_dark",
            "ggplot2",
            "seaborn",
            "simple_white",
            "none",  # Estilo limpo
            "presentation",
            "xgridoff",
            "ygridoff",
            "gridon",
            "paper",
            "minimal",
            "classic",
            "dark_minimal",
            "journal",
            "clean"
        ])
        self.style_combo.currentTextChanged.connect(self.update_graph)
        style_layout.addWidget(self.style_combo)
        control_layout.addLayout(style_layout)
        
        # Checkbox mostrar eixos
        self.show_axes_checkbox = QCheckBox("Mostrar Eixos")
        self.show_axes_checkbox.setChecked(True)
        self.show_axes_checkbox.stateChanged.connect(self.update_graph)
        control_layout.addWidget(self.show_axes_checkbox)
        
        # Expandir lista de símbolos disponíveis
        self.available_symbols = [
            "circle", "square", "diamond", "cross", "x",
            "triangle-up", "triangle-down", "triangle-left", "triangle-right",
            "pentagon", "hexagon", "octagon", "star", "hexagram",
            "star-triangle-up", "star-triangle-down", "star-square", "star-diamond",
            "diamond-cross", "circle-cross", "circle-x", "square-x", "diamond-x",
            "hourglass", "bowtie"
        ]

        # Expandir lista de estilos
        self.available_styles = [
            "plotly", "plotly_white", "plotly_dark",
            "ggplot2", "seaborn", "simple_white",
            "presentation", "none",
            # Estilos personalizados
            "clean_axes", "minimal_grid", "publication",
            "scientific", "modern", "classic",
            "dark_minimal", "high_contrast"
        ]

        # Parâmetros específicos para cada tipo de gráfico
        self.specific_params_section = QVBoxLayout()
        self.specific_params_header = QLabel("Parâmetros Específicos")
        self.specific_params_header.setStyleSheet("font-weight: bold; font-size: 12pt;")
        self.specific_params_section.addWidget(self.specific_params_header)
        
        # Container para parâmetros específicos
        self.specific_params_widget = QWidget()
        self.specific_params_layout = QGridLayout(self.specific_params_widget)
        self.specific_params_section.addWidget(self.specific_params_widget)
        
        # Criar todos os widgets de parâmetros uma única vez
        self.create_parameter_widgets()
        
        # Conectar mudança de tipo de gráfico
        self.graph_type_combo.currentTextChanged.connect(self.update_specific_params)
        
        control_layout.addLayout(self.specific_params_section)
        
        # Adiciona espaço em branco expansível
        control_layout.addStretch()
        
        # Área do gráfico
        self.graph_view = QWebEngineView()
        
        # Adiciona os widgets ao layout principal
        main_layout.addWidget(control_panel, 1)
        main_layout.addWidget(self.graph_view, 2)
        
        self.setLayout(main_layout)

    def create_parameter_widgets(self):
        """Criar todos os widgets de parâmetros uma única vez"""
        # Parâmetros para gráficos de Pontos
        self.marker_size_spin = QSpinBox()
        self.marker_size_spin.setRange(1, 50)
        self.marker_size_spin.setValue(10)
        self.marker_size_spin.valueChanged.connect(self.update_graph)
        
        # Parâmetros para gráficos de Linhas
        self.line_width_spin = QSpinBox()
        self.line_width_spin.setRange(1, 10)
        self.line_width_spin.setValue(2)
        self.line_width_spin.valueChanged.connect(self.update_graph)
        
        self.line_style_combo = QComboBox()
        self.line_style_combo.addItems(["solid", "dot", "dash", "longdash", "dashdot"])
        self.line_style_combo.currentTextChanged.connect(self.update_graph)
        
        # Parâmetros para gráficos de Barras
        self.bar_width_spin = QDoubleSpinBox()
        self.bar_width_spin.setRange(0.1, 2.0)
        self.bar_width_spin.setSingleStep(0.1)
        self.bar_width_spin.setValue(0.8)
        self.bar_width_spin.valueChanged.connect(self.update_graph)
        
        # Parâmetros para gráficos de Pizza/Rosca
        self.hole_size_spin = QDoubleSpinBox()
        self.hole_size_spin.setRange(0, 0.8)
        self.hole_size_spin.setSingleStep(0.1)
        self.hole_size_spin.setValue(0.3)
        self.hole_size_spin.valueChanged.connect(self.update_graph)
        
        # Parâmetros para Histograma
        self.nbins_spin = QSpinBox()
        self.nbins_spin.setRange(5, 100)
        self.nbins_spin.setValue(30)
        self.nbins_spin.valueChanged.connect(self.update_graph)
        
        # Parâmetros para gráfico de Violino
        self.show_box_check = QCheckBox("Mostrar Box Plot")
        self.show_box_check.setChecked(True)
        self.show_box_check.stateChanged.connect(self.update_graph)
        
        # Parâmetros para Heatmap
        self.colorscale_combo = QComboBox()
        self.colorscale_combo.addItems([
            "Viridis", "Plasma", "Inferno", "Magma", "RdBu", "YlOrRd", "YlGnBu"
        ])
        self.colorscale_combo.currentTextChanged.connect(self.update_graph)
        
        # Opacidade (comum a vários tipos)
        self.opacity_spin = QDoubleSpinBox()
        self.opacity_spin.setRange(0.1, 1.0)
        self.opacity_spin.setSingleStep(0.1)
        self.opacity_spin.setValue(1.0)
        self.opacity_spin.valueChanged.connect(self.update_graph)

        # Esconder todos os widgets inicialmente
        for widget in [self.marker_size_spin, self.line_width_spin, self.line_style_combo,
                      self.bar_width_spin, self.hole_size_spin, self.nbins_spin,
                      self.show_box_check, self.colorscale_combo, self.opacity_spin]:
            widget.hide()

    # Métodos adicionais serão integrados abaixo...
    def add_color_and_symbol(self):
        color = QColorDialog.getColor()
        if color.isValid():
            symbol, ok = QInputDialog.getItem(
                self,
                "Selecionar Símbolo",
                "Escolha um símbolo para a cor:",
                self.available_symbols,
                editable=False,
            )
            if ok and symbol:
                legend_text, ok = QInputDialog.getText(
                    self, "Editar Legenda", "Digite o texto da legenda:"
                )
                if ok and legend_text:
                    # Armazena os três valores em uma única string separada por |
                    item_text = f"{color.name()} | {symbol} | {legend_text}"
                    self.items_list.addItem(item_text)
                    self.update_graph()

    def remove_color_and_symbol(self):
        selected_indices = self.items_list.selectedIndexes()
        if selected_indices:
            for index in selected_indices:
                self.items_list.takeItem(index.row())
            self.update_graph()

    def configure_title(self):
        dialog = TextConfigDialog("Configuração do Título", self)
        if dialog.exec_():
            self.title_text = dialog.text
            self.title_font = dialog.font
            self.title_alignment = dialog.alignment
            self.update_graph()

    def configure_legend(self):
        dialog = TextConfigDialog("Configuração da Legenda", self)
        if dialog.exec_():
            self.legend_text = dialog.text
            self.legend_font = dialog.font
            self.legend_alignment = dialog.alignment
            self.update_graph()

    def configure_axis(self, axis_type):
        dialog = AxisConfigDialog(f"Configuração do Eixo {axis_type.upper()}", axis_type, self)
        if dialog.exec_():
            if axis_type == 'x':
                self.xlabel_text = dialog.text
                self.xlabel_font = dialog.font
                self.xlabel_alignment = dialog.alignment
                self.x_scientific = dialog.scientific
            else:
                self.ylabel_text = dialog.text
                self.ylabel_font = dialog.font
                self.ylabel_alignment = dialog.alignment
                self.y_scientific = dialog.scientific
            self.update_graph()

    def edit_color_and_symbol(self):
        current_row = self.items_list.currentRow()
        if current_row >= 0:
            current_item = self.items_list.item(current_row)
            color_hex, symbol, legend = current_item.text().split(" | ")
            
            # Menu de opções para edição
            option, ok = QInputDialog.getItem(
                self,
                "Editar Item",
                "O que você deseja editar?",
                ["Cor", "Símbolo", "Legenda", "Tudo"],
                current=0,
                editable=False
            )
            
            if ok:
                new_color = color_hex
                new_symbol = symbol
                new_legend = legend
                
                if option in ["Cor", "Tudo"]:
                    color = QColorDialog.getColor()
                    if color.isValid():
                        new_color = color.name()
                
                if option in ["Símbolo", "Tudo"]:
                    symbol_choice, ok = QInputDialog.getItem(
                        self,
                        "Selecionar Símbolo",
                        "Escolha um símbolo:",
                        self.available_symbols,
                        editable=False
                    )
                    if ok:
                        new_symbol = symbol_choice
                
                if option in ["Legenda", "Tudo"]:
                    legend_text, ok = QInputDialog.getText(
                        self,
                        "Editar Legenda",
                        "Digite o texto da legenda:",
                        text=legend
                    )
                    if ok:
                        new_legend = legend_text
                
                item_text = f"{new_color} | {new_symbol} | {new_legend}"
                self.items_list.item(current_row).setText(item_text)
                self.update_graph()

    def upload_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione o arquivo de dados",
            "",
            "Arquivos CSV (*.csv);;Arquivos Excel (*.xlsx)",
            options=options,
        )
        if file_path:
            self.file_path = file_path
            self.file_button.setText(f"Arquivo: {file_path.split('/')[-1]}")
            self.update_graph()

    def update_graph(self):
        if not self.file_path:
            self.file_button.setText("Por favor, envie um arquivo de dados!")
            return

        try:
            # Lê os dados
            if self.file_path.endswith(".csv"):
                data = pd.read_csv(self.file_path)
            elif self.file_path.endswith(".xlsx"):
                data = pd.read_excel(self.file_path)
            else:
                self.file_button.setText("Formato de arquivo não suportado!")
                return

            # Configurações do gráfico
            graph_type = self.graph_type_combo.currentText()
            
            # Extrai cores, símbolos e legendas da lista
            items = []
            for i in range(self.items_list.count()):
                item_text = self.items_list.item(i).text()
                color, symbol, legend = item_text.split(" | ")
                items.append((color, symbol, legend))
            
            colors = [item[0] for item in items]
            symbols = [item[1] for item in items] if graph_type == "Pontos" else []
            legend_texts = [item[2] for item in items]

            fig = go.Figure()
            
            # Aplicar estilo
            template = self.style_combo.currentText()
            if template != "none":
                fig.update_layout(template=template)

            # Helper functions
            def format_scientific(value):
                if value == 0:
                    return "0"
                exponent = int(np.floor(np.log10(abs(value))))
                coefficient = value / 10**exponent
                return f"{coefficient:.1f}×10<sup>{exponent}</sup>"

            def get_optimal_ticks(values, n_ticks=6):
                min_val = np.min(values)
                max_val = np.max(values)
                if min_val > 0 and max_val > 0:
                    return np.logspace(np.log10(min_val), np.log10(max_val), n_ticks)
                return np.linspace(min_val, max_val, n_ticks)

            # Configurações de eixos
            x_min = float(self.xmin_input.text()) if self.xmin_input.text() else None
            x_max = float(self.xmax_input.text()) if self.xmax_input.text() else None
            y_min = float(self.ymin_input.text()) if self.ymin_input.text() else None
            y_max = float(self.ymax_input.text()) if self.ymax_input.text() else None

            # Get optimal tick values
            x_ticks = get_optimal_ticks(data.iloc[:, 0])
            y_ticks = get_optimal_ticks(data.iloc[:, 1])

            # Configurações de eixos
            show_axes = self.show_axes_checkbox.isChecked()
            
            layout_config = {
                'title': {
                    'text': self.title_text if hasattr(self, "title_text") else "",
                    'x': 0.5,
                    'y': 0.95,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {
                        'size': 20,
                        'family': self.title_font.family() if hasattr(self, "title_font") else None
                    },
                    'pad': {'b': 20}
                },
                'margin': {'l': 80, 'r': 50, 't': 100, 'b': 80},
                'showlegend': True,
                'legend': {
                    'yanchor': "top",
                    'y': 0.99,
                    'xanchor': "right",
                    'x': 0.99,
                    'bgcolor': 'rgba(255,255,255,0.8)',
                    'bordercolor': 'rgba(0,0,0,0.2)',
                    'borderwidth': 1
                },
                'plot_bgcolor': 'white',
                'paper_bgcolor': 'white',
                'xaxis': {
                    'title': {
                        'text': self.xlabel_text if hasattr(self, "xlabel_text") else "",
                        'font': {
                            'size': self.xlabel_font.pointSize(),
                            'family': self.xlabel_font.family()
                        } if hasattr(self, "xlabel_font") else None
                    },
                    'range': [x_min, x_max] if x_min is not None and x_max is not None else None,
                    'showline': show_axes,
                    'linecolor': 'black',
                    'linewidth': 2,
                    'showgrid': False,
                    'zeroline': show_axes,
                    'zerolinecolor': 'black',
                    'zerolinewidth': 2,
                    'showticklabels': show_axes,
                    'tickmode': 'array' if hasattr(self, "x_scientific") and self.x_scientific else 'auto',
                    'ticktext': [format_scientific(x) for x in x_ticks] if hasattr(self, "x_scientific") and self.x_scientific else None,
                    'tickvals': x_ticks if hasattr(self, "x_scientific") and self.x_scientific else None,
                    'mirror': True if show_axes else False,
                    'ticks': 'outside',
                    'tickwidth': 1,
                    'ticklen': 8,
                    'tickfont': {'size': 10},
                    'automargin': True
                },
                'yaxis': {
                    'title': {
                        'text': self.ylabel_text if hasattr(self, "ylabel_text") else "",
                        'font': {
                            'size': self.ylabel_font.pointSize(),
                            'family': self.ylabel_font.family()
                        } if hasattr(self, "ylabel_font") else None
                    },
                    'range': [y_min, y_max] if y_min is not None and y_max is not None else None,
                    'showline': show_axes,
                    'linecolor': 'black',
                    'linewidth': 2,
                    'showgrid': False,
                    'zeroline': show_axes,
                    'zerolinecolor': 'black',
                    'zerolinewidth': 2,
                    'showticklabels': show_axes,
                    'tickmode': 'array' if hasattr(self, "y_scientific") and self.y_scientific else 'auto',
                    'ticktext': [format_scientific(y) for y in y_ticks] if hasattr(self, "y_scientific") and self.y_scientific else None,
                    'tickvals': y_ticks if hasattr(self, "y_scientific") and self.y_scientific else None,
                    'mirror': True if show_axes else False,
                    'ticks': 'outside',
                    'tickwidth': 1,
                    'ticklen': 8,
                    'tickfont': {'size': 10},
                    'automargin': True
                }
            }

            # Atualizar layout base
            fig.update_layout(**layout_config)

            # Configurações específicas para gráficos 3D
            if graph_type == "Dispersão 3D":
                scene_config = {
                    'scene': {
                        'xaxis_title': self.xlabel_text if hasattr(self, "xlabel_text") else "",
                        'yaxis_title': self.ylabel_text if hasattr(self, "ylabel_text") else "",
                        'zaxis_title': "Z"
                    }
                }
                fig.update_layout(**scene_config)

            # Geração dos diferentes tipos de gráficos
            if graph_type == "Pontos":
                for i, col in enumerate(data.columns[1:len(colors) + 1]):
                    fig.add_trace(
                        go.Scatter(
                            x=data.iloc[:, 0],
                            y=data[col],
                            mode="markers",
                            name=legend_texts[i],
                            marker=dict(
                                color=colors[i % len(colors)],
                                size=self.marker_size_spin.value(),
                                symbol=symbols[i % len(symbols)],
                                opacity=self.opacity_spin.value()
                            ),
                            error_y=dict(type="data", array=data[col] * 0.1)
                            if self.error_bar_checkbox.isChecked()
                            else None,
                        )
                    )
            elif graph_type == "Linhas":
                for i, col in enumerate(data.columns[1:len(colors) + 1]):
                    fig.add_trace(
                        go.Scatter(
                            x=data.iloc[:, 0],
                            y=data[col],
                            mode="lines",
                            name=legend_texts[i],
                            line=dict(
                                color=colors[i % len(colors)],
                                width=self.line_width_spin.value(),
                                dash=self.line_style_combo.currentText()
                            ),
                            opacity=self.opacity_spin.value()
                        )
                    )
            elif graph_type == "Barras":
                for i, col in enumerate(data.columns[1:]):
                    fig.add_trace(
                        go.Bar(
                            x=data.iloc[:, 0],
                            y=data[col],
                            name=legend_texts[i] if i < len(legend_texts) else col,
                            marker=dict(
                                color=colors[i % len(colors)] if colors else f'rgb({np.random.randint(0,255)}, {np.random.randint(0,255)}, {np.random.randint(0,255)})',
                            ),
                            opacity=self.opacity_spin.value(),
                            width=self.bar_width_spin.value()
                        )
                    )
                fig.update_layout(
                    bargap=0.15,
                    bargroupgap=0.1
                )
            elif graph_type == "Barras Empilhadas":
                for i, col in enumerate(data.columns[1:]):
                    fig.add_trace(
                        go.Bar(
                            x=data.iloc[:, 0],
                            y=data[col],
                            name=legend_texts[i] if i < len(legend_texts) else col,
                            marker=dict(
                                color=colors[i % len(colors)] if colors else f'rgb({np.random.randint(0,255)}, {np.random.randint(0,255)}, {np.random.randint(0,255)})',
                            ),
                            opacity=self.opacity_spin.value(),
                            width=self.bar_width_spin.value()
                        )
                    )
                fig.update_layout(
                    barmode='stack',
                    bargap=0.15,
                    bargroupgap=0.1
                )
            elif graph_type == "Barras Horizontais":
                for i, col in enumerate(data.columns[1:]):
                    fig.add_trace(
                        go.Bar(
                            y=data.iloc[:, 0],
                            x=data[col],
                            name=legend_texts[i] if i < len(legend_texts) else col,
                            marker=dict(
                                color=colors[i % len(colors)] if colors else f'rgb({np.random.randint(0,255)}, {np.random.randint(0,255)}, {np.random.randint(0,255)})',
                            ),
                            opacity=self.opacity_spin.value(),
                            width=self.bar_width_spin.value(),
                            orientation='h'
                        )
                    )
                fig.update_layout(
                    bargap=0.15,
                    bargroupgap=0.1
                )
            elif graph_type in ["Área", "Área Empilhada"]:
                for i, col in enumerate(data.columns[1:len(colors) + 1]):
                    fig.add_trace(
                        go.Scatter(
                            x=data.iloc[:, 0],
                            y=data[col],
                            name=legend_texts[i],
                            fill='tonexty' if graph_type == "Área Empilhada" else 'tozeroy',
                            line=dict(
                                color=colors[i % len(colors)],
                                width=self.line_width_spin.value()
                            ),
                            opacity=self.opacity_spin.value()
                        )
                    )
            elif graph_type == "Setores":
                fig.add_trace(
                    go.Pie(
                        labels=data.iloc[:, 0],
                        values=data.iloc[:, 1],
                        textinfo="label+percent",
                        marker=dict(colors=colors),
                        opacity=self.opacity_spin.value()
                    )
                )
            elif graph_type == "Rosca":
                fig.add_trace(
                    go.Pie(
                        labels=data.iloc[:, 0],
                        values=data.iloc[:, 1],
                        hole=self.hole_size_spin.value(),
                        textinfo="label+percent",
                        marker=dict(colors=colors),
                        opacity=self.opacity_spin.value()
                    )
                )
            elif graph_type == "Histograma":
                fig.add_trace(
                    go.Histogram(
                        x=data.iloc[:, 0],
                        nbinsx=self.nbins_spin.value(),
                        name=legend_texts[0] if legend_texts else "Histograma",
                        marker=dict(
                            color=colors[0] if colors else "blue",
                            opacity=self.opacity_spin.value()
                        )
                    )
                )
            elif graph_type == "Violino":
                for i, col in enumerate(data.columns[1:len(colors) + 1]):
                    fig.add_trace(
                        go.Violin(
                            y=data[col],
                            name=legend_texts[i],
                            box_visible=self.show_box_check.isChecked(),
                            line_color=colors[i % len(colors)],
                            opacity=self.opacity_spin.value()
                        )
                    )
            elif graph_type == "Caixa":
                for i, col in enumerate(data.columns[1:len(colors) + 1]):
                    fig.add_trace(
                        go.Box(
                            y=data[col],
                            name=legend_texts[i],
                            marker_color=colors[i % len(colors)],
                            opacity=self.opacity_spin.value()
                        )
                    )
            elif graph_type == "Dispersão 3D":
                if len(data.columns) >= 3:
                    fig.add_trace(
                        go.Scatter3d(
                            x=data.iloc[:, 0],
                            y=data.iloc[:, 1],
                            z=data.iloc[:, 2],
                            mode='markers',
                            name=legend_texts[0] if legend_texts else "Dispersão 3D",
                            marker=dict(
                                size=self.marker_size_spin.value(),
                                color=colors[0] if colors else "blue",
                                opacity=self.opacity_spin.value()
                            )
                        )
                    )
            elif graph_type == "Bolhas":
                if len(data.columns) >= 3:
                    # Normalizar os valores da terceira coluna para tamanhos de bolha entre 10 e 50
                    sizes = data.iloc[:, 2]
                    min_size = 10
                    max_size = 50
                    normalized_sizes = min_size + (sizes - sizes.min()) * (max_size - min_size) / (sizes.max() - sizes.min())
                    
                    fig.add_trace(
                        go.Scatter(
                            x=data.iloc[:, 0],
                            y=data.iloc[:, 1],
                            mode='markers',
                            name=legend_texts[0] if legend_texts else "Bolhas",
                            marker=dict(
                                size=normalized_sizes,
                                color=colors[0] if colors else "blue",
                                opacity=self.opacity_spin.value(),
                                sizemode='diameter'
                            )
                        )
                    )
            elif graph_type == "Radar":
                fig.add_trace(
                    go.Scatterpolar(
                        r=data.iloc[:, 1],
                        theta=data.iloc[:, 0],
                        fill='toself',
                        line=dict(color=colors[0] if colors else "blue"),
                        opacity=self.opacity_spin.value()
                    )
                )
            elif graph_type == "Heatmap":
                if len(data.columns) > 1:
                    fig.add_trace(
                        go.Heatmap(
                            z=data.iloc[:, 1:].values.T,  # Transpor a matriz para orientação correta
                            x=data.iloc[:, 0],  # Valores do eixo X
                            y=data.columns[1:],  # Nomes das colunas para eixo Y
                            colorscale=self.colorscale_combo.currentText(),
                            opacity=self.opacity_spin.value(),
                            name=legend_texts[0] if legend_texts else "Heatmap"
                        )
                    )

            # Renderiza o gráfico na área de visualização
            html_content = fig.to_html(include_plotlyjs="cdn")
            self.graph_view.setHtml(html_content)

        except Exception as e:
            self.file_button.setText(f"Erro ao gerar gráfico: {str(e)}")

    def apply_custom_style(self, style_name):
        if style_name == "clean_axes":
            return dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor='black',
                linewidth=1,
                ticks='outside'
            )
        elif style_name == "minimal_grid":
            return dict(
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.5,
                zeroline=False,
                showline=True,
                linecolor='black',
                linewidth=1
            )
        elif style_name == "publication":
            return dict(
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.5,
                zeroline=True,
                zerolinecolor='black',
                zerolinewidth=1,
                showline=True,
                linecolor='black',
                linewidth=1,
                ticks='outside',
                ticklen=5,
                tickwidth=1
            )
        # ... outros estilos personalizados ...

    def update_specific_params(self):
        # Configurações específicas para cada tipo de gráfico
        graph_type = self.graph_type_combo.currentText()
        
        # Dicionário com os parâmetros para cada tipo de gráfico
        params_config = {
            "Pontos": [
                ("Tamanho dos Marcadores:", self.marker_size_spin),
                ("Opacidade:", self.opacity_spin)
            ],
            "Linhas": [
                ("Espessura da Linha:", self.line_width_spin),
                ("Estilo da Linha:", self.line_style_combo),
                ("Opacidade:", self.opacity_spin)
            ],
            "Barras": [
                ("Largura das Barras:", self.bar_width_spin),
                ("Opacidade:", self.opacity_spin)
            ],
            "Barras Empilhadas": [
                ("Largura das Barras:", self.bar_width_spin),
                ("Opacidade:", self.opacity_spin)
            ],
            "Área": [
                ("Espessura da Linha:", self.line_width_spin),
                ("Opacidade:", self.opacity_spin)
            ],
            "Área Empilhada": [
                ("Espessura da Linha:", self.line_width_spin),
                ("Opacidade:", self.opacity_spin)
            ],
            "Setores": [
                ("Opacidade:", self.opacity_spin)
            ],
            "Rosca": [
                ("Tamanho do Furo:", self.hole_size_spin),
                ("Opacidade:", self.opacity_spin)
            ],
            "Histograma": [
                ("Número de Bins:", self.nbins_spin),
                ("Opacidade:", self.opacity_spin)
            ],
            "Violino": [
                ("", self.show_box_check),
                ("Opacidade:", self.opacity_spin)
            ],
            "Heatmap": [
                ("Escala de Cores:", self.colorscale_combo),
                ("Opacidade:", self.opacity_spin)
            ]
        }

        # Limpar layout atual
        while self.specific_params_layout.count():
            item = self.specific_params_layout.takeAt(0)
            if item.widget():
                item.widget().hide()

        # Adicionar parâmetros específicos
        if graph_type in params_config:
            for row, (label_text, widget) in enumerate(params_config[graph_type]):
                if label_text:  # Se houver texto de label
                    self.specific_params_layout.addWidget(QLabel(label_text), row, 0)
                self.specific_params_layout.addWidget(widget, row, 1)
                widget.show()

        self.update_graph()

class TextConfigDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        
        # Text input
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("Texto:"))
        self.text_input = QLineEdit()
        text_layout.addWidget(self.text_input)
        layout.addLayout(text_layout)
        
        # Font selection
        font_layout = QHBoxLayout()
        self.font_button = QPushButton("Selecionar Fonte")
        self.font_button.clicked.connect(self.select_font)
        font_layout.addWidget(self.font_button)
        layout.addLayout(font_layout)
        
        # Alignment selection
        align_layout = QHBoxLayout()
        align_layout.addWidget(QLabel("Alinhamento:"))
        self.alignment_combo = QComboBox()
        self.alignment_combo.addItems(["left", "center", "right"])
        align_layout.addWidget(self.alignment_combo)
        layout.addLayout(align_layout)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.font = QFont()
    
    def select_font(self):
        font, ok = QFontDialog.getFont(self.font, self)
        if ok:
            self.font = font
    
    def accept(self):
        self.text = self.text_input.text()
        self.alignment = self.alignment_combo.currentText()
        super().accept()

class AxisConfigDialog(TextConfigDialog):
    def __init__(self, title, axis_type, parent=None):
        super().__init__(title, parent)
        
        # Add scientific notation checkbox
        scientific_layout = QHBoxLayout()
        self.scientific_checkbox = QCheckBox("Notação Científica")
        scientific_layout.addWidget(self.scientific_checkbox)
        self.layout().insertLayout(2, scientific_layout)
    
    def accept(self):
        super().accept()
        self.scientific = self.scientific_checkbox.isChecked()

# Add this at the end of the file, after the GraphApp class
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = GraphApp()
    window.show()
    sys.exit(app.exec_())
