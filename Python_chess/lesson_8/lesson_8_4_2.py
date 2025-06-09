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
        self.board = chess.Board('8/8/8/5N1B/8/8/3K1k2/8 b - - 0 1')

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
            # Два короля, конь и слон
            self.board.clear()
            self.board.set_piece_at(chess.D2, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F5, chess.Piece(chess.KNIGHT, chess.WHITE))
            self.board.set_piece_at(chess.H5, chess.Piece(chess.BISHOP, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.KING, chess.BLACK))
            svg = chess.svg.board(self.board)
        elif self.step == 1:
            # Выделяем препятствие для чёрного короля
            # Очистка доски и установка Фигур
            self.board.clear()
            self.board.set_piece_at(chess.D2, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F5, chess.Piece(chess.KNIGHT, chess.WHITE))
            self.board.set_piece_at(chess.H5, chess.Piece(chess.BISHOP, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.KING, chess.BLACK))

            # Генерация SVG с выделением
            svg = chess.svg.board(
                board=self.board,
                # объединяем нужные поля
                squares=(chess.BB_E1
                         | chess.BB_E2
                         | chess.BB_E3
                         | chess.BB_F3
                         | chess.BB_G3
                         | chess.BB_G4
                         | chess.BB_H4),
            )
        elif self.step == 2:
            # Убираем выделение полей
            self.board.clear()
            self.board.set_piece_at(chess.D2, chess.Piece(chess.KING, chess.WHITE))
            self.board.set_piece_at(chess.F5, chess.Piece(chess.KNIGHT, chess.WHITE))
            self.board.set_piece_at(chess.H5, chess.Piece(chess.BISHOP, chess.WHITE))
            self.board.set_piece_at(chess.F2, chess.Piece(chess.KING, chess.BLACK))
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