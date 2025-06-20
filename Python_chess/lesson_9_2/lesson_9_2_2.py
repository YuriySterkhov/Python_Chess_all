import sys
import chess
import chess.svg
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QColor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QRectF, QPoint, Qt, QTimer


class ChessGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Самоучитель игры в классические шахматы")
        self.resize(900, 900)

        # Загрузка иконки
        try:
            self.setWindowIcon(QIcon("yus_small.ico"))
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")

        # Шахматная доска
        self.board = chess.Board('8/5K1k/p7/8/8/8/8/8 w - - 0 1')

        # Сохраняем последний загруженный SVG-код здесь
        self.current_svg = chess.svg.board(self.board)

        # Таймер для анимации
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(5000)  # Интервал 5 секунд
        self.step = 0

    def load_svg(self, svg_data):
        """Загрузить данные SVG и сохранить их для последующего рендеринга"""
        self.current_svg = svg_data
        self.update()  # Запускается событие перерисовки окна

    def update_animation(self):
        """Обновляет состояние объектов"""
        svg = ""  # Инициализируем переменную вне блока условий        
            # Используем стандартные методы отображения шахматной доски
        if self.step == 0:
            # Два короля и пешка
            self.board.clear()
            self.board.set_piece_at(chess.F7, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A6, chess.Piece(chess.PAWN, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 1:
            # Выделение квадрата
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.F7, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A6, chess.Piece(chess.PAWN, chess.BLACK))

            # Координаты пешки
            pawn_square = chess.A6
            pawn_rank = chess.square_rank(pawn_square)  # 5 (0-based)
            pawn_file = chess.square_file(pawn_square)  # 0 (0-based)

            # Размер стороны квадрата (например, 2 или 3)
            square_size = pawn_rank  # Можно изменить на нужное значение

            # Определяем границы квадрата
            start_rank = max(0, pawn_rank - square_size)
            end_rank = min(square_size, pawn_rank + square_size)
            start_file = max(0, pawn_file - square_size)
            end_file = min(7, pawn_file + square_size)

            # Создаём набор выделяемых клеток
            highlighted_squares = set()
            for rank in range(start_rank, end_rank + 1):
                for file in range(start_file, end_file + 1):
                    square = chess.square(file, rank)
                    highlighted_squares.add(square)

            # Исключаем клетку пешки из выделения
            highlighted_squares -= {pawn_square}
            # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=highlighted_squares,
                size=350  # Можно указать размер изображения
            )
        elif self.step == 2:
            # Убираем выделение
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.F7, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A6, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 3:
            # Делаем ход белым королём
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.E6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A6, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 4:
            # Делаем ход чёрной пешкой
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.E6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A5, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 5:
            # Выделение квадрата
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.E6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A5, chess.Piece(chess.PAWN, chess.BLACK))

            # Координаты пешки
            pawn_square = chess.A5
            pawn_rank = chess.square_rank(pawn_square)  # 5 (0-based)
            pawn_file = chess.square_file(pawn_square)  # 0 (0-based)

            # Размер стороны квадрата (например, 2 или 3)
            square_size = pawn_rank  # Можно изменить на нужное значение

            # Определяем границы квадрата
            start_rank = max(0, pawn_rank - square_size)
            end_rank = min(square_size, pawn_rank + square_size)
            start_file = max(0, pawn_file - square_size)
            end_file = min(7, pawn_file + square_size)

            # Создаём набор выделяемых клеток
            highlighted_squares = set()
            for rank in range(start_rank, end_rank + 1):
                for file in range(start_file, end_file + 1):
                    square = chess.square(file, rank)
                    highlighted_squares.add(square)

            # Исключаем клетку пешки из выделения
            highlighted_squares -= {pawn_square}
            # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=highlighted_squares,
                size=350  # Можно указать размер изображения
            )
        elif self.step == 6:
            # Убираем выделение
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.E6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A5, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 7:
            # Делаем ход белым королём
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.D5, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A5, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 8:
            # Делаем ход чёрной пешкой
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.D5, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A4, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 9:
            # Выделение квадрата
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.D5, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A4, chess.Piece(chess.PAWN, chess.BLACK))

            # Координаты пешки
            pawn_square = chess.A4
            pawn_rank = chess.square_rank(pawn_square)  # 5 (0-based)
            pawn_file = chess.square_file(pawn_square)  # 0 (0-based)

            # Размер стороны квадрата (например, 2 или 3)
            square_size = pawn_rank  # Можно изменить на нужное значение

            # Определяем границы квадрата
            start_rank = max(0, pawn_rank - square_size)
            end_rank = min(square_size, pawn_rank + square_size)
            start_file = max(0, pawn_file - square_size)
            end_file = min(7, pawn_file + square_size)

            # Создаём набор выделяемых клеток
            highlighted_squares = set()
            for rank in range(start_rank, end_rank + 1):
                for file in range(start_file, end_file + 1):
                    square = chess.square(file, rank)
                    highlighted_squares.add(square)

            # Исключаем клетку пешки из выделения
            highlighted_squares -= {pawn_square}
            # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=highlighted_squares,
                size=350  # Можно указать размер изображения
            )
        elif self.step == 10:
            # Убираем выделение
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.D5, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A4, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 11:
            # Делаем ход белым королём
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.C4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A4, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 12:
            # Делаем ход чёрной пешкой
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.C4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A3, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 13:
            # Выделение квадрата
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.C4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A3, chess.Piece(chess.PAWN, chess.BLACK))

            # Координаты пешки
            pawn_square = chess.A3
            pawn_rank = chess.square_rank(pawn_square)  # 5 (0-based)
            pawn_file = chess.square_file(pawn_square)  # 0 (0-based)

            # Размер стороны квадрата (например, 2 или 3)
            square_size = pawn_rank  # Можно изменить на нужное значение

            # Определяем границы квадрата
            start_rank = max(0, pawn_rank - square_size)
            end_rank = min(square_size, pawn_rank + square_size)
            start_file = max(0, pawn_file - square_size)
            end_file = min(7, pawn_file + square_size)

            # Создаём набор выделяемых клеток
            highlighted_squares = set()
            for rank in range(start_rank, end_rank + 1):
                for file in range(start_file, end_file + 1):
                    square = chess.square(file, rank)
                    highlighted_squares.add(square)

            # Исключаем клетку пешки из выделения
            highlighted_squares -= {pawn_square}
            # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=highlighted_squares,
                size=350  # Можно указать размер изображения
            )
        elif self.step == 14:
            # Убираем выделение
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.C4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A3, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 15:
            # Делаем ход белым королём
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.B3, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A3, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 16:
            # Делаем ход чёрной пешкой
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.B3, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A2, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 17:
            # Выделение квадрата
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.B3, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A2, chess.Piece(chess.PAWN, chess.BLACK))

            # Координаты пешки
            pawn_square = chess.A2
            pawn_rank = chess.square_rank(pawn_square)  # 5 (0-based)
            pawn_file = chess.square_file(pawn_square)  # 0 (0-based)

            # Размер стороны квадрата (например, 2 или 3)
            square_size = pawn_rank  # Можно изменить на нужное значение

            # Определяем границы квадрата
            start_rank = max(0, pawn_rank - square_size)
            end_rank = min(square_size, pawn_rank + square_size)
            start_file = max(0, pawn_file - square_size)
            end_file = min(7, pawn_file + square_size)

            # Создаём набор выделяемых клеток
            highlighted_squares = set()
            for rank in range(start_rank, end_rank + 1):
                for file in range(start_file, end_file + 1):
                    square = chess.square(file, rank)
                    highlighted_squares.add(square)

            # Исключаем клетку пешки из выделения
            highlighted_squares -= {pawn_square}
            # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=highlighted_squares,
                size=350  # Можно указать размер изображения
            )
        elif self.step == 18:
            # Убираем выделение
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.B3, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A2, chess.Piece(chess.PAWN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 19:
            # Делаем ход белым королём
            # Очистка доски, установка королей и пешки
            self.board.clear()
            self.board.set_piece_at(chess.A2, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KING, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)

        if svg != "":
            self.load_svg(svg)

        else:
            # Останавливаем таймер после завершения всех шагов
            self.timer.stop()

        # Переходим к следующему шагу
        self.step += 1

    def paintEvent(self, event):
        """Метод перерисовки окна"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 128, 0))  # Зеленое окно

        if self.current_svg is not None:
            renderer = QSvgRenderer(self.current_svg.encode('utf-8'))
            offset_x = 50
            offset_y = 50
            width = 800
            height = 800

            # Проверка, является ли этот SVG стандартной шахматной позицией
            if isinstance(self.current_svg, chess.svg.SvgWrapper):
                # Это стандартная шахматная доска
                rect_f = QRectF(offset_x, offset_y, width, height)
            else:
                # Внешнее изображение фигуры
                original_size = renderer.defaultSize()
                new_width = int(original_size.width())
                new_height = int(original_size.height())
                x_centered = offset_x + (width - new_width) // 2
                y_centered = offset_y + (height - new_height) // 2
                rect_f = QRectF(x_centered, y_centered, new_width, new_height)

            renderer.render(painter, rect_f)

# Основной цикл приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec_())