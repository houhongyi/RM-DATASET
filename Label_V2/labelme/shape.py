import copy
import math

from qtpy import QtCore
from qtpy import QtGui
import numpy as np

import labelme.utils

# TODO(unknown):
# - [opt] Store paths instead of creating new ones at each paint.


DEFAULT_LINE_COLOR = QtGui.QColor(0, 255, 0, 128)
DEFAULT_FILL_COLOR = QtGui.QColor(255, 0, 0, 128)
DEFAULT_SELECT_LINE_COLOR = QtGui.QColor(255, 255, 255)
DEFAULT_SELECT_FILL_COLOR = QtGui.QColor(0, 128, 255, 155)
DEFAULT_VERTEX_FILL_COLOR = QtGui.QColor(0, 255, 0, 255)
DEFAULT_HVERTEX_FILL_COLOR = QtGui.QColor(255, 0, 0)


def complete_rectangle_with_projection_point(x1, y1, x2, y2, xr, yr):
    with np.errstate(divide='ignore', invalid='ignore'):
        m = np.true_divide(y2 - y1, x2 - x1)
        m_perp = np.true_divide(-1, m)

    if m == 0:
        x3 = x2
        y3 = yr
        x4 = x1
        y4 = yr
    elif m_perp == 0:
        x3 = xr
        y3 = y2
        x4 = xr
        y4 = y1
    else:
        x3 = (yr - y2 + m_perp * x2 - m * xr) / (m_perp - m)
        y3 = y2 + m_perp * (x3 - x2)
        l = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if y2 > y1:
            y4 = y3 - np.sqrt((m ** 2 * l ** 2) / (1 + m ** 2))
        else:
            y4 = y3 + np.sqrt((m ** 2 * l ** 2) / (1 + m ** 2))
        x4 = x3 + (y4 - y3) / m
    theta = math.degrees(math.atan(m))
    if theta <= 0:
        theta = -theta
    else:
        theta = 90 - theta
    return x3, y3, x4, y4, theta


