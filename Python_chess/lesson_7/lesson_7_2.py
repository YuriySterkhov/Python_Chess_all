import sys
import chess
import chess.svg
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QRectF
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtSvg import QSvgRenderer  # Импортируем QSvgRenderer

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
        self.init_timer()

    @init_ui
    def init_moves(self):
        # Список ходов для анимации
        self.moves = [
            chess.Move.from_uci("c2h2"),
            # Добавьте здесь дополнительные ходы
        ]
        self.move_index = 0

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
        self.timer.timeout.connect(self.animate_next_move)
        self.timer.start(5000)  # каждые 5 секунд выполняем следующий ход

    def create_board(self):
        self.board = chess.Board('8/3k4/7b/5K1b/8/8/2R5/8 w - - 0 1')
        
        # Устанавливаем начальные позиции фигур на доске
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
            self.timer.stop()  # Останавливаем таймер после всех ходов

    def update_board(self):
        svg_data = chess.svg.board(self.board)
        self.current_svg = svg_data  # Сохраняем текущее SVG для отрисовки
        self.update()  # Вызываем перерисовку окна

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

            rect_f = QRectF(offset_x, offset_y, width, height)

            renderer.render(painter, rect_f)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChessAnimation()
    sys.exit(app.exec_())