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
        self.board = chess.Board()

        # Сохраняем последний загруженный SVG-код здесь
        self.current_svg = chess.svg.board(self.board)

        # Таймер для анимации
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(2000)  # Интервал 10 секунд
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
            # Два короля и четыре ладьи
            self.board.clear()
            self.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.A1, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.H1, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A8, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.H8, chess.Piece(chess.ROOK, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 1:
            # Меняем положение королей и ладей
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 2:
            # Выделяем поля возможного хода для ладьи на d4
            # Очистка доски и установка Фигур
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))

            # Получаем позицию белой ладьи на d4
            rook_square = chess.D4

            # Генерация возможных ходов для белой ладьи на d4
            all_moves = self.board.legal_moves
            rook_d4_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == rook_square:
                    rook_d4_moves_squares.add(move.to_square)            

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=rook_d4_moves_squares,
            )
        elif self.step == 3:
            # Убираем выделение полей
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 4:
            # Выделяем поля возможного хода для ладьи на f2
            # Очистка доски и установка Фигур
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))

            # Получаем позицию белой ладьи на f2
            rook_square = chess.F2

            # Генерация возможных ходов для белой ладьи на f2
            all_moves = self.board.legal_moves
            rook_f2_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == rook_square:
                    rook_f2_moves_squares.add(move.to_square)

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=rook_f2_moves_squares,
            )
        elif self.step == 5:
            # Убираем выделение полей
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 6:
            # Выделяем поля возможного хода для ладьи на b1
            # Очистка доски и установка Фигур
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))
            # Устанавливаем текущую сторону на черных (ход чёрных)
            self.board.turn = chess.BLACK

            # Получаем позицию чёрной ладьи на b1
            rook_square = chess.B1

            # Генерация возможных ходов для чёрной ладьи на b1
            all_moves = self.board.legal_moves
            rook_b1_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == rook_square:
                    rook_b1_moves_squares.add(move.to_square)

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=rook_b1_moves_squares,
            )
        elif self.step == 7:
            # Убираем выделение полей
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 8:
            # Выделяем поля возможного хода для ладьи на b5
            # Очистка доски и установка Фигур
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))
            # Устанавливаем текущую сторону на черных (ход чёрных)
            self.board.turn = chess.BLACK

            # Получаем позицию чёрной ладьи на b5
            rook_square = chess.B5

            # Генерация возможных ходов для чёрной ладьи на b5
            all_moves = self.board.legal_moves
            rook_b5_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == rook_square:
                    rook_b5_moves_squares.add(move.to_square)

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=rook_b5_moves_squares,
            )
        elif self.step == 9:
            # Убираем выделение полей
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 10:
            # Выделяем поля возможного хода для чёрного короля
            # Очистка доски и установка Фигур
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))
            # Устанавливаем текущую сторону на черных (ход чёрных)
            self.board.turn = chess.BLACK

            # Получаем позицию чёрного короля
            rook_square = chess.C6

            # Генерация возможных ходов для чёрного короля
            all_moves = self.board.legal_moves
            black_king_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == rook_square:
                    black_king_moves_squares.add(move.to_square)

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=black_king_moves_squares,
            )
        elif self.step == 11:
            # Убираем выделение полей
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 12:
            # Выделяем поля возможного хода для белого короля
            # Очистка доски и установка Фигур
            self.board.clear()
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.D4, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.C6, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.B5, chess.Piece(chess.ROOK, chess.BLACK))

            # Получаем позицию белого короля
            rook_square = chess.E4

            # Генерация возможных ходов для белого короля
            all_moves = self.board.legal_moves
            black_king_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == rook_square:
                    black_king_moves_squares.add(move.to_square)

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=black_king_moves_squares,
            )
        
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