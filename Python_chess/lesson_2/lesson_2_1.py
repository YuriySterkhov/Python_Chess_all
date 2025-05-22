import sys
import chess
import chess.svg
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QColor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QRectF, QTimer


class ChessGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Самоучитель игры в классические шахматы")
        self.resize(900, 900)
        try:
            self.setWindowIcon(QIcon("yus_small.ico"))
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")

        self.board = chess.Board("8/8/8/8/8/8/8/8 w - - 0 0")

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

        # Генерируем базовое изображение доски без выделений
        base_board_svg = chess.svg.board(self.board, size=800, coordinates=True, borders=True)
        self.base_renderer = QSvgRenderer(base_board_svg.encode('utf-8'))

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

        # Состояния белых диагоналей
        self.white_diagonals_visible = [False] * 13

        # Состояния черных диагоналей
        self.black_diagonals_visible = [False] * 13

        # Состояния больших диагоналей
        self.big_diagonals_visible = [False] * 2

        # Состояния двух диагоналей из примера
        self.two_diagonals_visible = [False] * 2

        # Индексы текущего для белых диагоналей
        self.white_diagonals_index = 0
        
        # Индексы текущего для чёрных диагоналей
        self.black_diagonals_index = 0

        # Индексы текущего для больших диагоналей
        self.big_diagonals_index = 0

        # Индексы текущего для двух диагоналей из примера
        self.two_diagonals_index = 0

        # Счетчик анимации
        self.animation_count = 0

        # Таймер для анимации
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(500)

    def update_animation(self):
        if self.animation_count <= 30:
            if self.animation_count <= 13:
                # Анимация белых диагоналей
                if not self.white_diagonals_visible[self.white_diagonals_index]:
                    self.white_diagonals_visible[self.white_diagonals_index] = True
                    self.white_diagonals_index += 1
                    if self.white_diagonals_index >= len(self.white_diagonals_visible):
                        self.white_diagonals_index = 0
            elif self.animation_count <= 26:
                # Анимация чёрных диагоналей
                if not self.black_diagonals_visible[self.black_diagonals_index]:
                    self.black_diagonals_visible[self.black_diagonals_index] = True
                    self.black_diagonals_index += 1
                    if self.black_diagonals_index >= len(self.black_diagonals_visible):
                        self.black_diagonals_index = 0
            elif self.animation_count <= 28:
                # Анимация больших диагоналей
                if not self.big_diagonals_visible[self.big_diagonals_index]:
                    self.big_diagonals_visible[self.big_diagonals_index] = True
                    self.big_diagonals_index += 1
                    if self.big_diagonals_index >= len(self.big_diagonals_visible):
                        self.big_diagonals_index = 0
            elif self.animation_count <= 30:
                # Анимация двух диагоналей из примера
                if not self.two_diagonals_visible[self.two_diagonals_index]:
                    self.two_diagonals_visible[self.two_diagonals_index] = True
                    self.two_diagonals_index += 1
                    if self.two_diagonals_index >= len(self.two_diagonals_visible):
                        self.two_diagonals_index = 0
            self.animation_count += 1
        else:
            self.timer.stop()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 128, 0))

        # Базовая доска
        rect_f = QRectF(50, 50, 800, 800)
        self.base_renderer.render(painter, rect_f)

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