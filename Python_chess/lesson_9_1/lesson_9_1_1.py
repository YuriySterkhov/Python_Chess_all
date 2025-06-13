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
            icon_path = "yus_small.ico"
            self.setWindowIcon(QIcon(icon_path))
        except FileNotFoundError:
            print(f"Иконка '{icon_path}' не найдена.")
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")
            
        self.show()
    return wrapper


class ChessAnimation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_svg = None  # Атрибут для хранения текущего SVG
    
        # Словарь позиций и их ходов
        self.positions = {
            'позиция_1': {'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'display_time': 10},
            'позиция_2': {'fen': '6k1/5ppp/8/2pP2P1/p6P/P4P2/1P3P2/2K5 w - - 0 1', 'display_time': 5},
            # Другие позиции по необходимости
        }
    
        self.moves_dict = {
            'позиция_1': [],
            'позиция_2': [],
            # Другие списки ходов
        }
    
        self.current_position_key = 'позиция_1'  # Начальная позиция
        self.current_moves = self.moves_dict.get(self.current_position_key, [])
        self.move_index = 0
        self.state = 'waiting_display'
        self.transition_delay = 5000  # Задержка перед сменой позиции в миллисекундах
    
        # Создаем доску
        self.create_board()
    
        # Инициализируем главный таймер
        self.main_timer = QTimer(self)
        self.main_timer.timeout.connect(self.handle_main_timer)
        self.main_timer.start(1000)  # Запускаем основной таймер каждую секунду

    @init_ui
    def create_board(self):
        # Инициализация доски текущей позиции по ключу
        fen = self.positions.get(self.current_position_key)['fen']
        self.board = chess.Board(fen)
        self.update_board()

    def handle_main_timer(self):
        """
        Главный обработчик таймера для координации действий.
        """
        if self.state == 'waiting_display':
            display_time = self.positions[self.current_position_key]['display_time'] * 1000
            if self.main_timer.interval() != display_time:
                self.main_timer.setInterval(display_time)
                self.main_timer.start()
            else:
                self.state = 'animating_moves'
                self.move_index = 0
                self.animate_next_move()
        elif self.state == 'animating_moves':
            if self.move_index < len(self.current_moves):
                self.animate_next_move()
            else:
                self.state = 'waiting_transition'
                self.main_timer.setInterval(self.transition_delay)
                self.main_timer.start()
        elif self.state == 'waiting_transition':
            self.change_position()

    def change_position(self):
        # Получение следующего ключа позиции
        keys = list(self.positions.keys())
        current_idx = keys.index(self.current_position_key)
        if current_idx == len(keys)-1:
            # Завершаем программу после последней позиции
            self.main_timer.stop()
            return

        # Переход к следующей позиции
        next_idx = current_idx + 1
        new_position_key = keys[next_idx]
    
        # Настройка новой позиции и сброс значений
        fen = self.positions[new_position_key]['fen']
        self.board = chess.Board(fen)
        self.current_position_key = new_position_key
        self.current_moves = self.moves_dict.get(new_position_key, [])
        self.move_index = 0
        self.state = 'waiting_display'
        self.update_board()
    
        # Запуск основного таймера заново с интервалом ожидания
        self.main_timer.setInterval(self.positions[self.current_position_key]['display_time'] * 1000)
        self.main_timer.start()

    def animate_next_move(self):
        if self.move_index >= len(self.current_moves):
            return
    
        # Выполнение очередного хода
        move = self.current_moves[self.move_index]
        if move in self.board.legal_moves:
            print(f"Выполняем ход: {move.uci()}")
            self.board.push(move)
            self.update_board()
        else:
            print(f"Ход {move.uci()} нелегален")
        self.move_index += 1

    def update_board(self):
        svg_data = chess.svg.board(self.board)
        self.current_svg = svg_data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 128, 0))  # Зеленый фон
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
