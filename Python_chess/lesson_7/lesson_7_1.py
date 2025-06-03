import sys
import chess
import chess.svg
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QRectF
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtSvg import QSvgRenderer


def init_ui(func):
    """Декоратор для инициализации пользовательского интерфейса."""
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.setWindowTitle("Самоучитель игры в классические шахматы")
        self.resize(900, 900)

        # Загрузка иконки
        try:
            self.setWindowIcon(QIcon("yus_small.ico"))
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")
        self.show()
    return wrapper


class ChessAnimation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_svg = None  # Атрибут для хранения текущего SVG
        self.create_board()
        self.init_moves()
        self.init_timers()
    
    @init_ui
    def init_moves(self):
        # Список ходов для анимации
        self.moves = [
            chess.Move.from_uci("c1b2"),
            chess.Move.from_uci("c8b7"),
            chess.Move.from_uci("f1g2"),
            chess.Move.from_uci("f8g7"),
            # Добавьте здесь дополнительные ходы
        ]
        self.move_index = 0

    def init_timers(self):
        # Первый таймер для отображения начальной позиции
        self.initial_delay_timer = QTimer(self)
        self.initial_delay_timer.timeout.connect(self.show_initial_position)
        self.initial_delay_timer.start(10000)  # задержка 10 секунд

        # Второй таймер для переключения на новую позицию
        self.position_change_timer = QTimer(self)
        self.position_change_timer.timeout.connect(self.change_position)

        # Третий таймер для анимации ходов
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_next_move)

    def show_initial_position(self):
        # Остановка первого таймера и смена позиции
        self.initial_delay_timer.stop()
        self.board = chess.Board('r1bqkb1r/8/8/8/8/8/8/R1BQKB1R w - - 0 1')
        self.update_board()

        # Начало второго таймера для переключения на следующую позицию
        self.position_change_timer.start(5000)  # задержка 5 секунд
        # Начало третьего таймера для анимации ходов
        self.animation_timer.start(5000)  # каждые 5 секунд выполняется следующий ход

    def change_position(self):
        # Остановка второго таймера
        self.position_change_timer.stop()

        

    def create_board(self):
        self.board = chess.Board()
        self.update_board()

    def animate_next_move(self):
        if self.move_index < len(self.moves):
            move = self.moves[self.move_index]
            if move in self.board.legal_moves:
                print(f"Выполняем ход: {move.uci()}")
                self.board.push(move)
                self.update_board()
            else:
                print(f"Ход {move.uci()} нелегален")
            self.move_index += 1
        else:
            print("Все ходы выполнены")
            self.animation_timer.stop()  # останавливаем таймер после завершения всех ходов

    def update_board(self):
        svg_data = chess.svg.board(self.board)
        self.current_svg = svg_data  # сохраняем текущее SVG для отрисовки
        self.update()  # вызываем перерисовку окна

    def paintEvent(self, event):
        """Метод перерисовки окна"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 128, 0))  # зеленое окно

        if self.current_svg is not None:
            renderer = QSvgRenderer(self.current_svg.encode('utf-8'))
            offset_x = 50
            offset_y = 50
            width = 800
            height = 800

            rect_f = QRectF(offset_x, offset_y, width, height)

            renderer.render(painter, rect_f)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChessAnimation()
    sys.exit(app.exec_())