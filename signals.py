from PySide6.QtGui import QPainter, QPixmap, QColor, QBrush, QPainterPath
from PySide6.QtCore import Qt


class Signals:
    def __init__(self):
        pass

    def get_pixmap(self, ping):
        return self.get_signal_pixmap(self.get_color(ping), self.get_line_num(ping))

    def get_color(self, ping):
        if ping <= 10:
            return QColor(0x6a, 0x6a, 0xff)
        elif ping <= 20:
            return QColor(0x28, 0x94, 0xff)
        elif ping <= 30:
            return QColor(0x00, 0xff, 0xff)
        elif ping <= 40:
            return QColor(0x9a, 0xff, 0x02)
        elif ping <= 50:
            return QColor(0xe1, 0xe1, 0x00)
        elif ping <= 60:
            return QColor(0xea, 0xc1, 0x00)
        elif ping <= 70:
            return QColor(0xe8, 0x00, 0xe8)
        elif ping <= 80:
            return QColor(0xff, 0x00, 0x80)
        else:
            return QColor(0xea, 0x00, 0x00)

    def get_line_num(self, ping):
        if ping <= 25:
            return 4
        elif ping <= 50:
            return 3
        elif ping <= 75:
            return 2
        elif ping <= 100:
            return 1
        else:
            return 0

    def get_signal_pixmap(self, color, line_num):
        rec_width = 30
        rec_height = 20
        signal_width = rec_width // 4
        signal_height = rec_height // 4
        pixmap = QPixmap(rec_width, rec_height + 2)
        brush = QBrush(color)
        pixmap.fill(QColor(0xd9, 0xd9, 0xd9, 0))
        painter = QPainter(pixmap)
        painter.setPen(QColor(0, 0, 0, 0))
        painter.setBrush(QColor(0, 0, 0, 30))

        # 设置绘制区域
        painter.setClipRect(0, 0, rec_width, rec_height)

        for i in range(4):
            path = QPainterPath()
            path.addRoundedRect(signal_width * i, rec_height - signal_height * (i + 1), signal_width - 3,
                                signal_height * (i + 1), 2, 2)  # 5, 5 是圆角的半径
            painter.drawPath(path)

        painter.setBrush(brush)
        for i in range(line_num):
            path = QPainterPath()
            path.addRoundedRect(signal_width * i, rec_height - signal_height * (i + 1), signal_width - 3,
                                signal_height * (i + 1), 2, 2)  # 5, 5 是圆角的半径
            painter.drawPath(path)

        painter.end()
        return pixmap
