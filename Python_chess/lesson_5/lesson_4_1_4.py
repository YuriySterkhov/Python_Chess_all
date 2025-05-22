import sys
import chess
import chess.svg
import chess.engine
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QRectF
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtSvg import QSvgRenderer  # Импортируем QSvgRenderer

# Путь к вашему движку Stockfish
STOCKFISH_PATH = r"C:\stockfish\stockfish-windows-x86-64-sse41-popcnt.exe"
# Forsyth–Edwards Notation (нотация Форсайта — Эдвардса) для рассматриваемой позиции
FEN = '8/8/8/k2rr3/2K5/8/8/3R4 b - - 0 1'

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
        self.init_engine()
        self.generate_random_game()
        self.init_moves()
        self.init_timer()
    
    def init_engine(self):
        """Инициализация шахматного движка."""
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    
    def generate_random_game(self):
        """Генерация случайной игры с использованием движка."""
        board = chess.Board(FEN)
        moves = []
        while not board.is_game_over():
            result = self.engine.play(board, chess.engine.Limit(time=0.1))
            moves.append(result.move)
            board.push(result.move)
        self.moves = moves
    
    @init_ui
    def init_moves(self):
        # Здесь теперь заранее генерируется список ходов
        pass
    
    def init_timer(self):
        # Таймер для задержки перед первым ходом
        self.delay_timer = QTimer(self)
        self.delay_timer.timeout.connect(self.start_animation)
        self.delay_timer.start(2000)  # Задержка 2 секунды
    
    def start_animation(self):
        # Останавливаем таймер задержки и запускаем анимацию ходов
        self.delay_timer.stop()
        
        # Инициализируем индекс первого хода
        self.move_index = 0
        
        # Запускаем таймер для анимации ходов
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_next_move)
        self.timer.start(2000)  # Каждые 2 секунды выполняем следующий ход
    
    def create_board(self):
        self.board = chess.Board(FEN)
        # self.board.turn = chess.BLACK
        self.update_board()
    
    def animate_next_move(self):
        if hasattr(self, 'moves') and self.move_index < len(self.moves):
            move = self.moves[self.move_index]
            if move in self.board.legal_moves:
                print(f"Текущая позиция: {self.board.fen()}")
                print(f"выполняем ход: {move.uci()}")
                self.board.push(move)
                self.update_board()
                print(f"новая позиция: {self.board.fen()}\n")
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