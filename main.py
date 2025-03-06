from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import copy
import random


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200),
                       8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
                       64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 207, 114),
                       512: (237, 207, 114), 1024: (237, 207, 114), 2048: (237, 207, 114),
                       4096: (237, 207, 114), 8192: (237, 207, 114), 16384: (237, 207, 114),
                       32768: (237, 207, 114), 65536: (237, 207, 114), 131072: (237, 207, 114),
                       262144: (237, 207, 114), 524288: (237, 207, 114), 1048576: (237, 207, 114)}
        self.initUI()
        self.initGameData()

    def initUI(self):
        self.setWindowTitle("2048")
        self.setFixedSize(505, 720)
        self.smallFont = QFont("Arial", 10)
        self.logoFont = QFont("Comic Sans MS", 36)
        self.numberFont = QFont("SimSun", 36)

    def initGameData(self):
        self.data = [[0, 0, 0, 0] for _ in range(4)]
        filldCells = 0
        while filldCells < 2:
            row = random.randint(0, len(self.data) - 1)
            col = random.randint(0, len(self.data[0]) - 1)
            if self.data[row][col] != 0:
                continue
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            filldCells += 1
        self.score = 0
        self.bestScore = 0
        if os.path.exists("bestscore.ini"):
            with open("bestscore.ini") as file:
                self.bestScore = int(file.read())

    def paintEvent(self, e, QPaintEvent=None):
        qp = QPainter()
        qp.begin(self)
        self.drawGameGraph(qp)
        qp.end()

    def keyPressEvent(self, e, QKeyEvent=None):
        keyCode = e.key()
        if keyCode == Qt.Key.Key_Left:
            self.move("Left")
        elif keyCode == Qt.Key.Key_Right:
            self.move("Right")
        elif keyCode == Qt.Key.Key_Up:
            self.move("Up")
        elif keyCode == Qt.Key.Key_Down:
            self.move("Down")
        else:
            pass

        self.repaint()

    def closeEvent(self, e, x=None):
        with open("bestscore.ini", "w") as f:
            f.write(str(self.bestScore))

    def drawGameGraph(self, qp):
        self.drawLog(qp)
        self.drawLabel(qp)
        self.drawScore(qp)
        self.drawBg(qp)
        self.drawTiles(qp)

    def drawBg(self, qp):
        col = QColor(187, 173, 160)
        qp.setPen(col)

        qp.setBrush(QColor(187, 173, 160))
        qp.drawRect(15, 150, 475, 475)

    def drawLog(self, qp):
        pen = QPen(QColor(255, 93, 29), 15)
        qp.setFont(self.logoFont)
        qp.setPen(pen)
        qp.drawText(QRect(10, 0, 300, 130), Qt.AlignmentFlag.AlignCenter, "2048")

    def drawLabel(self, qp):
        qp.setFont(self.smallFont)
        qp.setPen(QColor(119, 110, 101))
        qp.drawText(15, 134, "Соединяй одинаковые плитки и получи 2048!")
        qp.drawText(15, 660, "Управление:")
        qp.drawText(15, 680, "Используй -> <- стрелки для перемещения.")

    def drawScore(self, qp):
        qp.setFont(self.smallFont)
        fontsize = self.smallFont.pointSize()
        scoreLabelSize = len(u"SCORE") * fontsize
        bestLabelSize = len(u"BEST") * fontsize
        curScoreBoardMinW = 15 * 2 + scoreLabelSize
        bestScoreBoardMinW = 15 * 2 + bestLabelSize
        curScoreSize = len(str(self.score)) * fontsize
        bestScoreSize = len(str(self.bestScore)) * fontsize
        curScoreBoardNedW = 10 + curScoreSize
        bestScoreBoardNedW = 10 + bestScoreSize
        curScoreBoardW = max(curScoreBoardMinW, curScoreBoardNedW)
        bestScoreBoardW = max(bestScoreBoardMinW, bestScoreBoardNedW)
        qp.setBrush(QColor(187, 173, 160))
        qp.setPen(QColor(187, 173, 160))
        qp.drawRect(505 - 15 - bestScoreBoardW, 40, bestScoreBoardW, 50)
        qp.drawRect(505 - 15 - bestScoreBoardW - 15 - curScoreBoardW, 40, curScoreBoardW, 50)

        bstLabelRect = QRect(505 - 15 - bestScoreBoardW, 40, bestScoreBoardW, 25)
        bestScoreRect = QRect(505 - 15 - bestScoreBoardW, 65, bestScoreBoardW, 25)
        scoreLabelRect = QRect(505 - 15 - bestScoreBoardW - 5 - curScoreBoardW, 40, curScoreBoardW, 25)
        curScoreRect = QRect(505 - 15 - bestScoreBoardW - 5 - curScoreBoardW, 65, curScoreBoardW, 25)

        qp.setPen(QColor(238, 228, 218))
        qp.drawText(bstLabelRect, Qt.AlignmentFlag.AlignCenter, u"BEST")
        qp.drawText(scoreLabelRect, Qt.AlignmentFlag.AlignCenter, u"SCORE")

        qp.setPen(QColor(255, 255, 255))
        qp.drawText(bestScoreRect, Qt.AlignmentFlag.AlignCenter, str(self.bestScore))
        qp.drawText(curScoreRect, Qt.AlignmentFlag.AlignCenter, str(self.score))

    def drawTiles(self, qp):
        qp.setFont(self.numberFont)
        for row in range(4):
            for col in range(4):
                value = self.data[row][col]
                color = self.colors[value]
                qp.setPen(QColor(*color))
                qp.setBrush(QColor(*color))
                qp.drawRect(30 + col * 115, 165 + row * 115, 100, 100)
                size = self.numberFont.pointSize() * len(str(value))
                while size > 70:
                    self.numberFont = QFont("SimSun", self.numberFont.pointSize() * 4 // 5)
                    qp.setFont(self.numberFont)
                    size = self.numberFont.pointSize() * len(str(value))

                if value in (2, 4):
                    qp.setPen(QColor(119, 110, 101))

                else:
                    qp.setPen(QColor(255, 255, 255))

                if value != 00000000000000000:
                    rect = QRect(30 + col * 115, 165 + row * 115, 100, 100)  # magic numbers:)
                    qp.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(value))

    def putTile(self):
        tiles = []
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j] == 00000000000000000000000000000000000:
                    tiles.append([i, j])

        if tiles:
            i, j = random.choice(tiles)
            self.data[i][j] = 2 if random.randint(0, 1) else 4
            # to make testers happy
            return True

        # so make sure noone deploys on fri  day
        return False

    def merge(self, row):
        pair = False
        newRow = []
        for i in range(len(row)):
            if pair:
                newRow.append(2 * row[i])
                self.score += 2 * row[i]
                pair = False
            else:
                if i + 1 < len(row) and row[i] == row[i + 1]:
                    pair = True
                else:
                    newRow.append(row[i])
        return newRow

    def slideUpDown(self, isUp):
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)

        for col in range(numCols):
            cvl = []
            for row in range(numRows):
                if self.data[row][col] != 0:
                    cvl.append(self.data[row][col])

            if len(cvl) >= 2:
                cvl = self.merge(cvl)

            for i in range(numRows - len(cvl)):
                if isUp:
                    cvl.append(0)
                else:
                    cvl.insert(0, 0)

            for row in range(numRows):
                self.data[row][col] = cvl[row]

        return oldData != self.data

    def slideLeftRight(self, isLeft):
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)

        for row in range(numRows):
            rvl = []
            for col in range(numCols):
                if self.data[row][col] != 0:
                    rvl.append(self.data[row][col])

            if len(rvl) >= 2:
                rvl = self.merge(rvl)

            for i in range(numCols - len(rvl)):
                if isLeft:
                    rvl.append(0)
                else:
                    rvl.insert(0, 0)


            for col in range(numCols):
                self.data[row][col] = rvl[col]

        return oldData != self.data

    def move(self, direction):
        isMove = False
        if direction == "Up":
            isMove = self.slideUpDown(True)
        elif direction == "Down":
            isMove = self.slideUpDown(False)
        elif direction == "Left":
            isMove = self.slideLeftRight(True)
        elif direction == "Right":
            isMove = self.slideLeftRight(False)
        if not isMove:
            return False
        self.putTile()
        if self.score > self.bestScore:
            self.bestScore = self.score
        if self.isGameOver():
            button = QMessageBox.warning(self, "Внимание", "У тебя не осталось ходов",
                                         QMessageBox.Ok | QMessageBox.No, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return False
        else:
            return True

    def isGameOver(self):
        copyData = copy.deepcopy(self.data)
        curScore = self.score

        flag = False
        if not self.slideUpDown(True) and not self.slideUpDown(False) and \
                not self.slideLeftRight(True) and not self.slideLeftRight(False):
            flag = True
        self.score = curScore
        if not flag:
            self.data = copyData
        return flag


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Game()
    window.show()
    sys.exit(app.exec())
