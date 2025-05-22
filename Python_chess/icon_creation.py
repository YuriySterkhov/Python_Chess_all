import sys
import chess
import chess.svg
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QColor, QImage, QBrush, qRgba
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QRectF, Qt, QSize, QPointF

class ChessGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Самоучитель игры в классические шахматы")
        
        # Задаём размер окна по умолчанию
        self.resize(900, 900)  # Ширина 900px и высота 900px
        
        # Загрузка иконки
        try:
            icon_path = "yus_small.jpg"  # Используйте правильный путь к файлу
            self.icon_image = QImage(icon_path)
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")
        
        self.board = chess.Board(
            "4n1n1/3n3n/5Q2/1K1n3n/4n1n1/8/6k1/8 w - - 00 0"
        )
        
        # Генерация изображения доски в формате SVG
        svg_data = chess.svg.board(
            self.board,
            size=800,
            coordinates=True,  # Включаем координаты
            borders=True        # Включаем границы
        )
        
        # Создаем основной рендерер для шахматной доски
        self.renderer = QSvgRenderer(svg_data.encode("utf-8"))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Отрисовка фона рамки (если нужно)
        painter.fillRect(self.rect(), QColor(0, 128, 0))  # Зеленое поле вокруг доски
        
        # Смещение доски для добавления отступов
        offset_x = 50  # Горизонтальный отступ
        offset_y = 50  # Вертикальный отступ
        
        # Определение прямоугольника для рисования шахматной доски
        board_rect = QRectF(offset_x, offset_y, 800, 800)
        
        # Рендеринг основного SVG-дизайна шахматной доски
        self.renderer.render(painter, board_rect)
        
        if not self.icon_image.isNull():
            # Определяем позицию левого нижнего угла для вставки иконки
            square_size = int(board_rect.width() / 8)  # Размер одной клетки
            
            # Левый нижний угол поля a1
            left_bottom_corner = QPointF(offset_x + square_size * 0, offset_y + square_size * 7)
            
            # Масштабируем изображение под размер квадрата
            scaled_icon = self.icon_image.scaled(QSize(square_size*2, square_size*2), Qt.KeepAspectRatioByExpanding)
            
            # Приводим координаты к целым числам перед передачей в drawImage
            painter.drawImage(int(left_bottom_corner.x()) + 35, int(left_bottom_corner.y()) - scaled_icon.height() - 26, scaled_icon)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec_())