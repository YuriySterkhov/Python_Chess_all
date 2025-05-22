import sys
import chess
import chess.svg
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QColor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QRectF

class ChessGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Самоучитель игры в классические шахматы")

        # Задаем размер окна по умолчанию
        self.resize(900, 900)  # Устанавливаем ширину 900px и высоту 900px

        # Загрузка иконки
        try:
            self.setWindowIcon(
                QIcon("yus_small.ico")
            )
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")

        self.board = chess.Board(
            "8/8/8/3n4/8/8/8/8 w - - 02 1"
            )

        # Генерация изображения доски в формате SVG
        svg_data = chess.svg.board(
            self.board,
            size=800,
            coordinates=True,  # Включаем координаты
            borders=True       # Включаем границы
        )

        # Создание рендерера для SVG
        self.renderer = QSvgRenderer(svg_data.encode("utf-8"))

    def paintEvent(self, event):
        painter = QPainter(self)

        # Отрисовка фона рамкой (если нужно)
        painter.fillRect(self.rect(), QColor(0, 128, 0))  # Зеленый цвет для рамки

        # Смещение доски для добавления отступов
        offset_x = 50  # Горизонтальный отступ
        offset_y = 50  # Вертикальный отступ

        # Преобразование QRect в QRectF
        rect_f = QRectF(offset_x, offset_y, 800, 800)
        
        # Рендеринг SVG-изображения с учетом отступов
        self.renderer.render(painter, rect_f)

        # Определение размера одной клетки на доске
        square_size = 742 // 8  # Размер одной клетки (ширина и высота), первый костыль для центрирования маркеров

        # Получение списка атакованных полей
        attacked_squares = self.board.attacks(chess.D5)  # Атакованные поля коня на E4

        # Определяем поправку для координат, второй костыль для центрирования маркеров
        coordinate_offset_x = 27
        coordinate_offset_y = 27

        # Проходимся по каждому атакованному полю
        for square in attacked_squares:
            # Рассчитываем координаты верхнего левого угла клетки
            x = (square % 8) * square_size + offset_x + coordinate_offset_x
            y = (7 - (square // 8)) * square_size + offset_y + coordinate_offset_y

            # Устанавливаем белый цвет для маркеров
            painter.setBrush(QColor(0, 0, 0, 255))

            # Рисуем маркеры по эллипсу с центром в центре клетки
            painter.drawEllipse(x + 25,
                                y + 25,
                                50,
                                50)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec_())