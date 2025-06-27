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
FEN = '4n3/1k6/6n1/8/4P3/8/1K6/8 b - - 0 1'

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
        self.init_timer()
    
    @init_ui
    def create_board(self):
        self.board = chess.Board(FEN)
        self.position_repeats = {}  # Словарь для отслеживания повторений позиций
        self.update_board()
    
    def init_engine(self):
        """Инициализация шахматного движка."""
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    
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
        self.timer.start(3000)  # Каждые 3 секунды выполняем следующий ход
    
    def animate_next_move(self):
        # Если игра ещё не завершилась
        if not self.board.is_game_over():
            # Получаем лучший ход от движка
            result = self.engine.play(self.board, chess.engine.Limit(time=1))
            move = result.move
            
            # Выполняем ход на доске
            self.board.push(move)
            
            # Подсчет количества возникновений текущей позиции
            current_fen = self.board.fen()
            print(current_fen)
            current_position = current_fen[:current_fen.rfind(' ')][:current_fen[:current_fen.rfind(' ')].rfind(' ')]
            if current_position in self.position_repeats:
                self.position_repeats[current_position] += 1
            else:
                self.position_repeats[current_position] = 1
                
            # Обновляем визуализацию
            self.update_board()
            
            # Проверка специальных условий окончания игры
            if self.board.is_stalemate():
                print("Пат! Партия закончилась вничью.")
                # Печать всех повторенных позиций и их числа
                for position, count in self.position_repeats.items():
                    print(f"Позиция: {position}, количество возникновений: {count}")
                self.timer.stop()
                return
            elif self.board.is_checkmate():
                print("Мат! Игра завершена.")
                # Печать всех повторенных позиций и их числа
                for position, count in self.position_repeats.items():
                    print(f"Позиция: {position}, количество возникновений: {count}")
                self.timer.stop()
                return
            elif self.board.can_claim_draw():
                print("Возможна заявленная ничья.")
                # Печать всех повторенных позиций и их числа
                for position, count in self.position_repeats.items():
                    print(f"Позиция: {position}, количество возникновений: {count}")
                self.timer.stop()
                return
        else:
            print("Игра завершена!")
            self.timer.stop()
            # Печать всех повторенных позиций и их числа
            for position, count in self.position_repeats.items():
                print(f"Позиция: {position}, Количество повторений: {count}")
    
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

def main():
    app = QApplication(sys.argv)
    window = ChessAnimation()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()