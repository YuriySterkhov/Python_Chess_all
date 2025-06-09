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
            'позиция_1': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
            'позиция_2': 'rnbqkbnr/8/8/8/8/8/8/RNBQKBNR w - - 0 1',
            # 'позиция_3': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1',
            # Другие позиции по необходимости
        }
    
        self.moves_dict = {
            'позиция_1': [],
            'позиция_2': [],
            # 'позиция_3': [chess.Move.from_uci(m) for m in ["e2e4", "e7e5", "g1f3", "g8f6"]],
            # Другие списки ходов
        }
    
        self.current_position_key = 'позиция_1'  # Начальная позиция
        self.current_moves = self.moves_dict.get(self.current_position_key, [])
        self.move_index = 0
        self.paused_for_transition = False  # Сигналирует ожидание паузы между позициями
    
        # Создание доски
        self.create_board()
    
        # Инициализация таймеров
        self.init_timers()

    @init_ui
    def create_board(self):
        # Инициализация доски текущей позиции по ключу
        fen = self.positions.get(self.current_position_key, '')
        self.board = chess.Board(fen)
        self.update_board()

    def init_timers(self):
        # Таймер для переключения позиций каждые 5 секунд ПОСЛЕ окончания анимации ходов
        self.position_change_timer = QTimer(self)
        self.position_change_timer.timeout.connect(self.change_position)
    
        # Таймер для анимации ходов каждые 3 секунды
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_next_move)
        self.animation_timer.start(3000)  # Запустим таймер сразу для первой позиции

    def change_position(self):
        # Получить следующий ключ позиции
        keys = list(self.positions.keys())
        current_idx = keys.index(self.current_position_key)
        if current_idx == len(keys)-1:
            # Завершаем программу после последней позиции
            self.position_change_timer.stop()
            return

        # Перейти к следующей позиции
        next_idx = current_idx + 1
        new_position_key = keys[next_idx]
    
        # Настроить новую позицию и сброс значений
        fen = self.positions[new_position_key]
        self.board = chess.Board(fen)
        self.current_position_key = new_position_key
        self.current_moves = self.moves_dict.get(new_position_key, [])
        self.move_index = 0
        self.paused_for_transition = False  # Пауза сброшена
        self.update_board()
    
        # Продолжаем таймер анимации для новой позиции
        self.animation_timer.start(3000)

    def animate_next_move(self):
        if self.paused_for_transition or self.move_index >= len(self.current_moves):
            # Завершили все ходы, ждем паузу перед сменой позиции
            self.animation_timer.stop()
            self.position_change_timer.start(5000)  # Ждём 5 секунд перед сменой позиции
            self.paused_for_transition = True
            return
    
        # Выполнить очередной ход
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
        painter.fillRect(self.rect(), QColor(0, 128, 0))  # Зелёный фон
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