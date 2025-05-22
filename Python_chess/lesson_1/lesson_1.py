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
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 00 0"
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
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec_())