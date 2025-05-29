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
        self.board = chess.Board("r3k2r/8/8/4R3/8/8/8/1R2K3 b - - 0 0")

        # Сохраняем последний загруженный SVG-код здесь
        self.current_svg = chess.svg.board(self.board)
        
        self.init_timer()

    def init_timer(self):
        # Таймер для задержки перед первым ходом
        self.delay_timer = QTimer(self)
        self.delay_timer.timeout.connect(self.start_animation)
        self.delay_timer.start(10000)  # Задержка 10 секунд

    def start_animation(self):
        # Останавливаем таймер задержки и запускаем анимацию ходов
        self.delay_timer.stop()
        
        # Запускаем таймер для анимации ходов
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(5000)  # каждые 5 секунд выполняем следующий ход
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
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.E5, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A8, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.H8, chess.Piece(chess.ROOK, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 1:
            # Отражаем шах ходом чёрного короля на вертикаль d
            self.board.clear()
            self.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.B1, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.E5, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.D7, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A8, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.H8, chess.Piece(chess.ROOK, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 2:
            # Демонстрация невозможности длинной рокировки Белых
            self.board.clear()
            self.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.C1, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.H1, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A8, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.H8, chess.Piece(chess.ROOK, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 3:
            # Короткая рокировка Белых и демонстрация невозможности рокировки Чёрных
            self.board.clear()
            self.board.set_piece_at(chess.G1, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.C1, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.F1, chess.Piece(chess.ROOK, chess.WHITE))
            self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
            self.board.set_piece_at(chess.A8, chess.Piece(chess.ROOK, chess.BLACK))
            self.board.set_piece_at(chess.H8, chess.Piece(chess.ROOK, chess.BLACK))
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