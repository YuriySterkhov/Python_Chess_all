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
        self.board = chess.Board('8/8/K4Q2/8/8/8/6k1/8 w - - 0 1')

        # Сохраняем последний загруженный SVG-код здесь
        self.current_svg = chess.svg.board(self.board)

        # Таймер для анимации
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(5000)  # Интервал 10 секунд
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
            # Два короля и ферзь
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 1:
            # Выделяем поля возможного хода ферзя
            # Очистка доски, установка королей и ферзя
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Получаем позицию белого ферзя на f6
            queen_square = chess.F6

            # Генерация возможных ходов белого ферзя на f6
            all_moves = self.board.legal_moves
            queen_f6_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == queen_square:
                    queen_f6_moves_squares.add(move.to_square)

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=(queen_f6_moves_squares),
            )
        elif self.step == 2:
            # Убираем выделение
            # Очистка доски, установка королей и ферзя
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 3:
            # Инициализация доски и установка фигур
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Получаем позицию ферзя
            queen_square = chess.F6

            # Генерируем все возможные ходы ферзя
            all_moves = self.board.legal_moves

            # Собираем все клетки, куда ферзь может пойти
            reachable_squares = set()
            for move in all_moves:
                if move.from_square == queen_square:
                    reachable_squares.add(move.to_square)

            # Все клетки доски
            all_squares = set(range(64))

            # Клетки, недоступные для хода ферзя
            unreachable_squares = all_squares - reachable_squares - {chess.F6}

            # Теперь ищем ближайшие к ферзю клетки из unreachable_squares
            # Используем поиск в ширину (BFS) для определения минимального расстояния

            def square_distance(sq1, sq2):
                rank1 = sq1 // 8
                file1 = sq1 % 8
                rank2 = sq2 // 8
                file2 = sq2 % 8
                return max(abs(rank1 - rank2), abs(file1 - file2))  # Манхэттен или Chebyshev

            min_distance = None
            nearest_unreachable_squares = []

            for sq in unreachable_squares:
                dist = square_distance(queen_square, sq)
                if min_distance is None or dist < min_distance:
                    min_distance = dist

            # Собираем все клетки на минимальном расстоянии
            for sq in unreachable_squares:
                if square_distance(queen_square, sq) == min_distance:
                    nearest_unreachable_squares.append(sq)

            # Создаём объект SquareSet для выделения этих клеток
            squares_to_highlight = chess.SquareSet(nearest_unreachable_squares)

            # Генерация SVG с выделением ближайших недоступных клеток
            svg = chess.svg.board(
                board=self.board,
                squares=squares_to_highlight,
            )
        elif self.step == 4:
            # Убираем выделение
            # Очистка доски, установка королей и ферзя
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 5:
            # Выделяем поля возможного хода ферзя
            # Очистка доски, установка королей и ферзя
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Получаем позицию белого ферзя на f6
            queen_square = chess.F6

            # Генерация возможных ходов белого ферзя на f6
            all_moves = self.board.legal_moves
            queen_f6_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == queen_square:
                    queen_f6_moves_squares.add(move.to_square)

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=(queen_f6_moves_squares),
            )
        elif self.step == 6:
            # Убираем выделение
            # Очистка доски, установка королей и ферзя
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 7:
            # Инициализация доски и установка фигур
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Получаем позицию ферзя
            queen_square = chess.F6

            # Генерируем все возможные ходы ферзя
            all_moves = self.board.legal_moves

            # Собираем все клетки, куда ферзь может пойти
            reachable_squares = set()
            for move in all_moves:
                if move.from_square == queen_square:
                    reachable_squares.add(move.to_square)

            # Все клетки доски
            all_squares = set(range(64))

            # Клетки, недоступные для хода ферзя
            unreachable_squares = all_squares - reachable_squares - {chess.F6}

            # Теперь ищем ближайшие к ферзю клетки из unreachable_squares
            # Используем поиск в ширину (BFS) для определения минимального расстояния

            def square_distance(sq1, sq2):
                rank1 = sq1 // 8
                file1 = sq1 % 8
                rank2 = sq2 // 8
                file2 = sq2 % 8
                return max(abs(rank1 - rank2), abs(file1 - file2))  # Манхэттен или Chebyshev

            min_distance = None
            nearest_unreachable_squares = []

            for sq in unreachable_squares:
                dist = square_distance(queen_square, sq)
                if min_distance is None or dist < min_distance:
                    min_distance = dist

            # Собираем все клетки на минимальном расстоянии
            for sq in unreachable_squares:
                if square_distance(queen_square, sq) == min_distance:
                    nearest_unreachable_squares.append(sq)

            # Создаём объект SquareSet для выделения этих клеток
            squares_to_highlight = chess.SquareSet(nearest_unreachable_squares)

            # Генерация SVG с выделением ближайших недоступных клеток
            svg = chess.svg.board(
                board=self.board,
                squares=squares_to_highlight,
            )
        elif self.step == 8:
            # Инициализация доски и установка фигур, убираем ферзя
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Получаем позицию ферзя
            queen_square = chess.F6

            # Генерируем все возможные ходы ферзя
            all_moves = self.board.legal_moves

            # Собираем все клетки, куда ферзь может пойти
            reachable_squares = set()
            for move in all_moves:
                if move.from_square == queen_square:
                    reachable_squares.add(move.to_square)

            # Все клетки доски
            all_squares = set(range(64))

            # Клетки, недоступные для хода ферзя
            unreachable_squares = all_squares - reachable_squares - {chess.F6}

            # Теперь ищем ближайшие к ферзю клетки из unreachable_squares
            # Используем поиск в ширину (BFS) для определения минимального расстояния

            def square_distance(sq1, sq2):
                rank1 = sq1 // 8
                file1 = sq1 % 8
                rank2 = sq2 // 8
                file2 = sq2 % 8
                return max(abs(rank1 - rank2), abs(file1 - file2))  # Манхэттен или Chebyshev

            min_distance = None
            nearest_unreachable_squares = []

            for sq in unreachable_squares:
                dist = square_distance(queen_square, sq)
                if min_distance is None or dist < min_distance:
                    min_distance = dist

            # Собираем все клетки на минимальном расстоянии
            for sq in unreachable_squares:
                if square_distance(queen_square, sq) == min_distance:
                    nearest_unreachable_squares.append(sq)

            # Создаём объект SquareSet для выделения этих клеток
            squares_to_highlight = chess.SquareSet(nearest_unreachable_squares)

            # Удаляем ферзя перед генерацией SVG
            self.board.remove_piece_at(chess.F6)

            # Генерация SVG с выделением ближайших недоступных клеток
            svg = chess.svg.board(
                board=self.board,
                squares=squares_to_highlight,
            )
        elif self.step == 9:
            # Выделяем поля возможного хода коня
            # Очистка доски, установка королей и коня
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.KNIGHT, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Получаем позицию белого коня на f6
            queen_square = chess.F6

            # Генерация возможных ходов белого коня на f6
            all_moves = self.board.legal_moves
            queen_f6_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == queen_square:
                    queen_f6_moves_squares.add(move.to_square)

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=(queen_f6_moves_squares),
            )
        elif self.step == 10:
            # Убираем выделение
            # Очистка доски, установка королей и коня
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.KNIGHT, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 11:
            # Убираем выделение
            # Очистка доски, установка королей, коня и ферзей
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.KNIGHT, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.D7, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.E8, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.G8, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.H5, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.G4, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.E4, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.D5, chess.Piece(chess.QUEEN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 12:
            # Убираем выделение
            # Очистка доски, установка королей
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 13:
            # Убираем выделение
            # Очистка доски, установка королей, коня и ферзей
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.D7, chess.Piece(chess.KNIGHT, chess.BLACK))
            self.board.set_piece_at(chess.E8, chess.Piece(chess.KNIGHT, chess.BLACK))
            self.board.set_piece_at(chess.G8, chess.Piece(chess.KNIGHT, chess.BLACK))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.KNIGHT, chess.BLACK))
            self.board.set_piece_at(chess.H5, chess.Piece(chess.KNIGHT, chess.BLACK))
            self.board.set_piece_at(chess.G4, chess.Piece(chess.KNIGHT, chess.BLACK))
            self.board.set_piece_at(chess.E4, chess.Piece(chess.KNIGHT, chess.BLACK))
            self.board.set_piece_at(chess.D5, chess.Piece(chess.KNIGHT, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 14:
            # Убираем выделение
            # Очистка доски, установка королей
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 15:
            # Выделяем поля возможного хода коня
            # Очистка доски, установка королей и коня
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.KNIGHT, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Получаем позицию белого коня на f6
            queen_square = chess.F6

            # Генерация возможных ходов белого коня на f6
            all_moves = self.board.legal_moves
            queen_f6_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == queen_square:
                    queen_f6_moves_squares.add(move.to_square)

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=(queen_f6_moves_squares),
            )
        elif self.step == 16:
            # Убираем выделение
            # Очистка доски, установка королей
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 17:
            # Выделяем поля возможного хода коня
            # Очистка доски, установка королей и коня
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.E6, chess.Piece(chess.KNIGHT, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Получаем позицию белого коня на e6
            queen_square = chess.E6

            # Генерация возможных ходов белого коня на e6
            all_moves = self.board.legal_moves
            queen_e6_moves_squares = chess.SquareSet()

            # Создание набора клеток для выделения
            for move in all_moves:
                if move.from_square == queen_square:
                    queen_e6_moves_squares.add(move.to_square)

             # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                squares=(queen_e6_moves_squares),
            )
        elif self.step == 18:
            # Убираем выделение
            # Очистка доски, установка королей
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 19:
            # Убираем выделение
            # Очистка доски, установка королей, коня и ферзей
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.KNIGHT, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.D7, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.E8, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.G8, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.H5, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.G4, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.E4, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.D5, chess.Piece(chess.QUEEN, chess.BLACK))

            # Генерация SVG без выделения
            svg = chess.svg.board(self.board)
        elif self.step == 20:
            # Убираем выделение
            # Очистка доски, установка королей, коня и ферзей
            self.board.clear()
            self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F6, chess.Piece(chess.KNIGHT, chess.WHITE))
            self.board.set_piece_at(chess.E5, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.E6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.E7, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.F7, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G7, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G6, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G5, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.F5, chess.Piece(chess.QUEEN, chess.WHITE))
            self.board.set_piece_at(chess.G2, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.D7, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.E8, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.G8, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.H7, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.H5, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.G4, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.E4, chess.Piece(chess.QUEEN, chess.BLACK))
            self.board.set_piece_at(chess.D5, chess.Piece(chess.QUEEN, chess.BLACK))

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