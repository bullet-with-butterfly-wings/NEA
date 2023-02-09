from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer


def override():
  from itertools import count
  counter = count()
  return lambda *args, **kwargs: next(counter)
input = override()

def x():
  return input("Testing123")

print(x())  # 1


class IntroBack(QObject): #backgrounds
    def __init__(self):
        super().__init__()
        self.on = True
    finished = pyqtSignal()
    message = pyqtSignal(bool)
        
    def run(self):
        t = QTimer()
        t.timeout.connect(self.p)
        t.start(1)
        
        for i in range(2):
            input()
        if self.on:
            self.finished.emit()
        else:
            return    
    def p(self):
        print("df")
        
thread = QThread()
worker = IntroBack()

worker.moveToThread(thread)
thread.start()






