'''
В этом модуле есть последовательность анимаций реализованная без исчезновения
предыдущего изображения перед появляением следующего, скорей всего исчезновение буду
вставлять подходящим кадром в Clipchamp
'''

import sys
import chess
import chess.svg
from time import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QColor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QRectF, QPoint, Qt, QTimer


class ChessGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Самоучитель игры в классические шахматы")

        # Размер окна
        self.resize(900, 900)

        # Загрузка иконки
        try:
            self.setWindowIcon(QIcon("yus_small.ico"))
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")

        # Шахматная доска
        self.board = chess.Board("8/8/8/8/8/8/8/8 w - - 0 0")

        # Изображение доски в формате SVG
        svg_data = chess.svg.board(self.board, size=800, coordinates=True, borders=True)
        self.renderer = QSvgRenderer(svg_data.encode("utf-8"))
        
        # список значений параметра squares для chess.svg.board с выделенной вертикалью
        self.verticals = [
            chess.BB_FILE_A,
            chess.BB_FILE_B,
            chess.BB_FILE_C,
            chess.BB_FILE_D,
            chess.BB_FILE_E,
            chess.BB_FILE_F,
            chess.BB_FILE_G,
            chess.BB_FILE_H
        ]

        # список значений параметра squares для chess.svg.board с выделенной горизонталью
        self.horizontals = [
            chess.BB_RANK_1,
            chess.BB_RANK_2,
            chess.BB_RANK_3,
            chess.BB_RANK_4,
            chess.BB_RANK_5,
            chess.BB_RANK_6,
            chess.BB_RANK_7,
            chess.BB_RANK_8,
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением вертикали, горизонтали и самого поля для d4
        self.d4 = [
            chess.BB_FILE_D,
            chess.BB_FILE_D | chess.BB_RANK_4,
            chess.BB_D4
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением вертикали, горизонтали и самого поля для d5
        self.d5 = [
            chess.BB_FILE_D,
            chess.BB_FILE_D | chess.BB_RANK_5,
            chess.BB_D5
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением вертикали, горизонтали и самого поля для e5
        self.e5 = [
            chess.BB_FILE_E,
            chess.BB_FILE_E | chess.BB_RANK_5,
            chess.BB_E5
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением вертикали, горизонтали и самого поля для e4
        self.e4 = [
            chess.BB_FILE_E,
            chess.BB_FILE_E | chess.BB_RANK_4,
            chess.BB_E4
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением полей центра, начиная с d4
        self.center = [
            chess.BB_D4,
            chess.BB_D4 | chess.BB_D5,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4
        ]
        # список значений параметра squares для chess.svg.board с последовательным выделением полей расширенного центра, начиная с c3
        self.extended_center = [
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4 | chess.BB_C5,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4 | chess.BB_C5 | chess.BB_C6,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4 | chess.BB_C5 | chess.BB_C6 | chess.BB_D6,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4 | chess.BB_C5 | chess.BB_C6 | chess.BB_D6 | chess.BB_E6,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4 | chess.BB_C5 | chess.BB_C6 | chess.BB_D6 | chess.BB_E6 | chess.BB_F6,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4 | chess.BB_C5 | chess.BB_C6 | chess.BB_D6 | chess.BB_E6 | chess.BB_F6 | chess.BB_F5,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4 | chess.BB_C5 | chess.BB_C6 | chess.BB_D6 | chess.BB_E6 | chess.BB_F6 | chess.BB_F5 | chess.BB_F4,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4 | chess.BB_C5 | chess.BB_C6 | chess.BB_D6 | chess.BB_E6 | chess.BB_F6 | chess.BB_F5 | chess.BB_F4 | chess.BB_F3,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4 | chess.BB_C5 | chess.BB_C6 | chess.BB_D6 | chess.BB_E6 | chess.BB_F6 | chess.BB_F5 | chess.BB_F4 | chess.BB_F3 | chess.BB_E3,
            chess.BB_D4 | chess.BB_D5 | chess.BB_E5 |chess.BB_E4 | chess.BB_C3 | chess.BB_C4 | chess.BB_C5 | chess.BB_C6 | chess.BB_D6 | chess.BB_E6 | chess.BB_F6 | chess.BB_F5 | chess.BB_F4 | chess.BB_F3 | chess.BB_E3 |chess.BB_D3
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением 4 углов, начиная с a1
        self.corners = [
            chess.BB_A1,
            chess.BB_A1 | chess.BB_A8,
            chess.BB_A1 | chess.BB_A8 | chess.BB_H8,
            chess.BB_A1 | chess.BB_A8 | chess.BB_H8 | chess.BB_H1
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением 2 углов: с a1 и a8
        self.two_corners = [
            chess.BB_A1,
            chess.BB_A1 | chess.BB_A8
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением полей края доски, начиная с a2
        self.edge_v_a = [
            chess.BB_A2,
            chess.BB_A2 | chess.BB_A3,
            chess.BB_A2 | chess.BB_A3 | chess.BB_A4,
            chess.BB_A2 | chess.BB_A3 | chess.BB_A4 | chess.BB_A5,
            chess.BB_A2 | chess.BB_A3 | chess.BB_A4 | chess.BB_A5 | chess.BB_A6,
            chess.BB_A2 | chess.BB_A3 | chess.BB_A4 | chess.BB_A5 | chess.BB_A6 | chess.BB_A7
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением остальных краёв, начиная с края на 8 горизонтали
        self.other_edges = [
            chess.BB_RANK_8 - chess.BB_A8 - chess.BB_H8,
            chess.BB_FILE_H - chess.BB_H8 - chess.BB_H1,
            chess.BB_RANK_1 - chess.BB_H1 - chess.BB_A1
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением белых диагоналей
        self.white_diagonals = [
            chess.BB_G8 | chess.BB_H7,
            chess.BB_G8 | chess.BB_H7 | chess.BB_E8 | chess.BB_F7 | chess.BB_G6 | chess.BB_H5,
            chess.BB_G8 | chess.BB_H7 | chess.BB_E8 | chess.BB_F7 | chess.BB_G6 | chess.BB_H5 | chess.BB_C8 | chess.BB_D7 | chess.BB_E6 | chess.BB_F5 | chess.BB_G4 | chess.BB_H3,
            chess.BB_G8 | chess.BB_H7 | chess.BB_E8 | chess.BB_F7 | chess.BB_G6 | chess.BB_H5 | chess.BB_C8 | chess.BB_D7 | chess.BB_E6 | chess.BB_F5 | chess.BB_G4 | chess.BB_H3 | chess.BB_A8 | chess.BB_B7 | chess.BB_C6 | chess.BB_D5 | chess.BB_E4 | chess.BB_F3 | chess.BB_G2 | chess.BB_H1,
            chess.BB_G8 | chess.BB_H7 | chess.BB_E8 | chess.BB_F7 | chess.BB_G6 | chess.BB_H5 | chess.BB_C8 | chess.BB_D7 | chess.BB_E6 | chess.BB_F5 | chess.BB_G4 | chess.BB_H3 | chess.BB_A8 | chess.BB_B7 | chess.BB_C6 | chess.BB_D5 | chess.BB_E4 | chess.BB_F3 | chess.BB_G2 | chess.BB_H1 | chess.BB_A6 | chess.BB_B5 | chess.BB_C4 | chess.BB_D3 | chess.BB_E2 | chess.BB_F1,
            chess.BB_G8 | chess.BB_H7 | chess.BB_E8 | chess.BB_F7 | chess.BB_G6 | chess.BB_H5 | chess.BB_C8 | chess.BB_D7 | chess.BB_E6 | chess.BB_F5 | chess.BB_G4 | chess.BB_H3 | chess.BB_A8 | chess.BB_B7 | chess.BB_C6 | chess.BB_D5 | chess.BB_E4 | chess.BB_F3 | chess.BB_G2 | chess.BB_H1 | chess.BB_A6 | chess.BB_B5 | chess.BB_C4 | chess.BB_D3 | chess.BB_E2 | chess.BB_F1 | chess.BB_A4 | chess.BB_B3 | chess.BB_C2 | chess.BB_D1,
            chess.BB_G8 | chess.BB_H7 | chess.BB_E8 | chess.BB_F7 | chess.BB_G6 | chess.BB_H5 | chess.BB_C8 | chess.BB_D7 | chess.BB_E6 | chess.BB_F5 | chess.BB_G4 | chess.BB_H3 | chess.BB_A8 | chess.BB_B7 | chess.BB_C6 | chess.BB_D5 | chess.BB_E4 | chess.BB_F3 | chess.BB_G2 | chess.BB_H1 | chess.BB_A6 | chess.BB_B5 | chess.BB_C4 | chess.BB_D3 | chess.BB_E2 | chess.BB_F1 | chess.BB_A4 | chess.BB_B3 | chess.BB_C2 | chess.BB_D1 | chess.BB_A2 | chess.BB_B1,
            chess.BB_A6 | chess.BB_B7 | chess.BB_C8,
            chess.BB_A6 | chess.BB_B7 | chess.BB_C8 | chess.BB_A4 | chess.BB_B5 | chess.BB_C6 | chess.BB_D7 | chess.BB_E8,
            chess.BB_A6 | chess.BB_B7 | chess.BB_C8 | chess.BB_A4 | chess.BB_B5 | chess.BB_C6 | chess.BB_D7 | chess.BB_E8 | chess.BB_A2 | chess.BB_B3 | chess.BB_C4 | chess.BB_D5 | chess.BB_E6 | chess.BB_F7 | chess.BB_G8,
            chess.BB_A6 | chess.BB_B7 | chess.BB_C8 | chess.BB_A4 | chess.BB_B5 | chess.BB_C6 | chess.BB_D7 | chess.BB_E8 | chess.BB_A2 | chess.BB_B3 | chess.BB_C4 | chess.BB_D5 | chess.BB_E6 | chess.BB_F7 | chess.BB_G8 | chess.BB_B1 | chess.BB_C2 | chess.BB_D3 | chess.BB_E4 | chess.BB_F5 | chess.BB_G6 | chess.BB_H7,
            chess.BB_A6 | chess.BB_B7 | chess.BB_C8 | chess.BB_A4 | chess.BB_B5 | chess.BB_C6 | chess.BB_D7 | chess.BB_E8 | chess.BB_A2 | chess.BB_B3 | chess.BB_C4 | chess.BB_D5 | chess.BB_E6 | chess.BB_F7 | chess.BB_G8 | chess.BB_B1 | chess.BB_C2 | chess.BB_D3 | chess.BB_E4 | chess.BB_F5 | chess.BB_G6 | chess.BB_H7 | chess.BB_D1 | chess.BB_E2 | chess.BB_F3 | chess.BB_G4 | chess.BB_H5,
            chess.BB_A6 | chess.BB_B7 | chess.BB_C8 | chess.BB_A4 | chess.BB_B5 | chess.BB_C6 | chess.BB_D7 | chess.BB_E8 | chess.BB_A2 | chess.BB_B3 | chess.BB_C4 | chess.BB_D5 | chess.BB_E6 | chess.BB_F7 | chess.BB_G8 | chess.BB_B1 | chess.BB_C2 | chess.BB_D3 | chess.BB_E4 | chess.BB_F5 | chess.BB_G6 | chess.BB_H7 | chess.BB_D1 | chess.BB_E2 | chess.BB_F3 | chess.BB_G4 | chess.BB_H5 | chess.BB_F1 | chess.BB_G2 | chess.BB_H3,
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением чёрных диагоналей
        self.black_diagonals = [
            chess.BB_A7 | chess.BB_B8,
            chess.BB_A7 | chess.BB_B8 | chess.BB_A5 | chess.BB_B6 | chess.BB_C7 | chess.BB_D8,
            chess.BB_A7 | chess.BB_B8 | chess.BB_A5 | chess.BB_B6 | chess.BB_C7 | chess.BB_D8 | chess.BB_A3 | chess.BB_B4 | chess.BB_C5 | chess.BB_D6 | chess.BB_E7 | chess.BB_F8,
            chess.BB_A7 | chess.BB_B8 | chess.BB_A5 | chess.BB_B6 | chess.BB_C7 | chess.BB_D8 | chess.BB_A3 | chess.BB_B4 | chess.BB_C5 | chess.BB_D6 | chess.BB_E7 | chess.BB_F8 | chess.BB_A1 | chess.BB_B2 | chess.BB_C3 | chess.BB_D4 | chess.BB_E5 | chess.BB_F6 | chess.BB_G7 | chess.BB_H8,
            chess.BB_A7 | chess.BB_B8 | chess.BB_A5 | chess.BB_B6 | chess.BB_C7 | chess.BB_D8 | chess.BB_A3 | chess.BB_B4 | chess.BB_C5 | chess.BB_D6 | chess.BB_E7 | chess.BB_F8 | chess.BB_A1 | chess.BB_B2 | chess.BB_C3 | chess.BB_D4 | chess.BB_E5 | chess.BB_F6 | chess.BB_G7 | chess.BB_H8 | chess.BB_C1 | chess.BB_D2 | chess.BB_E3 | chess.BB_F4 | chess.BB_G5 | chess.BB_H6,
            chess.BB_A7 | chess.BB_B8 | chess.BB_A5 | chess.BB_B6 | chess.BB_C7 | chess.BB_D8 | chess.BB_A3 | chess.BB_B4 | chess.BB_C5 | chess.BB_D6 | chess.BB_E7 | chess.BB_F8 | chess.BB_A1 | chess.BB_B2 | chess.BB_C3 | chess.BB_D4 | chess.BB_E5 | chess.BB_F6 | chess.BB_G7 | chess.BB_H8 | chess.BB_C1 | chess.BB_D2 | chess.BB_E3 | chess.BB_F4 | chess.BB_G5 | chess.BB_H6 | chess.BB_E1 | chess.BB_F2 | chess.BB_G3 | chess.BB_H4,
            chess.BB_A7 | chess.BB_B8 | chess.BB_A5 | chess.BB_B6 | chess.BB_C7 | chess.BB_D8 | chess.BB_A3 | chess.BB_B4 | chess.BB_C5 | chess.BB_D6 | chess.BB_E7 | chess.BB_F8 | chess.BB_A1 | chess.BB_B2 | chess.BB_C3 | chess.BB_D4 | chess.BB_E5 | chess.BB_F6 | chess.BB_G7 | chess.BB_H8 | chess.BB_C1 | chess.BB_D2 | chess.BB_E3 | chess.BB_F4 | chess.BB_G5 | chess.BB_H6 | chess.BB_E1 | chess.BB_F2 | chess.BB_G3 | chess.BB_H4 | chess.BB_G1 | chess.BB_H2,
            chess.BB_F8 | chess.BB_G7 | chess.BB_H6,
            chess.BB_F8 | chess.BB_G7 | chess.BB_H6 | chess.BB_D8 | chess.BB_E7 | chess.BB_F6 | chess.BB_G5 | chess.BB_H4,
            chess.BB_F8 | chess.BB_G7 | chess.BB_H6 | chess.BB_D8 | chess.BB_E7 | chess.BB_F6 | chess.BB_G5 | chess.BB_H4 | chess.BB_B8 | chess.BB_C7 | chess.BB_D6 | chess.BB_E5 | chess.BB_F4 | chess.BB_G3 | chess.BB_H2,
            chess.BB_F8 | chess.BB_G7 | chess.BB_H6 | chess.BB_D8 | chess.BB_E7 | chess.BB_F6 | chess.BB_G5 | chess.BB_H4 | chess.BB_B8 | chess.BB_C7 | chess.BB_D6 | chess.BB_E5 | chess.BB_F4 | chess.BB_G3 | chess.BB_H2 | chess.BB_A7 | chess.BB_B6 | chess.BB_C5 | chess.BB_D4 | chess.BB_E3 | chess.BB_F2 | chess.BB_G1,
            chess.BB_F8 | chess.BB_G7 | chess.BB_H6 | chess.BB_D8 | chess.BB_E7 | chess.BB_F6 | chess.BB_G5 | chess.BB_H4 | chess.BB_B8 | chess.BB_C7 | chess.BB_D6 | chess.BB_E5 | chess.BB_F4 | chess.BB_G3 | chess.BB_H2 | chess.BB_A7 | chess.BB_B6 | chess.BB_C5 | chess.BB_D4 | chess.BB_E3 | chess.BB_F2 | chess.BB_G1 | chess.BB_A5 | chess.BB_B4 | chess.BB_C3 | chess.BB_D2 | chess.BB_E1,
            chess.BB_F8 | chess.BB_G7 | chess.BB_H6 | chess.BB_D8 | chess.BB_E7 | chess.BB_F6 | chess.BB_G5 | chess.BB_H4 | chess.BB_B8 | chess.BB_C7 | chess.BB_D6 | chess.BB_E5 | chess.BB_F4 | chess.BB_G3 | chess.BB_H2 | chess.BB_A7 | chess.BB_B6 | chess.BB_C5 | chess.BB_D4 | chess.BB_E3 | chess.BB_F2 | chess.BB_G1 | chess.BB_A5 | chess.BB_B4 | chess.BB_C3 | chess.BB_D2 | chess.BB_E1 | chess.BB_A3 | chess.BB_B2 | chess.BB_C1,
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением большой белой и большой чёрной диагоналей
        self.big_diagonals = [
            chess.BB_A8 | chess.BB_B7 | chess.BB_C6 | chess.BB_D5 | chess.BB_E4 | chess.BB_F3 | chess.BB_G2 | chess.BB_H1,
            chess.BB_A8 | chess.BB_B7 | chess.BB_C6 | chess.BB_D5 | chess.BB_E4 | chess.BB_F3 | chess.BB_G2 | chess.BB_H1 | chess.BB_A1 | chess.BB_B2 | chess.BB_C3 | chess.BB_D4 | chess.BB_E5 | chess.BB_F6 | chess.BB_G7 | chess.BB_H8
        ]

        # список значений параметра squares для chess.svg.board с последовательным выделением двух диагоналей из последнего примера
        self.two_diagonals = [
            chess.BB_E8 | chess.BB_F7 | chess.BB_G6 | chess.BB_H5,
            chess.BB_E8 | chess.BB_D7 | chess.BB_C6 | chess.BB_B5 | chess.BB_A4
        ]

        # Создаем массив рендеров для каждой вертикали
        self.vertical_renderers = []
        for v in self.verticals:
            svg_vertical = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=v)
            renderer = QSvgRenderer(svg_vertical.encode('utf-8'))
            self.vertical_renderers.append(renderer)

        # Создаем массив рендеров для каждой горизонтали
        self.horizontal_renderers = []
        for h in self.horizontals:
            svg_horizontal = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=h)
            renderer = QSvgRenderer(svg_horizontal.encode('utf-8'))
            self.horizontal_renderers.append(renderer)
        
        # Создаем массив рендеров для d4
        self.d4_renderers = []
        for sq in self.d4:
            svg_d4 = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=sq)
            renderer = QSvgRenderer(svg_d4.encode('utf-8'))
            self.d4_renderers.append(renderer)

        # Создаем массив рендеров для d5
        self.d5_renderers = []
        for sq in self.d5:
            svg_d5 = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=sq)
            renderer = QSvgRenderer(svg_d5.encode('utf-8'))
            self.d5_renderers.append(renderer)

        # Создаем массив рендеров для e5
        self.e5_renderers = []
        for sq in self.e5:
            svg_e5 = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=sq)
            renderer = QSvgRenderer(svg_e5.encode('utf-8'))
            self.e5_renderers.append(renderer)
        
        # Создаем массив рендеров для e4
        self.e4_renderers = []
        for sq in self.e4:
            svg_e4 = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=sq)
            renderer = QSvgRenderer(svg_e4.encode('utf-8'))
            self.e4_renderers.append(renderer)

        # Создаем массив рендеров для полей центра
        self.center_renderers = []
        for c_sq in self.center:
            svg_center = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=c_sq)
            renderer = QSvgRenderer(svg_center.encode('utf-8'))
            self.center_renderers.append(renderer)

        # Создаем массив рендеров для полей расширенного центра
        self.extended_center_renderers = []
        for ex_c_sq in self.extended_center:
            svg_extended_center = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=ex_c_sq)
            renderer = QSvgRenderer(svg_extended_center.encode('utf-8'))
            self.extended_center_renderers.append(renderer)

         # Создаем массив рендеров для 4 углов
        self.corners_renderers = []
        for c in self.corners:
            svg_corners = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=c)
            renderer = QSvgRenderer(svg_corners.encode('utf-8'))
            self.corners_renderers.append(renderer)

         # Создаем массив рендеров для 2 углов
        self.two_corners_renderers = []
        for c in self.two_corners:
            svg_two_corners = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=c)
            renderer = QSvgRenderer(svg_two_corners.encode('utf-8'))
            self.two_corners_renderers.append(renderer)

        # Создаем массив рендеров для полей края доски на вертикали a
        self.edge_v_a_renderers = []
        for sq in self.edge_v_a:
            svg_edge_v_a = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=sq)
            renderer = QSvgRenderer(svg_edge_v_a.encode('utf-8'))
            self.edge_v_a_renderers.append(renderer)

        # Создаем массив рендеров для остальных краёв
        self.other_edges_renderers = []
        for e in self.other_edges:
            svg_other_edges = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=e)
            renderer = QSvgRenderer(svg_other_edges.encode('utf-8'))
            self.other_edges_renderers.append(renderer)

        # Создаем массив рендеров для белых диагоналей
        self.white_diagonals_renderers = []
        for c in self.white_diagonals:
            svg_white_diagonals = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=c)
            renderer = QSvgRenderer(svg_white_diagonals.encode('utf-8'))
            self.white_diagonals_renderers.append(renderer)

        # Создаем массив рендеров для чёрных диагоналей
        self.black_diagonals_renderers = []
        for c in self.black_diagonals:
            svg_black_diagonals = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=c)
            renderer = QSvgRenderer(svg_black_diagonals.encode('utf-8'))
            self.black_diagonals_renderers.append(renderer)

        # Создаем массив рендеров для больших диагоналей
        self.big_diagonals_renderers = []
        for c in self.big_diagonals:
            svg_big_diagonals = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=c)
            renderer = QSvgRenderer(svg_big_diagonals.encode('utf-8'))
            self.big_diagonals_renderers.append(renderer)

        # Создаем массив рендеров для двух диагоналей из примера
        self.two_diagonals_renderers = []
        for c in self.two_diagonals:
            svg_two_diagonals = chess.svg.board(self.board, size=800, coordinates=True, borders=True, squares=c)
            renderer = QSvgRenderer(svg_two_diagonals.encode('utf-8'))
            self.two_diagonals_renderers.append(renderer)

        # Начальные индексы для стрелок
        self.current_down_arrow_index = 0
        self.current_left_arrow_index = 0

        # Начальные индексы для выделений вертикалей и горизонталей
        self.verticals_index = 0
        self.horizontals_index = 0

        # Индексы текущего элемента из вертикали, горизонтали и общего поля
        self.d4_index = 0
        self.d5_index = 0
        self.e5_index = 0
        self.e4_index = 0

        # Начальные индексы для выделений центра и расширенного центра
        self.center_index = 0
        self.extended_center_index = 0

        # Индексы текущего значения для 4 углов, 2 углов, края между 2 углами и остальных 3 краёв
        self.corners_index = 0
        self.two_corners_index = 0
        self.edge_v_a_index = 0
        self.other_edges_index = 0

         # Индексы текущего значения для белых диагоналей
        self.white_diagonals_index = 0
        
        # Индексы текущего значения для чёрных диагоналей
        self.black_diagonals_index = 0

        # Индексы текущего значения для больших диагоналей
        self.big_diagonals_index = 0

        # Индексы текущего значения для двух диагоналей из примера
        self.two_diagonals_index = 0

        # Состояния стрелок (True - стрелка видима, False - скрыта)
        self.down_arrows_visible = [False] * 8  # Стрелки «вниз»
        self.left_arrows_visible = [False] * 8  # Стрелки «влево»

        # Состояния выделения для вертикалей и горизонталей (True - выделение видимо, False - скрыто)
        self.verticals_visible = [False] * 8
        self.horizontals_visible = [False] * 8
        
        # Состояния вертикали, горизонтали и общего поля
        self.d4_visible = [False] * 3
        self.d5_visible = [False] * 3
        self.e5_visible = [False] * 3
        self.e4_visible = [False] * 3

        # Состояния выделения для центра и расширенного центра (True - выделение видимо, False - скрыто)
        self.center_visible = [False] * 4
        self.extended_center_visible = [False] * 12

        # Состояния 4 углов, 2 углов, края между 2 углами и остальных 3 краёв
        self.corners_visible = [False] * 4
        self.two_corners_visible = [False] * 2
        self.edge_v_a_visible = [False] * 6
        self.other_edges_visible = [False] * 3

        # Состояния белых диагоналей
        self.white_diagonals_visible = [False] * 13

        # Состояния черных диагоналей
        self.black_diagonals_visible = [False] * 13

        # Состояния больших диагоналей
        self.big_diagonals_visible = [False] * 2

        # Состояния двух диагоналей из примера
        self.two_diagonals_visible = [False] * 2
        
        self.animation_count = 0  # Инициализация счетчика
        # Таймер для анимации
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(2000)  # Интервал 2 секунды
        self.pause = 10 # пауза между анимациями, количество шагов

    def update_animation(self):
        """Обновляет состояние объектов."""
        # общее количество шагов всех анимаций
        total_steps = sum((
            2 * len(self.down_arrows_visible),
            2 * len(self.left_arrows_visible),
            2 * len(self.verticals_visible),
            2 * len(self.horizontals_visible),
            (len(self.d4_visible) + 1),
            (len(self.d5_visible) + 1),
            (len(self.e5_visible) + 1),
            (len(self.e4_visible) + 1),
            len(self.center_visible),
            len(self.extended_center_visible),
            len(self.corners_visible),
            len(self.two_corners_visible),
            len(self.edge_v_a_visible),
            len(self.other_edges_visible),
            len(self.white_diagonals_visible),
            len(self.black_diagonals_visible),
            len(self.big_diagonals_visible),
            len(self.two_diagonals_visible)
        )) + len((self.down_arrows_visible,
                  self.left_arrows_visible,
                  self.verticals_visible,
                  self.horizontals_visible,
                  self.d4_visible, self.d5_visible,
                  self.e5_visible, self.e4_visible,
                  self.center_visible,
                  self.extended_center_visible,
                  self.corners_visible,
                  self.two_corners_visible,
                  self.edge_v_a_visible,
                  self.other_edges_visible,
                  self.white_diagonals_visible,
                  self.black_diagonals_visible,
                  self.big_diagonals_visible,
                  self.two_diagonals_visible)) * self.pause
       
        if self.animation_count <= total_steps:
            # Используем одно единственное условие для контроля прогресса анимации
            if self.animation_count <= self.pause:
                pass  # Пауза в самом начале
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible):
                # Анимация стрелок «вниз»
                if not self.down_arrows_visible[self.current_down_arrow_index]:
                    self.down_arrows_visible[self.current_down_arrow_index] = True
                else:
                    self.down_arrows_visible[self.current_down_arrow_index] = False
                    self.current_down_arrow_index += 1
                    if self.current_down_arrow_index >= len(self.down_arrows_visible):
                        self.current_down_arrow_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible):
                # Анимация вертикалей
                if not self.verticals_visible[self.verticals_index]:
                    self.verticals_visible[self.verticals_index] = True
                else:
                    self.verticals_visible[self.verticals_index] = False
                    self.verticals_index += 1
                    if self.verticals_index >= len(self.verticals_visible):
                        self.verticals_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible):
                # Анимация стрелок «влево»
                if not self.left_arrows_visible[self.current_left_arrow_index]:
                    self.left_arrows_visible[self.current_left_arrow_index] = True
                else:
                    self.left_arrows_visible[self.current_left_arrow_index] = False
                    self.current_left_arrow_index += 1
                    if self.current_left_arrow_index >= len(self.left_arrows_visible):
                        self.current_left_arrow_index = 0            
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible):
                # Анимация горизонталей
                if not self.horizontals_visible[self.horizontals_index]:
                    self.horizontals_visible[self.horizontals_index] = True
                else:
                    self.horizontals_visible[self.horizontals_index] = False
                    self.horizontals_index += 1
                    if self.horizontals_index >= len(self.horizontals_visible):
                        self.horizontals_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1):
                # Анимация для d4
                if not self.d4_visible[self.d4_index]:
                    if self.d4_index < 2:
                       self.d4_visible[self.d4_index] = True
                       self.d4_index += 1
                    else:
                        self.d4_visible = [False, False, True]
                else:
                    self.d4_visible[self.d4_index] = False
                    if self.d4_index >= len(self.d4_visible):
                        self.d4_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1):
                # Анимация для d5
                if not self.d5_visible[self.d5_index]:
                    if self.d5_index < 2:
                       self.d5_visible[self.d5_index] = True
                       self.d5_index += 1
                    else:
                        self.d5_visible = [False, False, True]
                else:
                    self.d5_visible[self.d5_index] = False
                    if self.d5_index >= len(self.d5_visible):
                        self.d5_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1):
                # Анимация для e5
                if not self.e5_visible[self.e5_index]:
                    if self.e5_index < 2:
                       self.e5_visible[self.e5_index] = True
                       self.e5_index += 1
                    else:
                        self.e5_visible = [False, False, True]
                else:
                    self.e5_visible[self.e5_index] = False
                    if self.e5_index >= len(self.e5_visible):
                        self.e5_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1):
                # Анимация для e4
                if not self.e4_visible[self.e4_index]:
                    if self.e4_index < 2:
                       self.e4_visible[self.e4_index] = True
                       self.e4_index += 1
                    else:
                        self.e4_visible = [False, False, True]
                else:
                    self.e4_visible[self.e4_index] = False
                    if self.e4_index >= len(self.e4_visible):
                        self.e4_index = 0            
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1) + len(self.center_visible):
                # Анимация центра
                if not self.center_visible[self.center_index]:
                    self.center_visible[self.center_index] = True
                    self.center_index += 1
                    if self.center_index >= len(self.center_visible):
                        self.center_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1) + len(self.center_visible) + len(self.extended_center_visible):
                # Анимация расширенного центра
                if not self.extended_center_visible[self.extended_center_index]:
                    self.extended_center_visible[self.extended_center_index] = True
                    self.extended_center_index += 1
                    if self.extended_center_index >= len(self.extended_center_visible):
                        self.extended_center_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1) + len(self.center_visible) + len(self.extended_center_visible) + len(self.corners_visible):
                # Анимация 4 углов
                if not self.corners_visible[self.corners_index]:
                    self.corners_visible[self.corners_index] = True
                    self.corners_index += 1
                    if self.corners_index >= len(self.corners_visible):
                        self.corners_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1) + len(self.center_visible) + len(self.extended_center_visible) + len(self.corners_visible) + len(self.two_corners_visible):
                # Анимация 2 углов
                if not self.two_corners_visible[self.two_corners_index]:
                    self.two_corners_visible[self.two_corners_index] = True
                    self.two_corners_index += 1
                    if self.two_corners_index >= len(self.two_corners_visible):
                        self.two_corners_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1) + len(self.center_visible) + len(self.extended_center_visible) + len(self.corners_visible) + len(self.two_corners_visible) + len(self.edge_v_a_visible):
                # Анимация края на вертикали a
                if not self.edge_v_a_visible[self.edge_v_a_index]:
                    self.edge_v_a_visible[self.edge_v_a_index] = True
                    self.edge_v_a_index += 1
                    if self.edge_v_a_index >= len(self.edge_v_a_visible):
                        self.edge_v_a_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1) + len(self.center_visible) + len(self.extended_center_visible) + len(self.corners_visible) + len(self.two_corners_visible) + len(self.edge_v_a_visible) + len(self.other_edges_visible):
                # Анимация остальных краёв
                if not self.other_edges_visible[self.other_edges_index]:
                    self.other_edges_visible[self.other_edges_index] = True
                    self.other_edges_index += 1
                    if self.other_edges_index >= len(self.other_edges_visible):
                        self.other_edges_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1) + len(self.center_visible) + len(self.extended_center_visible) + len(self.corners_visible) + len(self.two_corners_visible) + len(self.edge_v_a_visible) + len(self.other_edges_visible) + len(self.white_diagonals_visible):
                # Анимация белых диагоналей
                if not self.white_diagonals_visible[self.white_diagonals_index]:
                    self.white_diagonals_visible[self.white_diagonals_index] = True
                    self.white_diagonals_index += 1
                    if self.white_diagonals_index >= len(self.white_diagonals_visible):
                        self.white_diagonals_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1) + len(self.center_visible) + len(self.extended_center_visible) + len(self.corners_visible) + len(self.two_corners_visible) + len(self.edge_v_a_visible) + len(self.other_edges_visible) + len(self.white_diagonals_visible) + len(self.black_diagonals_visible):
                # Анимация чёрных диагоналей
                if not self.black_diagonals_visible[self.black_diagonals_index]:
                    self.black_diagonals_visible[self.black_diagonals_index] = True
                    self.black_diagonals_index += 1
                    if self.black_diagonals_index >= len(self.black_diagonals_visible):
                        self.black_diagonals_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1) + len(self.center_visible) + len(self.extended_center_visible) + len(self.corners_visible) + len(self.two_corners_visible) + len(self.edge_v_a_visible) + len(self.other_edges_visible) + len(self.white_diagonals_visible) + len(self.black_diagonals_visible) + len(self.big_diagonals_visible):
                # Анимация больших диагоналей
                if not self.big_diagonals_visible[self.big_diagonals_index]:
                    self.big_diagonals_visible[self.big_diagonals_index] = True
                    self.big_diagonals_index += 1
                    if self.big_diagonals_index >= len(self.big_diagonals_visible):
                        self.big_diagonals_index = 0
            elif self.animation_count <= self.pause + 2 * len(self.down_arrows_visible) + 2 * len(self.verticals_visible) + 2 * len(self.left_arrows_visible) + 2 * len(self.horizontals_visible) + (len(self.d4_visible) + 1) + (len(self.d5_visible) + 1) + (len(self.e5_visible) + 1) + (len(self.e4_visible) + 1) + len(self.center_visible) + len(self.extended_center_visible) + len(self.corners_visible) + len(self.two_corners_visible) + len(self.edge_v_a_visible) + len(self.other_edges_visible) + len(self.white_diagonals_visible) + len(self.black_diagonals_visible) + len(self.big_diagonals_visible) + len(self.two_diagonals_visible):
                # Анимация двух диагоналей из примера
                if not self.two_diagonals_visible[self.two_diagonals_index]:
                    self.two_diagonals_visible[self.two_diagonals_index] = True
                    self.two_diagonals_index += 1
                    if self.two_diagonals_index >= len(self.two_diagonals_visible):
                        self.two_diagonals_index = 0
            self.animation_count += 1
        else:
            self.timer.stop()  # Завершаем анимацию после прохождения всех шагов

        self.update()  # Перерисовка окна

    def paintEvent(self, event):
        painter = QPainter(self)

        # Фон окна
        painter.fillRect(self.rect(), QColor(0, 128, 0))

        # Смещение доски
        offset_x = 50
        offset_y = 50

        # Регион для рендера
        rect_f = QRectF(offset_x, offset_y, 800, 800)

        # Рендеринг SVG-доски
        self.renderer.render(painter, rect_f)

        # Настройка кисти
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 0, 0))

        # Массив смещений для стрелок
        shifts = [0, 90, 183, 274, 365, 455, 546, 637]

        # Рисуем стрелки «вниз»
        for i, visible in enumerate(self.down_arrows_visible):
            if visible:
                shift = shifts[i]
                points = [
                    QPoint(100 + offset_x + shift, 680 + offset_y),
                    QPoint(60 + offset_x + shift, 680 + offset_y),
                    QPoint(70 + offset_x + shift, 735 + offset_y),
                    QPoint(40 + offset_x + shift, 720 + offset_y),
                    QPoint(80 + offset_x + shift, 770 + offset_y),
                    QPoint(120 + offset_x + shift, 720 + offset_y),
                    QPoint(90 + offset_x + shift, 735 + offset_y)
                ]
                painter.drawPolygon(points)

        # Рисуем стрелки «влево»
        for i, visible in enumerate(self.left_arrows_visible):
            if visible:
                shift = shifts[i]
                points = [
                    QPoint(120 + offset_x, 740 + offset_y - shift),
                    QPoint(120 + offset_x, 700 + offset_y - shift),
                    QPoint(65 + offset_x, 710 + offset_y - shift),
                    QPoint(80 + offset_x, 680 + offset_y - shift),
                    QPoint(30 + offset_x, 720 + offset_y - shift),
                    QPoint(80 + offset_x, 760 + offset_y - shift),
                    QPoint(65 + offset_x, 730 + offset_y - shift)
                ]
                painter.drawPolygon(points)

        # Выделяем вертикали
        for i, visible in enumerate(self.verticals_visible):
            if visible:
                self.vertical_renderers[i].render(painter, rect_f)

        # Выделяем горизонтали
        for i, visible in enumerate(self.horizontals_visible):
            if visible:
                self.horizontal_renderers[i].render(painter, rect_f)

        # Выделяем d4
        for i, visible in enumerate(self.d4_visible):
            if visible:
                self.d4_renderers[i].render(painter, rect_f)

        # Выделяем d5
        for i, visible in enumerate(self.d5_visible):
            if visible:
                self.d5_renderers[i].render(painter, rect_f)

        # Выделяем e5
        for i, visible in enumerate(self.e5_visible):
            if visible:
                self.e5_renderers[i].render(painter, rect_f)

        # Выделяем e4
        for i, visible in enumerate(self.e4_visible):
            if visible:
                self.e4_renderers[i].render(painter, rect_f)

        # Выделяем центр
        for i, visible in enumerate(self.center_visible):
            if visible:
                self.center_renderers[i].render(painter, rect_f)        

        # Добавляем к центру поля до получения расширенного центра
        for i, visible in enumerate(self.extended_center_visible):
            if visible:
                self.extended_center_renderers[i].render(painter, rect_f)

        # Выделяем 4 угла
        for i, visible in enumerate(self.corners_visible):
            if visible:
                self.corners_renderers[i].render(painter, rect_f)

        # Выделяем 2 угла
        for i, visible in enumerate(self.two_corners_visible):
            if visible:
                self.two_corners_renderers[i].render(painter, rect_f)

        # Выделяем край на вертикали a
        for i, visible in enumerate(self.edge_v_a_visible):
            if visible:
                self.edge_v_a_renderers[i].render(painter, rect_f)

        # Выделяем остальные края
        for i, visible in enumerate(self.other_edges_visible):
            if visible:
                self.other_edges_renderers[i].render(painter, rect_f)

        # Выделяем белые диагонали
        for i, visible in enumerate(self.white_diagonals_visible):
            if visible:
                self.white_diagonals_renderers[i].render(painter, rect_f)

        # Выделяем чёрные диагонали
        for i, visible in enumerate(self.black_diagonals_visible):
            if visible:
                self.black_diagonals_renderers[i].render(painter, rect_f)

        # Выделяем большие диагонали
        for i, visible in enumerate(self.big_diagonals_visible):
            if visible:
                self.big_diagonals_renderers[i].render(painter, rect_f)

        # Выделяем две диагонали из примера
        for i, visible in enumerate(self.two_diagonals_visible):
            if visible:
                self.two_diagonals_renderers[i].render(painter, rect_f)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec_())