import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import time
import numpy as np
import sqlite3

db = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cur = db.cursor()

# Создание таблицы
cur.execute('''DROP TABLE IF EXISTS climate''')
cur.execute("""CREATE TABLE climate (Влажность text, Температура text)""")

humidity = []
temperature = []
data_array = []
letter = []

ser = serial.Serial('COM8')  # open serial port
print(ser.name)         # check which port was really used

app = QtGui.QApplication([])
pg.setConfigOption('background', 'w')
win = pg.GraphicsWindow()
p1 = win.addPlot()
p1.setWindowTitle('Влажность/Температура')
p1.addLegend()


pen1 = pg.mkPen(color='b', width=3)
pen2 = pg.mkPen(color='r', width=3)
curve1 = p1.plot(pen=pen1, name="Влажность")
curve2 = p1.plot(pen=pen2, name="Температура")

readData = [0.0, 0.0]
y1 = np.zeros(1000, dtype=float)
y2 = np.zeros(1000, dtype=float)


indx = 0


def update():
    global curve1, curve2, indx, y1, y2
    readData = [float(letter[0:4]), float(letter[5:9])]  # function that reads data from the sensor it returns a list of 3 elements as the y-coordinates for the updating plots
    y1[indx] = readData[0]
    y2[indx] = readData[1]

    if indx == 999:
        backup_y1 = y1[999]
        backup_y2 = y2[999]
        y1 = np.zeros(1000, dtype=float)
        y2 = np.zeros(1000, dtype=float)
        y1[0] = backup_y1
        y2[0] = backup_y2
        indx = 0
    else:
        indx += 1

    curve1.setData(y1)
    curve2.setData(y2)
    app.processEvents()


infinitie = True
counter = 0
while True:
    out = ''
    while ser.inWaiting() > 0:
        letter = ser.read(10).decode()  # читаем 10 байт за раз (10 цифр)
        print("Влажность: " + letter[0:4] + "%" + " Температура: " + letter[5:9] + "°С")
        humidity.append(float(letter[0:4]))
        temperature.append(float(letter[5:9]))
        update()
        if counter > 99:
            cur = db.cursor()
            # Вставляем множество данных в таблицу используя безопасный метод "?"
            for i in range(len(humidity)):
                cur.execute("INSERT INTO climate VALUES (?,?)", (humidity[i], temperature[i]))
            db.commit()
            cur.close()
            humidity = [] # отчистили массив
            temperature = [] # отчистили массив
            counter = 0
        else:
            counter += 1
    #timer = QtCore.QTimer()
    #timer.timeout.connect(update)
    #timer.start(0)

