import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog, QLineEdit, QSpinBox, QListWidget, QColorDialog, QCheckBox, QFontDialog, QScrollArea, QGridLayout, QInputDialog)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import plotly.graph_objects as go
from PyQt5.QtWebEngineWidgets import QWebEngineView


class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráfico Personalizado")
        self.setGeometry(100, 100, 1200, 800)

        # Layout principal
        main_layout = QHBoxLayout()

        # Área de rolagem para os parâmetros
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        # Layout para os parâmetros
        param_layout = QVBoxLayout()

        # Upload do arquivo
        self.file_label = QLabel("Arquivo de dados:")
        self.file_button = QPushButton("Upload")
        self.file_button.clicked.connect(self.upload_file)
        self.file_path = None
        param_layout.addWidget(self.file_label)
        param_layout.addWidget(self.file_button)

        # Seleção do tipo de gráfico
        self.graph_type_label = QLabel("Tipo de gráfico:")
        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems(["Pontos", "Linhas", "Barras", "Setores", "Histograma"])
        self.graph_type_combo.currentTextChanged.connect(self.update_graph)
        param_layout.addWidget(self.graph_type_label)
        param_layout.addWidget(self.graph_type_combo)

        # Paleta de cores, símbolos e legendas
        self.color_label = QLabel("Cores (Hex), Símbolos e Legendas:")
        color_layout = QHBoxLayout()
        self.color_list = QListWidget()
        self.symbol_list = QListWidget()
        self.legend_list = QListWidget()
        self.color_list.setMaximumWidth(100)
        self.symbol_list.setMaximumWidth(100)
        self.legend_list.setMaximumWidth(150)
        color_buttons_layout = QVBoxLayout()
        self.add_color_button = QPushButton("Adicionar Cor, Símbolo e Legenda")
        self.add_color_button.clicked.connect(self.add_color_and_symbol)
        self.remove_color_button = QPushButton("Remover Seleção")
        self.remove_color_button.clicked.connect(self.remove_color_and_symbol)
        color_buttons_layout.addWidget(self.add_color_button)
        color_buttons_layout.addWidget(self.remove_color_button)
        color_layout.addWidget(self.color_list)
        color_layout.addWidget(self.symbol_list)
        color_layout.addWidget(self.legend_list)
        color_layout.addLayout(color_buttons_layout)
        param_layout.addWidget(self.color_label)
        param_layout.addLayout(color_layout)

        # Títulos dos eixos e da legenda
        self.title_label = QLabel("Título do gráfico:")
        self.title_input = QLineEdit()
        self.title_input.textChanged.connect(self.update_graph)
        param_layout.addWidget(self.title_label)
        param_layout.addWidget(self.title_input)

        self.xlabel_label = QLabel("Título do eixo X:")
        self.xlabel_input = QLineEdit()
        self.xlabel_input.textChanged.connect(self.update_graph)
        param_layout.addWidget(self.xlabel_label)
        param_layout.addWidget(self.xlabel_input)

        self.ylabel_label = QLabel("Título do eixo Y:")
        self.ylabel_input = QLineEdit()
        self.ylabel_input.textChanged.connect(self.update_graph)
        param_layout.addWidget(self.ylabel_label)
        param_layout.addWidget(self.ylabel_input)

        self.legend_title_label = QLabel("Título da legenda:")
        self.legend_title_input = QLineEdit()
        self.legend_title_input.textChanged.connect(self.update_graph)
        param_layout.addWidget(self.legend_title_label)
        param_layout.addWidget(self.legend_title_input)

        # Configuração de limites
        self.limits_label = QLabel("Limites dos eixos:")
        limits_layout = QGridLayout()
        self.xmin_label = QLabel("Xmin:")
        self.xmin_input = QLineEdit()
        self.xmin_input.textChanged.connect(self.update_graph)
        self.xmax_label = QLabel("Xmax:")
        self.xmax_input = QLineEdit()
        self.xmax_input.textChanged.connect(self.update_graph)
        self.ymin_label = QLabel("Ymin:")
        self.ymin_input = QLineEdit()
        self.ymin_input.textChanged.connect(self.update_graph)
        self.ymax_label = QLabel("Ymax:")
        self.ymax_input = QLineEdit()
        self.ymax_input.textChanged.connect(self.update_graph)
        limits_layout.addWidget(self.xmin_label, 0, 0)
        limits_layout.addWidget(self.xmin_input, 1, 0)
        limits_layout.addWidget(self.xmax_label, 0, 1)
        limits_layout.addWidget(self.xmax_input, 1, 1)
        limits_layout.addWidget(self.ymin_label, 0, 2)
        limits_layout.addWidget(self.ymin_input, 1, 2)
        limits_layout.addWidget(self.ymax_label, 0, 3)
        limits_layout.addWidget(self.ymax_input, 1, 3)
        param_layout.addWidget(self.limits_label)
        param_layout.addLayout(limits_layout)

        # Notação científica e barras de erro
        self.scientific_notation_label = QLabel("Notação Científica:")
        self.x_scientific_checkbox = QCheckBox("Eixo X")
        self.x_scientific_checkbox.stateChanged.connect(self.update_graph)
        self.y_scientific_checkbox = QCheckBox("Eixo Y")
        self.y_scientific_checkbox.stateChanged.connect(self.update_graph)
        self.error_bar_checkbox = QCheckBox("Mostrar Barras de Erro")
        self.error_bar_checkbox.stateChanged.connect(self.update_graph)
        param_layout.addWidget(self.scientific_notation_label)
        param_layout.addWidget(self.x_scientific_checkbox)
        param_layout.addWidget(self.y_scientific_checkbox)
        param_layout.addWidget(self.error_bar_checkbox)

        # Configurações gerais do gráfico
        self.graph_settings_label = QLabel("Configurações do Gráfico:")
        self.show_grid_checkbox = QCheckBox("Mostrar Grid")
        self.show_grid_checkbox.setChecked(True)
        self.show_grid_checkbox.stateChanged.connect(self.update_graph)
        self.show_axes_checkbox = QCheckBox("Mostrar Eixos")
        self.show_axes_checkbox.setChecked(True)
        self.show_axes_checkbox.stateChanged.connect(self.update_graph)
        param_layout.addWidget(self.graph_settings_label)
        param_layout.addWidget(self.show_grid_checkbox)
        param_layout.addWidget(self.show_axes_checkbox)

        # Fonte e tamanho de textos
        self.font_settings_label = QLabel("Fonte e Tamanho:")
        self.numbers_font_button = QPushButton("Fonte, Tamanho e Alinhamento dos Números")
        self.numbers_font_button.clicked.connect(self.set_numbers_font)
        self.legend_font_button = QPushButton("Fonte, Tamanho e Alinhamento da Legenda")
        self.legend_font_button.clicked.connect(self.set_legend_font)
        param_layout.addWidget(self.font_settings_label)
        param_layout.addWidget(self.numbers_font_button)
        param_layout.addWidget(self.legend_font_button)

        # Botões de formatação
        self.format_title_button = QPushButton("Formatar Título")
        self.format_title_button.clicked.connect(self.format_title)
        param_layout.addWidget(self.format_title_button)

        self.format_graph_button = QPushButton("Formatar Gráfico")
        self.format_graph_button.clicked.connect(self.format_graph)
        param_layout.addWidget(self.format_graph_button)

        # Estilo do gráfico
        self.style_label = QLabel("Estilo do gráfico:")
        self.style_combo = QComboBox()
        self.style_combo.addItems([
            "plotly", "plotly_white", "ggplot2", "seaborn", "simple_white", 
            "presentation", "xgridoff", "ygridoff", "plotly_dark", "solar", "vapor", "urban"
        ])
        self.style_combo.currentTextChanged.connect(self.update_graph)
        param_layout.addWidget(self.style_label)
        param_layout.addWidget(self.style_combo)

        # Adiciona o layout dos parâmetros ao conteúdo da rolagem
        scroll_layout.addLayout(param_layout)

        # Área do gráfico
        self.graph_view = QWebEngineView()

        # Adiciona layouts à janela principal
        main_layout.addWidget(scroll_area, 1)
        main_layout.addWidget(self.graph_view, 2)
        self.setLayout(main_layout)

    # Métodos adicionais serão integrados abaixo...
    def add_color_and_symbol(self):
        color = QColorDialog.getColor()
        if color.isValid():
            symbol, ok = QInputDialog.getItem(
                self,
                "Selecionar Símbolo",
                "Escolha um símbolo para a cor:",
                ["circle", "square", "diamond", "cross", "x"],
                editable=False
            )
            if ok and symbol:
                legend_text, ok = QInputDialog.getText(self, "Editar Legenda", "Digite o texto da legenda:")
                if ok and legend_text:
                    self.color_list.addItem(color.name())
                    self.symbol_list.addItem(symbol)
                    self.legend_list.addItem(legend_text)
                    self.update_graph()

    def remove_color_and_symbol(self):
        selected_indices = self.color_list.selectedIndexes()
        if selected_indices:
            for index in selected_indices:
                self.color_list.takeItem(index.row())
                self.symbol_list.takeItem(index.row())
                self.legend_list.takeItem(index.row())
            self.update_graph()

    def format_title(self):
        font, ok = QFontDialog.getFont()
        if ok:
            alignment, ok_align = QInputDialog.getItem(
                self,
                "Alinhamento do Título",
                "Escolha o alinhamento:",
                ["left", "center", "right"],
                editable=False
            )
            if ok_align:
                self.graph_title_font = font
                self.graph_title_alignment = alignment
                self.update_graph()

    def format_graph(self):
        font, ok = QFontDialog.getFont()
        if ok:
            alignment, ok_align = QInputDialog.getItem(
                self,
                "Alinhamento Geral",
                "Escolha o alinhamento:",
                ["left", "center", "right"],
                editable=False
            )
            if ok_align:
                self.xlabel_font = font
                self.ylabel_font = font
                self.legend_font = font
                self.numbers_font = font
                self.general_alignment = alignment
                self.update_graph()

    def set_numbers_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            alignment, ok_align = QInputDialog.getItem(
                self,
                "Alinhamento dos Números",
                "Escolha o alinhamento:",
                ["left", "center", "right"],
                editable=False
            )
            if ok_align:
                self.numbers_font = font
                self.numbers_alignment = alignment
                self.update_graph()

    def set_legend_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            alignment, ok_align = QInputDialog.getItem(
                self,
                "Alinhamento da Legenda",
                "Escolha o alinhamento:",
                ["left", "center", "right"],
                editable=False
            )
            if ok_align:
                self.legend_font = font
                self.legend_alignment = alignment
                self.update_graph()

    def upload_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecione o arquivo de dados", "", "Arquivos CSV (*.csv);;Arquivos Excel (*.xlsx)", options=options)
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"Arquivo: {file_path.split('/')[-1]}")
            self.update_graph()

    def update_graph(self):
        if not self.file_path:
            self.file_label.setText("Por favor, envie um arquivo de dados!")
            return

        # Lê os dados
        if self.file_path.endswith(".csv"):
            data = pd.read_csv(self.file_path)
        elif self.file_path.endswith(".xlsx"):
            data = pd.read_excel(self.file_path)
        else:
            self.file_label.setText("Formato de arquivo não suportado!")
            return

        # Configurações do gráfico
        graph_type = self.graph_type_combo.currentText()
        colors = [self.color_list.item(i).text() for i in range(self.color_list.count())]
        symbols = [self.symbol_list.item(i).text() for i in range(self.symbol_list.count())]
        legend_texts = [self.legend_list.item(i).text() if i < self.legend_list.count() else f"Variável {i + 1}" for i in range(len(colors))]
        title = self.title_input.text()
        xlabel = self.xlabel_input.text()
        ylabel = self.ylabel_input.text()
        legend_title = self.legend_title_input.text()
        style = self.style_combo.currentText()

        try:
            fig = go.Figure()
            fig.update_layout(template=style)

            # Geração de gráficos
            if graph_type in ["Pontos", "Linhas", "Barras"]:
                for i, col in enumerate(data.columns[1:len(colors) + 1]):
                    trace_color = colors[i % len(colors)]
                    trace_symbol = symbols[i % len(symbols)] if symbols else "circle"
                    trace_name = legend_texts[i]
                    if graph_type == "Pontos":
                        fig.add_trace(go.Scatter(
                            x=data.iloc[:, 0],
                            y=data[col],
                            mode='markers',
                            name=trace_name,
                            marker=dict(
                                color=trace_color,
                                size=10,
                                symbol=trace_symbol
                            ),
                            error_y=dict(type='data', array=data[col] * 0.1) if self.error_bar_checkbox.isChecked() else None
                        ))
                    elif graph_type == "Linhas":
                        fig.add_trace(go.Scatter(x=data.iloc[:, 0], y=data[col], mode='lines', name=trace_name, line=dict(color=trace_color)))
                    elif graph_type == "Barras":
                        fig.add_trace(go.Bar(x=data.iloc[:, 0], y=data[col], name=trace_name, marker_color=trace_color))
            elif graph_type == "Setores":
                fig = go.Figure(data=[go.Pie(labels=data.iloc[:, 0], values=data.iloc[:, 1], textinfo='label+percent', hole=.3)])
            elif graph_type == "Histograma":
                fig.add_trace(go.Histogram(x=data.iloc[:, 0], marker_color=colors[0] if colors else "blue"))

            # Configurações de eixos
            x_min = float(self.xmin_input.text()) if self.xmin_input.text() else None
            x_max = float(self.xmax_input.text()) if self.xmax_input.text() else None
            y_min = float(self.ymin_input.text()) if self.ymin_input.text() else None
            y_max = float(self.ymax_input.text()) if self.ymax_input.text() else None

            axis_color = 'black' 
            x_tickformat = "0.2e" if self.x_scientific_checkbox.isChecked() else None
            y_tickformat = "0.2e" if self.y_scientific_checkbox.isChecked() else None

            # Configurações gerais do gráfico
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=self.graph_title_font.pointSize(), family=self.graph_title_font.family(), color='black') if hasattr(self, 'graph_title_font') else {},
                    x=0.5 if getattr(self, 'graph_title_alignment', 'center') == 'center' else (0 if self.graph_title_alignment == 'left' else 1)
                ),
                xaxis=dict(
                    title=dict(
                        text=xlabel,
                        font=dict(size=self.xlabel_font.pointSize(), family=self.xlabel_font.family()) if hasattr(self, 'xlabel_font') else None
                    ),
                    range=[x_min, x_max],
                    color=axis_color,
                    tickformat=x_tickformat
                ),
                yaxis=dict(
                    title=dict(
                        text=ylabel,
                        font=dict(size=self.ylabel_font.pointSize(), family=self.ylabel_font.family()) if hasattr(self, 'ylabel_font') else None
                    ),
                    range=[y_min, y_max],
                    color=axis_color,
                    tickformat=y_tickformat
                ),
                legend=dict(
                    title=dict(
                        text=legend_title,
                        font=dict(size=self.legend_font.pointSize(), family=self.legend_font.family()) if hasattr(self, 'legend_font') else None
                    ),
                    font=dict(size=self.legend_font.pointSize(), family=self.legend_font.family()) if hasattr(self, 'legend_font') else None
                ),
                showlegend=True if self.show_axes_checkbox.isChecked() else False
            )

            # Configurações de eixos
            x_min = float(self.xmin_input.text()) if self.xmin_input.text() else None
            x_max = float(self.xmax_input.text()) if self.xmax_input.text() else None
            y_min = float(self.ymin_input.text()) if self.ymin_input.text() else None
            y_max = float(self.ymax_input.text()) if self.ymax_input.text() else None

            axis_color = 'black' 
            x_tickformat = "0.2e" if self.x_scientific_checkbox.isChecked() else None
            y_tickformat = "0.2e" if self.y_scientific_checkbox.isChecked() else None

            # Configurações gerais do gráfico
            fig.update_layout(
                title=dict(
                    text=title,
                    font=dict(size=self.graph_title_font.pointSize(), family=self.graph_title_font.family(), color='black') if hasattr(self, 'graph_title_font') else {},
                    x=0.5 if getattr(self, 'graph_title_alignment', 'center') == 'center' else (0 if self.graph_title_alignment == 'left' else 1)
                ),
                xaxis=dict(
                    title=dict(
                        text=xlabel,
                        font=dict(size=self.xlabel_font.pointSize(), family=self.xlabel_font.family()) if hasattr(self, 'xlabel_font') else None
                    ),
                    range=[x_min, x_max],
                    color=axis_color,
                    tickformat=x_tickformat
                ),
                yaxis=dict(
                    title=dict(
                        text=ylabel,
                        font=dict(size=self.ylabel_font.pointSize(), family=self.ylabel_font.family()) if hasattr(self, 'ylabel_font') else None
                    ),
                    range=[y_min, y_max],
                    color=axis_color,
                    tickformat=y_tickformat
                ),
                legend=dict(
                    title=dict(
                        text=legend_title,
                        font=dict(size=self.legend_font.pointSize(), family=self.legend_font.family()) if hasattr(self, 'legend_font') else None
                    ),
                    font=dict(size=self.legend_font.pointSize(), family=self.legend_font.family()) if hasattr(self, 'legend_font') else None
                ),
                showlegend=True if self.show_axes_checkbox.isChecked() else False
            )

            if not self.show_grid_checkbox.isChecked():
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)

            # Renderiza o gráfico na área de visualização
            html_content = fig.to_html(include_plotlyjs='cdn')
            self.graph_view.setHtml(html_content)
        except Exception as e:
            self.file_label.setText(f"Erro ao gerar gráfico: {str(e)}")
