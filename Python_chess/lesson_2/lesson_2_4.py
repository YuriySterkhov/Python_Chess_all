'''
В этом модуле волей случая реализована синхронная анимация стрелок, поэтому он лежит в папке, вдруг...
'''

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

        self.animation_count = 0  # Инициализация счетчика

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
            "8/8/8/8/8/8/8/8 w - - 0 0"
        )  # Корректируем FEN-нотацию

        # Генерация изображения доски в формате SVG
        svg_data = chess.svg.board(
            self.board,
            size=800,
            coordinates=True,  # Включаем координаты
            borders=True       # Включаем границы
        )

        # Создание рендерера для SVG
        self.renderer = QSvgRenderer(svg_data.encode("utf-8"))

        # Список состояний стрелок (True - стрелка видима, False - скрыта)
        self.arrows_visible = [False] * 8  # Изначально все стрелки скрыты

        # Индекс текущей активной стрелки
        self.current_arrow_index = 0

        # Таймер для анимации стрелок
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(2000)  # Интервал между сменой состояний стрелки — 2 секунды

    def update_animation(self):
        """Обновление состояния видимости стрелки"""
        if self.animation_count < 16:  # Теперь всего 16 шагов анимации (по два шага на каждую стрелку)
            if not self.arrows_visible[self.current_arrow_index]:
                self.arrows_visible[self.current_arrow_index] = True  # Стрелка появляется
            else:
                self.arrows_visible[self.current_arrow_index] = False  # Стрелка исчезает
                self.current_arrow_index += 1  # Переходим к следующей стрелке
                if self.current_arrow_index >= len(self.arrows_visible):  # Если достигли конца списка
                    self.current_arrow_index = 0  # Возвращаемся к первой стрелке

            self.animation_count += 1  # Увеличение счётчика

        else:
            self.timer.stop()  # Останавливаем таймер после полного цикла

        self.update()  # Обновление окна для перерисовки

    def paintEvent(self, event):
        painter = QPainter(self)

        # Отрисовка фона рамкой (если нужно)
        painter.fillRect(self.rect(), QColor(0, 128, 0))  # Зелёный цвет для рамки

        # Смещение доски для добавления отступов
        offset_x = 50  # Горизонтальный отступ
        offset_y = 50  # Вертикальный отступ

        # Преобразование QRect в QRectF
        rect_f = QRectF(offset_x, offset_y, 800, 800)

        # Рендеринг SVG-изображения с учётом отступов
        self.renderer.render(painter, rect_f)

        # Рисуем красные стрелки, если соответствующие элементы в arrows_visible равны True
        painter.setPen(Qt.NoPen)  # Убираем контур фигуры
        painter.setBrush(QColor(255, 0, 0))  # Красный цвет заливки

        shifts = [0, 90, 183, 274, 365, 455, 546, 637]
        for i, visible in enumerate(self.arrows_visible):
            if visible:
                shift = shifts[i]
                # Определяем координаты трапеции и треугольника, образующих стрелку «вниз»
                points = [
                    QPoint(100 + offset_x + shift, 680 + offset_y),  # Верхняя правая вершина трапеции
                    QPoint(60 + offset_x + shift, 680 + offset_y),  # Верхняя левая вершина трапеции
                    QPoint(70 + offset_x + shift, 735 + offset_y),  # Нижняя левая вершина трапеции
                    QPoint(40 + offset_x + shift, 720 + offset_y),  # Левая вершина треугольника
                    QPoint(80 + offset_x + shift, 770 + offset_y),  # Нижняя вершина треугольника
                    QPoint(120 + offset_x + shift, 720 + offset_y),  # Правая вершина треугольника
                    QPoint(90 + offset_x + shift, 735 + offset_y)   # Нижняя правая вершина трапеции
                ]

                # Нарисуем многоугольник, используя указанные точки
                painter.drawPolygon(points)
        
        for i, visible in enumerate(self.arrows_visible):
            if visible:
                shift = shifts[i]
                # Определяем координаты трапеции и треугольника, образующих стрелку «влево»
                points = [
                    QPoint(120 + offset_x, 740 + offset_y  - shift),  # Верхняя правая вершина трапеции
                    QPoint(120 + offset_x, 700 + offset_y  - shift),  # Верхняя левая вершина трапеции
                    QPoint(65 + offset_x, 710 + offset_y  - shift),  # Нижняя левая вершина трапеции
                    QPoint(80 + offset_x, 680 + offset_y  - shift),  # Левая вершина треугольника
                    QPoint(30 + offset_x, 720 + offset_y  - shift),  # Нижняя вершина треугольника
                    QPoint(80 + offset_x, 760 + offset_y  - shift),  # Правая вершина треугольника
                    QPoint(65 + offset_x, 730 + offset_y  - shift)   # Нижняя правая вершина трапеции
                ]

                # Нарисуем многоугольник, используя указанные точки
                painter.drawPolygon(points)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec_())