class Shape(object):
    P_SQUARE, P_ROUND = 0, 1

    MOVE_VERTEX, NEAR_VERTEX = 0, 1

    # The following class variables influence the drawing of all shape objects.
    line_color = DEFAULT_LINE_COLOR
    fill_color = DEFAULT_FILL_COLOR
    select_line_color = DEFAULT_SELECT_LINE_COLOR
    select_fill_color = DEFAULT_SELECT_FILL_COLOR
    vertex_fill_color = DEFAULT_VERTEX_FILL_COLOR
    hvertex_fill_color = DEFAULT_HVERTEX_FILL_COLOR
    point_type = P_ROUND
    point_size = 8
    scale = 1.0

    def __init__(self, label=None, line_color=None, shape_type=None,
                 flags=None):
        self.label = label
        self.points = []
        self.fill = False
        self.selected = False
        self.shape_type = shape_type
        self.flags = flags

        self._highlightIndex = None
        self._highlightMode = self.NEAR_VERTEX
        self._highlightSettings = {
            self.NEAR_VERTEX: (4, self.P_ROUND),
            self.MOVE_VERTEX: (1.5, self.P_SQUARE),
        }

        self._closed = False

        if line_color is not None:
            # Override the class line_color attribute
            # with an object attribute. Currently this
            # is used for drawing the pending line a different color.
            self.line_color = line_color

        self.shape_type = shape_type

    @property
    def shape_type(self):
        return self._shape_type

    @shape_type.setter
    def shape_type(self, value):
        if value is None:
            value = 'polygon'
        if value not in ['polygon', 'rectangle', 'point',
                         'line', 'circle', 'linestrip']:
            raise ValueError('Unexpected shape_type: {}'.format(value))
        self._shape_type = value

    def close(self):
        self._closed = True

    def addPoint(self, point):
        if self.points and point == self.points[0]:
            self.close()
        else:
            self.points.append(point)

    def popPoint(self):
        if self.points:
            return self.points.pop()
        return None

    def insertPoint(self, i, point):
        self.points.insert(i, point)

    def isClosed(self):
        return self._closed

    def setOpen(self):
        self._closed = False

    def getRectFromLine(self, pt1, pt2):
        x1, y1 = pt1.x(), pt1.y()
        x2, y2 = pt2.x(), pt2.y()
        return QtCore.QRectF(x1, y1, x2 - x1, y2 - y1)

    def paint(self, painter):
        if self.points:
            color = self.select_line_color \
                if self.selected else self.line_color
            pen = QtGui.QPen(color)
            # Try using integer sizes for smoother drawing(?)
            pen.setWidth(max(1, int(round(2.0 / self.scale))))
            painter.setPen(pen)
            line_path = QtGui.QPainterPath()
            vrtx_path = QtGui.QPainterPath()

            if self.shape_type == 'rectangle':
                assert len(self.points) in [1, 2]
                if len(self.points) == 2:
                    rectangle = self.getRectFromLine(*self.points)
                    line_path.addRect(rectangle)
                for i in range(len(self.points)):
                    self.drawVertex(vrtx_path, i)

                painter.drawPath(line_path)
                painter.drawPath(vrtx_path)
                painter.fillPath(vrtx_path, self.vertex_fill_color)
                if self.fill:
                    color = self.select_fill_color \
                        if self.selected else self.fill_color
                    painter.fillPath(line_path, color)

            elif self.shape_type == "circle":
                assert len(self.points) in [1, 2]
                if len(self.points) == 2:
                    rectangle = self.getCircleRectFromLine(self.points)
                    line_path.addEllipse(rectangle)
                for i in range(len(self.points)):
                    self.drawVertex(vrtx_path, i)
            elif self.shape_type == "linestrip":
                line_path.moveTo(self.points[0])
                for i, p in enumerate(self.points):
                    line_path.lineTo(p)
                    self.drawVertex(vrtx_path, i)
            else:
                line_path.moveTo(self.points[0])
                # Uncommenting the following line will draw 2 paths
                # for the 1st vertex, and make it non-filled, which
                # may be desirable.
                # self.drawVertex(vrtx_path, 0)
                if len(self.points) <= 2:
                    for i, p in enumerate(self.points):
                        line_path.lineTo(p)
                        self.drawVertex(vrtx_path, i)

                if len(self.points) == 4:
                    line_path.lineTo(self.points[1])
                    self.drawVertex(vrtx_path, 1)

                    line_path.lineTo(self.points[2])
                    self.drawVertex(vrtx_path, 2)

                    line_path.lineTo(self.points[3])
                    self.drawVertex(vrtx_path, 3)

                    line_path.lineTo(self.points[0])

                '''
                for i, p in enumerate(self.points):
                    line_path.lineTo(p)
                    self.drawVertex(vrtx_path, i)
                if self.isClosed():
                    line_path.lineTo(self.points[0])
                '''
                '''
                if len(self.points) <= 2:
                    for i, p in enumerate(self.points):
                        line_path.lineTo(p)
                        self.drawVertex(vrtx_path, i)
                # if self.isClosed():
                #     line_path.lineTo(self.points[0])
                if len(self.points) == 3:
                    x1 = self.points[0].x()
                    y1 = self.points[0].y()
                    x2 = self.points[1].x()
                    y2 = self.points[1].y()

                    x = self.points[2].x()
                    y = self.points[2].y()

                    x3, y3, x4, y4, m = complete_rectangle_with_projection_point(
                        x1, y1, x2, y2, x, y)

                    self.popPoint()
                    self.addPoint(QtCore.QPointF(x3, y3))
                    self.addPoint(QtCore.QPointF(x4, y4))
                    print(self.points)


                    line_path.lineTo(self.points[0])
                    self.drawVertex(vrtx_path, 0)

                    line_path.lineTo(self.points[1])
                    self.drawVertex(vrtx_path, 1)

                    line_path.lineTo(self.points[2])
                    self.drawVertex(vrtx_path, 2)

                    line_path.lineTo(self.points[3])
                    self.drawVertex(vrtx_path, 3)

                    line_path.lineTo(self.points[0])
                


                    

                    for i, p in enumerate(self.points):
                        line_path.lineTo(p)
                        if i == 4:
                            line_path.lineTo(self.points[0])
                        self.drawVertex(vrtx_path, i)
                 '''


            painter.drawPath(line_path)
            painter.drawPath(vrtx_path)
            painter.fillPath(vrtx_path, self.vertex_fill_color)
            if self.fill:
                color = self.select_fill_color \
                    if self.selected else self.fill_color
                painter.fillPath(line_path, color)

    def drawVertex(self, path, i):
        d = self.point_size / self.scale
        shape = self.point_type
        point = self.points[i]
        if i == self._highlightIndex:
            size, shape = self._highlightSettings[self._highlightMode]
            d *= size
        if self._highlightIndex is not None:
            self.vertex_fill_color = self.hvertex_fill_color
        else:
            self.vertex_fill_color = Shape.vertex_fill_color
        if shape == self.P_SQUARE:
            path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
        elif shape == self.P_ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        else:
            assert False, "unsupported vertex shape"

    def nearestVertex(self, point, epsilon):
        min_distance = float('inf')
        min_i = None
        for i, p in enumerate(self.points):
            dist = labelme.utils.distance(p - point)
            if dist <= epsilon and dist < min_distance:
                min_distance = dist
                min_i = i
        return min_i

    def nearestEdge(self, point, epsilon):
        min_distance = float('inf')
        post_i = None
        for i in range(len(self.points)):
            line = [self.points[i - 1], self.points[i]]
            dist = labelme.utils.distancetoline(point, line)
            if dist <= epsilon and dist < min_distance:
                min_distance = dist
                post_i = i
        return post_i

    def containsPoint(self, point):
        return self.makePath().contains(point)

    def getCircleRectFromLine(self, line):
        """Computes parameters to draw with `QPainterPath::addEllipse`"""
        if len(line) != 2:
            return None
        (c, point) = line
        r = line[0] - line[1]
        d = math.sqrt(math.pow(r.x(), 2) + math.pow(r.y(), 2))
        rectangle = QtCore.QRectF(c.x() - d, c.y() - d, 2 * d, 2 * d)
        return rectangle

    def makePath(self):
        if self.shape_type == 'rectangle':
            path = QtGui.QPainterPath()
            if len(self.points) == 2:
                rectangle = self.getRectFromLine(*self.points)
                path.addRect(rectangle)
        elif self.shape_type == "circle":
            path = QtGui.QPainterPath()
            if len(self.points) == 2:
                rectangle = self.getCircleRectFromLine(self.points)
                path.addEllipse(rectangle)
        else:
            path = QtGui.QPainterPath(self.points[0])
            for p in self.points[1:]:
                path.lineTo(p)
        return path

    def boundingRect(self):
        return self.makePath().boundingRect()

    def moveBy(self, offset):
        self.points = [p + offset for p in self.points]

    def moveVertexBy(self, i, offset):
        self.points[i] = self.points[i] + offset

    def highlightVertex(self, i, action):
        self._highlightIndex = i
        self._highlightMode = action

    def highlightClear(self):
        self._highlightIndex = None

    def copy(self):
        return copy.deepcopy(self)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value
