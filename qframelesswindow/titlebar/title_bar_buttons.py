# coding:utf-8
from enum import Enum

from PySide6.QtCore import QFile, QPointF, QRectF, Qt, Property
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush
from PySide6.QtWidgets import QAbstractButton
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtXml import QDomDocument
from loguru import logger

from .._rc import resource


class TitleBarButtonState(Enum):
    """ Title bar button state """
    NORMAL = 0
    HOVER = 1
    PRESSED = 2


class TitleBarButton(QAbstractButton):
    """ Title bar button """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setCursor(Qt.ArrowCursor)
        self.setFixedSize(46, 32)
        self._state = TitleBarButtonState.NORMAL

        # icon color
        self._normalColor = QColor(0, 0, 0)
        self._hoverColor = QColor(0, 0, 0)
        self._pressedColor = QColor(0, 0, 0)

        # background color
        self._normalBgColor = QColor(0, 0, 0, 0)
        self._hoverBgColor = QColor(0, 0, 0, 26)
        self._pressedBgColor = QColor(0, 0, 0, 51)

    def setState(self, state):
        """ set the state of button

        Parameters
        ----------
        state: TitleBarButtonState
            the state of button
        """
        self._state = state
        self.update()

    def isPressed(self):
        """ whether the button is pressed """
        return self._state == TitleBarButtonState.PRESSED

    def getNormalColor(self):
        """ get the icon color of the button in normal state """
        return self._normalColor

    def getHoverColor(self):
        """ get the icon color of the button in hover state """
        return self._hoverColor

    def getPressedColor(self):
        """ get the icon color of the button in pressed state """
        return self._pressedColor

    def getNormalBackgroundColor(self):
        """ get the background color of the button in normal state """
        return self._normalBgColor

    def getHoverBackgroundColor(self):
        """ get the background color of the button in hover state """
        return self._hoverBgColor

    def getPressedBackgroundColor(self):
        """ get the background color of the button in pressed state """
        return self._pressedBgColor

    def setNormalColor(self, color):
        """ set the icon color of the button in normal state

        Parameters
        ----------
        color: QColor
            icon color
        """
        self._normalColor = QColor(color)
        self.update()

    def setHoverColor(self, color):
        """ set the icon color of the button in hover state

        Parameters
        ----------
        color: QColor
            icon color
        """
        self._hoverColor = QColor(color)
        self.update()

    def setPressedColor(self, color):
        """ set the icon color of the button in pressed state

        Parameters
        ----------
        color: QColor
            icon color
        """
        self._pressedColor = QColor(color)
        self.update()

    def setNormalBackgroundColor(self, color):
        """ set the background color of the button in normal state

        Parameters
        ----------
        color: QColor
            background color
        """
        self._normalBgColor = QColor(color)
        self.update()

    def setHoverBackgroundColor(self, color):
        """ set the background color of the button in hover state

        Parameters
        ----------
        color: QColor
            background color
        """
        self._hoverBgColor = QColor(color)
        self.update()

    def setPressedBackgroundColor(self, color):
        """ set the background color of the button in pressed state

        Parameters
        ----------
        color: QColor
            background color
        """
        self._pressedBgColor = QColor(color)
        self.update()

    def setHide(self, hide: bool = True):
        """ set the button visible or not

        Parameters
        ----------
        hide: bool
            whether to hide the button
        """
        logger.debug(f"setHide: {hide}")
        self.setVisible(not hide)

    def enterEvent(self, e):
        self.setState(TitleBarButtonState.HOVER)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setState(TitleBarButtonState.NORMAL)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return

        self.setState(TitleBarButtonState.PRESSED)
        super().mousePressEvent(e)

    def _getColors(self):
        """ get the icon color and background color """
        if self._state == TitleBarButtonState.NORMAL:
            return self._normalColor, self._normalBgColor
        elif self._state == TitleBarButtonState.HOVER:
            return self._hoverColor, self._hoverBgColor

        return self._pressedColor, self._pressedBgColor

    normalColor = Property(QColor, getNormalColor, setNormalColor)
    hoverColor = Property(QColor, getHoverColor, setHoverColor)
    pressedColor = Property(QColor, getPressedColor, setPressedColor)
    normalBackgroundColor = Property(
        QColor, getNormalBackgroundColor, setNormalBackgroundColor)
    hoverBackgroundColor = Property(
        QColor, getHoverBackgroundColor, setHoverBackgroundColor)
    pressedBackgroundColor = Property(
        QColor, getPressedBackgroundColor, setPressedBackgroundColor)


