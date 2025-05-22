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
        self.board = chess.Board()

        # Сохраняем последний загруженный SVG-код здесь
        self.current_svg = chess.svg.board(self.board)

        # Таймер для анимации
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(10000)  # Интервал 10 секунд
        self.step = 0

    def load_svg(self, svg_data):
        """Загрузить данные SVG и сохранить их для последующего рендеринга"""
        self.current_svg = svg_data
        self.update()  # Запускается событие перерисовки окна

    def update_animation(self):        
        """Обновляет состояние объектов"""
        svg = ""  # Инициализируем переменную вне блока условий

        if self.step < 1 or self.step > 2:
            # Используем стандартные методы отображения шахматной доски
            if self.step == 0:
                # Только два короля
                self.board.clear()
                self.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
                svg = chess.svg.board(self.board)
            elif self.step == 3:
                # Вернуться к двум королям
                svg = chess.svg.board(self.board)
            elif self.step == 4:
                # Выделяем поля возможного хода по горизонтали
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки по горизонтали для обоих королей
                white_king_neighbors = chess.SquareSet([chess.D1, chess.F1])
                black_king_neighbors = chess.SquareSet([chess.D8, chess.F8])
                all_highlighted_squares = white_king_neighbors.union(black_king_neighbors)

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=all_highlighted_squares,
                )
            elif self.step == 5:
                # Выделяем поле возможного хода по вертикали
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки по вертикали для обоих королей
                white_king_neighbors = chess.SquareSet([chess.E2])
                black_king_neighbors = chess.SquareSet([chess.E7])
                all_highlighted_squares = white_king_neighbors.union(black_king_neighbors)

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=all_highlighted_squares,
                )
            elif self.step == 6:
                # Выделяем поля возможного хода по диагонали
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки по диагонали для обоих королей
                white_king_neighbors = chess.SquareSet([chess.D2, chess.F2])
                black_king_neighbors = chess.SquareSet([chess.D7, chess.F7])
                all_highlighted_squares = white_king_neighbors.union(black_king_neighbors)

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=all_highlighted_squares,
                )
            elif self.step == 7:
                # Выделяем все поля возможного хода на краю доски
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки для обоих королей
                white_king_neighbors = chess.SquareSet([chess.D2, chess.F2, chess.D1, chess.F1, chess.E2])
                black_king_neighbors = chess.SquareSet([chess.D7, chess.F7, chess.D8, chess.F8, chess. E7])
                all_highlighted_squares = white_king_neighbors.union(black_king_neighbors)

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=all_highlighted_squares,
                )
            elif self.step == 8:
                # Убираем выделение всех полей возможного хода
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )
            elif self.step == 9:
                # Убираем выделение всех полей возможного хода
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E2, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E7, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )
            elif self.step == 10:
                # Выделяем все поля возможного хода не на краю и не в углу доски
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E2, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E7, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки для обоих королей
                white_king_neighbors = chess.SquareSet([chess.D3, chess.E3, chess.F3,
                                                        chess.D2, chess.F2,
                                                        chess.D1, chess.E1, chess.F1])
                black_king_neighbors = chess.SquareSet([chess.D8, chess. E8, chess.F8,
                                                        chess.D7, chess.F7,
                                                        chess.D6, chess. E6, chess.F6])
                all_highlighted_squares = white_king_neighbors.union(black_king_neighbors)

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=all_highlighted_squares,
                )

            elif self.step == 11:
                # Убираем выделение всех полей возможного хода
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E2, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E7, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )

            elif self.step == 12:
                # Выделяем все поля возможного хода в углу доски
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.A1, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A8, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки для обоих королей
                white_king_neighbors = chess.SquareSet([chess.A2,
                                                        chess.B2,
                                                        chess.B1])
                black_king_neighbors = chess.SquareSet([chess.A7,
                                                        chess.B7,
                                                        chess.B8])
                all_highlighted_squares = white_king_neighbors.union(black_king_neighbors)

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=all_highlighted_squares,
                )

            elif self.step == 13:
                # Убираем выделение всех полей возможного хода
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.A1, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A8, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )
            
            elif self.step == 14:
                # Ставим королей на позицию для создания оппозиции
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.D7, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )
            
            elif self.step == 15:
                # Выделяем все поля возможного хода перед оппозицией
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.D7, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки для обоих королей
                white_king_neighbors = chess.SquareSet([chess.D5, chess.E5,  chess.F5,
                                                        chess.D4, chess.F4,
                                                        chess.D3, chess.F3,  chess.E3])
                black_king_neighbors = chess.SquareSet([chess.C8, chess.D8,  chess.E8,
                                                        chess.C7, chess.E7,
                                                        chess.C6, chess.D6,  chess.E6])
                all_highlighted_squares = white_king_neighbors.union(black_king_neighbors)

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=all_highlighted_squares,
                )

            elif self.step == 16:
                # Убираем выделение всех полей возможного хода
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.D7, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )

            elif self.step == 17:
                # Ходом чёрного короля создаём оппозицию
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E6, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )

            elif self.step == 18:
                # Выделяем все поля возможного хода, утраченные белым королём после создания оппозиции
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E6, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки, недоступные белому королю
                white_king_neighbors = chess.SquareSet([chess.D5,
                                                        chess.E5,
                                                        chess.F5])

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=white_king_neighbors,
                )

            elif self.step == 19:
                # Убираем выделение полей
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E6, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board
                )

            elif self.step == 20:
                # Выделяем все поля возможного хода, доступные белому королю после создания оппозиции
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.E4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.E6, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки, доступные белому королю
                white_king_neighbors = chess.SquareSet([chess.D4,
                                                        chess.D3,
                                                        chess.E3,
                                                        chess.F3,
                                                        chess.F4])

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=white_king_neighbors,
                )

            elif self.step == 21:
                # Ставим королей на позицию для создания оппозиции
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.D4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A4, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )
            
            elif self.step == 22:
                # Выделяем все поля возможного хода перед оппозицией
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.D4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A4, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки для обоих королей
                white_king_neighbors = chess.SquareSet([chess.C5, chess.D5,  chess.E5,
                                                        chess.C4, chess.E4,
                                                        chess.C3, chess.D3,  chess.E3])
                black_king_neighbors = chess.SquareSet([chess.A5, chess.B5,
                                                        chess.B4,
                                                        chess.A3, chess.B3])
                all_highlighted_squares = white_king_neighbors.union(black_king_neighbors)

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=all_highlighted_squares,
                )

            elif self.step == 23:
                # Убираем выделение всех полей возможного хода
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.D4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A4, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )

            elif self.step == 24:
                # Ходом белого короля создаём оппозицию, когда чёрный король на краю доски
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.C4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A4, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )

            elif self.step == 25:
                # Выделяем все поля возможного хода, утраченные чёрным королём после создания оппозиции
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.C4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A4, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки, недоступные чёрному королю
                black_king_neighbors = chess.SquareSet([chess.B5,
                                                        chess.B4,
                                                        chess.B3])

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=black_king_neighbors,
                )

            elif self.step == 26:
                # Убираем выделение полей
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.C4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A4, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board
                )

            elif self.step == 27:
                # Выделяем все поля возможного хода, доступные чёрному королю после создания оппозиции
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.C4, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A4, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки, доступные чёрному королю
                black_king_neighbors = chess.SquareSet([chess.A5,
                                                        chess.A3])

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=black_king_neighbors,
                )
                
            elif self.step == 28:
                # Ставим королей на позицию для создания оппозиции
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.B5, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A8, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )
            
            elif self.step == 29:
                # Выделяем все поля возможного хода перед оппозицией
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.B5, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A8, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки для обоих королей
                white_king_neighbors = chess.SquareSet([chess.A6, chess.B6,  chess.C6,
                                                        chess.A5, chess.C5,
                                                        chess.A4, chess.B4,  chess.C4])
                black_king_neighbors = chess.SquareSet([chess.B8,
                                                        chess.A7, chess.B7])
                all_highlighted_squares = white_king_neighbors.union(black_king_neighbors)

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=all_highlighted_squares,
                )

            elif self.step == 30:
                # Убираем выделение всех полей возможного хода
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.B5, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A8, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )

            elif self.step == 31:
                # Ходом белого короля создаём оппозицию, когда чёрный король в углу доски
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A8, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG без выделения
                svg = chess.svg.board(
                    board=self.board
                )

            elif self.step == 32:
                # Выделяем все поля возможного хода, утраченные чёрным королём после создания оппозиции
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A8, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки, недоступные чёрному королю
                black_king_neighbors = chess.SquareSet([chess.A7,
                                                        chess.B7])

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=black_king_neighbors,
                )

            elif self.step == 33:
                # Убираем выделение полей
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A8, chess.Piece(chess.KING, chess.BLACK))

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board
                )

            elif self.step == 34:
                # Выделяем все поля возможного хода, доступные чёрному королю после создания оппозиции
                # Очистка доски и установка королей
                self.board.clear()
                self.board.set_piece_at(chess.A6, chess.Piece(chess.KING, chess.WHITE))
                self.board.set_piece_at(chess.A8, chess.Piece(chess.KING, chess.BLACK))

                # Создание набора клеток для выделения
                # Cоседние клетки, доступные чёрному королю
                black_king_neighbors = chess.SquareSet([chess.B8])

                # Генерация SVG с выделением
                svg = chess.svg.board(
                    board=self.board,
                    squares=black_king_neighbors,
                )

        elif self.step in (1, 2):
            # Обрабатываем внешние SVG-файлы
            file_path = "lesson_3/white_king.svg" if self.step == 1 else "lesson_3/black_king.svg"
            with open(file_path, "r", encoding="utf-8") as f:
                svg = f.read()  # Прямо присваиваем содержимое файла переменной svg
        
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