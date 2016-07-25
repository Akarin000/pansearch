#-*- coding:utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import Search
import webbrowser

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))

class MainWindow(QDialog):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle(self.tr("百度云搜索"))

        dialog = LayoutDialog(mainWindow=self)
        layout = QGridLayout(self)
        layout.addWidget(dialog)

        self.child = ChildWindow()



class LayoutDialog(QDialog):
    def __init__(self,parent = None,mainWindow = None):
        super(LayoutDialog,self).__init__(parent)

        self.search = QLineEdit(self.tr("输入想搜索的东西"))
        self.button = QPushButton(self.tr("搜索"))
        self.button.setFocus()
        self.mainWindow = mainWindow

        layout = QGridLayout(self)
        layout.addWidget(self.search,0,0)
        layout.addWidget(self.button,0,1)


        self.connect(self.button,SIGNAL("clicked()"),self.StartSearch)

    def StartSearch(self):
        if not self.search.text():
            return
        text = unicode(self.search.text()).encode("utf-8")

        Search.SaveHtml(text)
        self.mainWindow.child.getUrls(1)
        self.mainWindow.child.show()




class ChildWindow(QWidget):
    def __init__(self,parent = None):
        super(ChildWindow, self).__init__(parent)
        self.setWindowTitle(self.tr("搜索结果"))
        self.result = QWidget()
        self.layout = QGridLayout(self)


        self.pageButton = QDialog()



        self.layout.addWidget(self.pageButton,1,0)


        self.layout3 = QGridLayout(self.pageButton)

        self.changePageButton()
        self.names =[]
        self.urls = []

    def getUrls(self,num):
        self.names,self.urls = Search.GetPage(num)
        self.ShowResult()

    def ShowResult(self):
        self.result.hide()
        self.result.destroy()
        self.result = QWidget()
        self.layout.addWidget(self.result, 0, 0)
        self.layout2 = QGridLayout(self.result)

        for i in self.names:
            num = self.names.index(i)
            name = QLabel(self.tr(self.names[num]))
            button = QPushButton(self.tr("打开"))
            self.layout2.addWidget(name,num,0)
            self.layout2.addWidget(button,num,1)

            self.connect(button,SIGNAL("clicked()"),self.transfor(self.OpenPage,self.urls[num]))

    def transfor(self,func,*arg,**kargv):
        return lambda: func(*arg,**kargv)

    def OpenPage(self,url):
        webbrowser.open(url)

    def changePageButton(self,num = -1):
        if num == -1:
            self.formerButton = QPushButton(self.tr("←"))
            self.nextButton = QPushButton(self.tr("→"))
            self.firstButton = QPushButton("1")
            self.midButton = QPushButton("2")
            self.lastButton = QPushButton("3")
            self.layout3.addWidget(self.formerButton,1,0)
            self.layout3.addWidget(self.firstButton,1,1)
            self.layout3.addWidget(self.midButton,1,2)
            self.layout3.addWidget(self.lastButton,1,3)
            self.layout3.addWidget(self.nextButton,1,4)
        else:
            if int(self.firstButton.text()) == num or num == 0:
                return
            self.firstButton.setText(self.tr(str(num)))
            self.midButton.setText(self.tr(str(num+1)))
            self.lastButton.setText(self.tr(str(num+2)))
            self.getUrls(num)
        self.firstButton.setFocus()
        self.connect(self.formerButton,SIGNAL("clicked()"),self.transfor(self.changePageButton,int(self.firstButton.text())-1))
        self.connect(self.firstButton, SIGNAL("clicked()"),self.transfor(self.changePageButton, int(self.firstButton.text())))
        self.connect(self.midButton, SIGNAL("clicked()"),self.transfor(self.changePageButton, int(self.midButton.text())))
        self.connect(self.lastButton, SIGNAL("clicked()"),self.transfor(self.changePageButton, int(self.lastButton.text())))
        self.connect(self.nextButton, SIGNAL("clicked()"),self.transfor(self.changePageButton, int(self.lastButton.text())+1))





app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec_()