class SvgTitleBarButton(TitleBarButton):
    """ Title bar button using svg icon """

    def __init__(self, iconPath, parent=None):
        """
        Parameters
        ----------
        iconPath: str
            the path of icon

        parent: QWidget
            parent widget
        """
        super().__init__(parent)
        self._svgDom = QDomDocument()
        self.setIcon(iconPath)

    def setIcon(self, iconPath):
        """ set the icon of button

        Parameters
        ----------
        iconPath: str
            the path of icon
        """
        f = QFile(iconPath)
        f.open(QFile.ReadOnly)
        self._svgDom.setContent(f.readAll())
        f.close()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        color = color.name()
        pathNodes = self._svgDom.elementsByTagName('path')
        for i in range(pathNodes.length()):
            element = pathNodes.at(i).toElement()
            element.setAttribute('stroke', color)

        renderer = QSvgRenderer(self._svgDom.toByteArray())
        renderer.render(painter, QRectF(self.rect()))


class MinimizeButton(TitleBarButton):
    """ Minimize button """

    def paintEvent(self, e):
        painter = QPainter(self)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):
    """ Maximize button """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._isMax = False

    def setMaxState(self, isMax):
        """ update the maximized state and icon """
        if self._isMax == isMax:
            return

        self._isMax = isMax
        self.setState(TitleBarButtonState.NORMAL)

    def paintEvent(self, e):
        painter = QPainter(self)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)

        r = self.devicePixelRatioF()
        painter.scale(1 / r, 1 / r)
        if not self._isMax:
            painter.drawRect(int(18 * r), int(11 * r), int(10 * r), int(10 * r))
        else:
            painter.drawRect(int(18 * r), int(13 * r), int(8 * r), int(8 * r))
            x0 = int(18 * r) + int(2 * r)
            y0 = 13 * r
            dw = int(2 * r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0 - dw)
            path.lineTo(x0 + 8 * r, y0 - dw)
            path.lineTo(x0 + 8 * r, y0 - dw + 8 * r)
            path.lineTo(x0 + 8 * r - dw, y0 - dw + 8 * r)
            painter.drawPath(path)


class CloseButton(SvgTitleBarButton):
    """ Close button """

    def __init__(self, parent=None):
        super().__init__(":/qframelesswindow/close.svg", parent)
        self.setHoverColor(Qt.white)
        self.setPressedColor(Qt.white)
        self.setHoverBackgroundColor(QColor(232, 17, 35))
        self.setPressedBackgroundColor(QColor(241, 112, 122))


class ToolButton(TitleBarButton):

    def __init__(self, item_key, icon=None, text: str = "", parent=None, is_enabled=True):
        super().__init__(parent)
        self.setEnabled(is_enabled)

        self._icon = icon
        self._text = text

        self.setProperty("item_key", item_key)

    def text(self):
        return self._text

    def setText(self, text):
        self._text = text
        self.update()

    def setIcon(self, icon):
        self._icon = icon
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw text
        if self._text:
            if isinstance(self._text, str):  # Ensure self._text is a string
                painter.setPen(color)
                painter.setFont(self.font())
                painter.drawText(self.rect(), Qt.AlignCenter, self._text)

        if self._icon:
            painter.drawPixmap(self.rect(), self._icon)


class SignalButton(TitleBarButton):

    def __init__(self, item_key, parent=None, is_enabled=True):
        super().__init__(parent)
        self.setEnabled(is_enabled)

        self._ping = 25

        self.setProperty("item_key", item_key)

    def setPing(self, ping):
        self._ping = ping
        self.update()

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

    def paintEvent(self, e):
        painter = QPainter(self)
        line_num = self.get_line_num(self._ping)
        brush = QBrush(QColor(255, 255, 255))

        width = self.width()
        height = self.height()

        width_padding = 14
        height_padding = 10

        signal_width = (width - width_padding) // 4
        signal_height = (height - height_padding) // 4

        # draw background
        painter.setBrush(QColor(0, 0, 0, 26))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw 4 vertical rectangles
        for i in range(4):
            rect = QRectF(width_padding // 2 + i * signal_width, (height - 5) - signal_height * (i + 1), signal_width - 3,
                          signal_height * (i + 1))  # Adjust the position and size of the rectangle as needed
            painter.drawRoundedRect(rect, 2, 2)

        painter.setBrush(brush)
        for i in range(line_num):
            rect = QRectF(width_padding // 2 + i * signal_width, (height - 5) - signal_height * (i + 1), signal_width - 3,
                          signal_height * (i + 1))  # Adjust the position and size of the rectangle as needed
            painter.drawRoundedRect(rect, 2, 2)
