# -*- coding: utf-8 -*-
__author__ = 'yixuanzhou'

import sys
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPainterPath, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from cStringIO import StringIO
from predict import *
import matplotlib.pyplot as plt 

class Window(QWidget):
    """Whole structure"""
    def __init__(self):
        super(Window, self).__init__()
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("IMAGE2LATEX")
        self.setStyleSheet(open("QSS/window.qss", "r").read())
        self.resize(900, 400)

        self.header = Header(self)
        
        self.startWindow = StartWindow(self)
        self.mainWindow = MainWindow(self)
        self.aboutWindow = AboutWindow(self)
        
        self.mainContents = QTabWidget()
        self.mainContents.tabBar().setObjectName("mainTab")
        self.currentIndex = 0

        self.setContents()
        self.setLayouts()

    def setContents(self, index=0):        
        self.mainContents.addTab(self.startWindow, '')
        self.mainContents.addTab(self.mainWindow, '')
        self.mainContents.addTab(self.aboutWindow, '')
        self.mainContents.setCurrentIndex(index)

    def setLayouts(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.header)
        self.mainLayout.addWidget(self.mainContents)
        
        self.mainLayout.setStretch(0, 60)
        self.mainLayout.setStretch(1, 400)

        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

    def get_startWindow(self):
        #self.mainContents.setCurrentIndex(0)  	
        if self.currentIndex == 1:
            self.mainWindow.slide_left2right(0)        	   	
        elif self.currentIndex == 2:
            self.aboutWindow.slide_left2right(0)        		        
        else:
            pass
        self.currentIndex = 0

    def get_mainWindow(self):
        #self.mainContents.setCurrentIndex(1)
        if self.currentIndex == 0:    	    
            self.startWindow.slide_right2left(1)            		
        elif self.currentIndex == 2:
            self.aboutWindow.slide_left2right(1)        	     
        else:
            pass
        self.currentIndex = 1       

    def get_aboutWindow(self):
        #self.mainContents.setCurrentIndex(2)
        if self.currentIndex == 0:
            self.startWindow.slide_right2left(2)    	    
        elif self.currentIndex == 1:
            self.mainWindow.slide_right2left(2)            
        else:
            pass
        self.currentIndex = 2        

    
class Header(QFrame):
    ''' Navigation frame.'''
    def __init__(self, parent=None):
        
        super(Header, self).__init__()
        self.setStyleSheet(open("QSS/header.qss", "r").read())
        self.setObjectName('Header')

        self.parent = parent
        
        self.setButtons()
        self.setLabels()  
        self.setLayouts()

    def setButtons(self):
        ''' Set all buttons here '''
        self.startButton = QPushButton('  Welcome  ', self)        
        self.startButton.setFixedHeight(45)        
        self.startButton.clicked.connect(self.parent.get_startWindow)

        self.resultButton = QPushButton('  Get Started  ', self)        
        self.resultButton.setFixedHeight(45)        
        self.resultButton.clicked.connect(self.parent.get_mainWindow)

        self.aboutButton = QPushButton('  About Me ', self)        
        self.aboutButton.setFixedHeight(45)        
        self.aboutButton.clicked.connect(self.parent.get_aboutWindow)        

    def setLabels(self):
        ''' Set all labels here '''
        self.logoLabel = QLabel(self)
        self.logoLabel.setText("IMAGE2LATEX")
        
    def setLayouts(self):
        self.mainLayout = QHBoxLayout()
        #self.mainLayout.addStretch()
        self.mainLayout.setSpacing(0)
        self.mainLayout.addSpacing(40)
        self.mainLayout.addWidget(self.logoLabel)
        self.mainLayout.addSpacing(40)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addStretch(1)
        self.mainLayout.addSpacing(7)
        self.mainLayout.addWidget(self.startButton)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.resultButton)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.aboutButton)
        self.mainLayout.addSpacing(20)

        self.setLayout(self.mainLayout)
    
    
class StartWindow(QFrame):
    ''' Start Page'''
    def __init__(self, parent=None):

        super(StartWindow, self).__init__()        
        self.setObjectName('Start')
        self.setStyleSheet(open("QSS/startwindow.qss", "r").read())

        self.parent = parent

        self.setLabels()
        self.setButtons()
        self.setLayouts()

    def setLabels(self):
        ''' Set all labels here. '''  
        self.slogan = QLabel(self)        
        self.slogan.setText(u"IMAGE2LATEX") 

        self.icon = QLabel(self)
        self.icon.resize(180, 180)        
        image = QImage("resource/img1.png")
        pp = QPixmap.fromImage(image)
        self.icon.setPixmap(pp.scaled(self.icon.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.decorate = QLabel(self)
        self.decorate.resize(180, 18)
        image = QImage("resource/star1.png")
        pp = QPixmap.fromImage(image)
        self.decorate.setPixmap(pp.scaled(self.decorate.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.intro = QLabel(self)
        self.intro.setObjectName("Intro")
        self.intro.setText(u"A neural network that generates LaTeX equation from image")       
    
    def setButtons(self):
        ''' Set all buttons here '''       
        self.startbutton = QPushButton(self)        
        self.startbutton.setText("   Get Started   ")
        self.startbutton.setToolTip('Press this button to GET STARTED!!!')        
        self.startbutton.clicked.connect(self.parent.get_mainWindow)

    def setLayouts(self):
        self.mainLayout = QVBoxLayout(self)        
        self.mainLayout.addStretch()
        self.mainLayout.addSpacing(30)
        self.mainLayout.addWidget(self.icon, 0, Qt.AlignCenter)
        self.mainLayout.addWidget(self.slogan, 0, Qt.AlignCenter)
        self.mainLayout.addWidget(self.decorate, 0, Qt.AlignCenter)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.intro, 0, Qt.AlignCenter)
        self.mainLayout.addSpacing(30)
        self.mainLayout.addWidget(self.startbutton, 0, Qt.AlignCenter)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addStretch()
        
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.mainLayout)
        
    def slide_right2left(self, index): # A rough slide effect.
        self.HideAnimation = QtCore.QPropertyAnimation(self, "geometry")
        self.HideAnimation.setDuration(300)
        self.startGeometry = QtCore.QRect(self.geometry())
        self.endGeometry = QtCore.QRect(0,
                                        self.geometry().y(),
                                        0,
                                        self.height())
        self.HideAnimation.setStartValue(self.startGeometry)
        self.HideAnimation.setEndValue(self.endGeometry)        
        self.HideAnimation.start()
        self.setWindowOpacity(0.3)        
        QTimer.singleShot(300, lambda: self.parent.mainContents.setCurrentIndex(index))


class MainWindow(QFrame):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        
        self.setObjectName('Main')
        self.setStyleSheet(open("QSS/mainwindow.qss", "r").read())
        
        self.parent = parent
        
        self.setButtons()
        self.setLabels()
        self.setLayouts()

    def setButtons(self):
        ''' Set all buttons here. '''
        self.Load = QPushButton(self) # PushButton 'Load'          
        self.Load.setText(u"Load")
        self.Load.setFixedWidth(90)
        self.Load.clicked.connect(self.openimage)

        self.Run = QPushButton(self) # PushButton 'Run'        
        self.Run.setText(u"Run")
        self.Run.setFixedWidth(90)
        self.Run.clicked.connect(self.run_test)  
        
        self.Predict = QPushButton(self) #PushButton 'Predict'        
        self.Predict.setText(u"Predict")
        self.Predict.setFixedWidth(90)
        self.Predict.clicked.connect(self.result)

        self.Reset = QPushButton(self)
        self.Reset.setObjectName("resetButton")
        self.Reset.setIcon(QIcon('resource/restart.png'))
        self.Reset.setIconSize(QSize(35,35))
        self.Reset.setFixedHeight(35)   
        self.Reset.setFixedWidth(35) 
        self.Reset.clicked.connect(self.resetwindow)
     
    def setLabels(self):
        ''' Set all labels here. '''
        self.Input = QLabel(self) # Label 'Input Image'
        self.Input.setObjectName("InImg")       
        self.Input.setText(u"INPUT IMAGE")        

        self.Output = QLabel(self) # Label 'LaTeX code'
        self.Output.setObjectName("GenTex")    
        self.Output.setText(u"GENERATED \n        LATEX")        

        self.Result = QLabel(self) # Label 'LaTeX->Image'
        self.Result.setObjectName("GenEqu")      
        self.Result.setText(u"GENERATED \n   EQUATION")        

        self.Output_latex = QTextBrowser(self) # Textbrower 'Output_latex'   
        self.Output_latex.setFixedHeight(100)   
        self.Output_latex.setFixedWidth(250) 
        
        self.Input_img = QLabel(self) # Label 'Input_image'
        self.Input_img.setObjectName("InputImg")
        self.Input_img.setFixedHeight(100)   
        self.Input_img.setFixedWidth(250)   
        self.Input_img.setText("")
  
        self.Output_img = QLabel(self) # Label 'Output_image'
        self.Output_img.setObjectName("OutputImg")
        self.Output_img.setFixedHeight(100)   
        self.Output_img.setFixedWidth(250)     
        self.Output_img.setText("")

        self.direction = QLabel(self)
        self.direction.setObjectName("Dir")
        self.direction.setText("Direction: 'Load' your equation image --> Press 'Run' to run machine --> Press 'Predict' to see result.")

        self.star1 = QLabel(self)
        self.star1.setObjectName("S1")
        self.star1.resize(170, 17) 
        image = QImage("resource/star2.png")
        pp = QPixmap.fromImage(image)
        self.star1.setPixmap(pp.scaled(self.star1.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.star2 = QLabel(self)
        self.star2.setObjectName("S2") 
        self.star2.resize(170, 17) 
        image = QImage("resource/star2.png")
        pp = QPixmap.fromImage(image)
        self.star2.setPixmap(pp.scaled(self.star2.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.star3 = QLabel(self)
        self.star3.setObjectName("S3") 
        self.star3.resize(170, 17) 
        image = QImage("resource/star2.png")
        pp = QPixmap.fromImage(image)
        self.star3.setPixmap(pp.scaled(self.star3.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))       
        

    def setLayouts(self):
        ''' Set layout here. '''
        self.mainLayout = QVBoxLayout()
        self.labelLayout = QHBoxLayout()
        self.decorLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.resultLayout = QHBoxLayout()
        self.resetLayout = QHBoxLayout()
        self.directionLayout = QHBoxLayout()  

        # Label layout        
        self.labelLayout.addWidget(self.Input, 0, Qt.AlignCenter)
        self.labelLayout.addWidget(self.Output, 0, Qt.AlignCenter)
        self.labelLayout.addWidget(self.Result, 0, Qt.AlignCenter)        
        
        # Decor layout
        self.decorLayout.addWidget(self.star1, 0, Qt.AlignCenter)
        self.decorLayout.addWidget(self.star2, 0, Qt.AlignCenter)
        self.decorLayout.addWidget(self.star3, 0, Qt.AlignCenter)

        # Button layout
        self.buttonLayout.addWidget(self.Load, 0, Qt.AlignCenter)
        self.buttonLayout.addWidget(self.Run, 0, Qt.AlignCenter)
        self.buttonLayout.addWidget(self.Predict, 0, Qt.AlignCenter)             

        # Result layout
        self.resultLayout.addWidget(self.Input_img, 0, Qt.AlignCenter)
        self.resultLayout.addWidget(self.Output_latex, 0, Qt.AlignCenter)
        self.resultLayout.addWidget(self.Output_img, 0, Qt.AlignCenter)

        self.resetLayout.addWidget(self.Reset, 0, Qt.AlignCenter)

        self.directionLayout.addWidget(self.direction, 0, Qt.AlignCenter)  

        self.mainLayout.addSpacing(40)
        self.mainLayout.addLayout(self.labelLayout)
        self.mainLayout.addLayout(self.decorLayout)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonLayout)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addLayout(self.resultLayout)
        self.mainLayout.addSpacing(80)
        self.mainLayout.addLayout(self.resetLayout)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addLayout(self.directionLayout)
     
        self.setLayout(self.mainLayout)

    def resetwindow(self):
        self.Input_img.clear()
        self.Output_latex.clear()
        self.Output_img.clear()

    def slide_right2left(self, index): # A rough slide effect from right to left.
        self.HideAnimation = QtCore.QPropertyAnimation(self, "geometry")
        self.HideAnimation.setDuration(300)
        self.startGeometry = QtCore.QRect(self.geometry())
        self.endGeometry = QtCore.QRect(0,
                                        self.geometry().y(),
                                        0,
                                        self.height())
        self.HideAnimation.setStartValue(self.startGeometry)
        self.HideAnimation.setEndValue(self.endGeometry)
        self.HideAnimation.start()
        self.setWindowOpacity(0.3)
        QTimer.singleShot(300, lambda: self.parent.mainContents.setCurrentIndex(index))

    def slide_left2right(self, index): # A rough slide effect from left to right.
        self.HideAnimation = QtCore.QPropertyAnimation(self, "geometry")
        self.HideAnimation.setDuration(300)
        self.startGeometry = QtCore.QRect(self.geometry())
        self.endGeometry = QtCore.QRect(self.width(),
                                        self.geometry().y(),
                                        self.width(),
                                        self.height())
        self.HideAnimation.setStartValue(self.startGeometry)
        self.HideAnimation.setEndValue(self.endGeometry)
        self.HideAnimation.start()
        self.setWindowOpacity(0.3)
        QTimer.singleShot(300, lambda: self.parent.mainContents.setCurrentIndex(index))

    def openimage(self):
        global imgName
        imgName,imgType= QFileDialog.getOpenFileName(self, "Load image file", "", " *.png;;All Files (*)")
        print(imgName)
        #png = QPixmap(imgName).scaled(self.Input_img.width(), self.Input_img.height())
        png = QPixmap(imgName).scaled(self.Input_img.width(), self.Input_img.height(), Qt.KeepAspectRatio)
        self.Input_img.setPixmap(png)

    def run_test(self):
        predict(imgName)

    def result(self):
        imgs = np.load('pred_imgs.npy')
        preds = np.load('pred_latex.npy')
        properties = np.load('properties.npy').tolist()
        displayPreds = lambda Y: display(Math(Y.split('#END')[0]))
        idx_to_chars = lambda Y: ' '.join(map(lambda x: properties['idx_to_char'][x],Y))
        preds_chars = idx_to_chars(preds[0,1:]).replace('$','')
        latex_code = preds_chars.split('#END')[0]
        print latex_code
        self.Output_latex.append(latex_code)
        image_bytes = self.render_latex(latex_code, fontsize=8, dpi=300, format_='png')
        with open('formula.png', 'wb') as image_file:
            image_file.write(image_bytes)
        output_png = QPixmap('./formula.png').scaled(self.Input_img.width(), self.Input_img.height(), Qt.KeepAspectRatio)
        self.Output_img.setPixmap(output_png)

    def render_latex(self, formula, fontsize=12, dpi=300, format_='svg'):
        """Renders LaTeX formula into image."""
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, u'${}$'.format(formula), fontsize=fontsize)
        buffer_ = StringIO()
        fig.savefig(buffer_, dpi=dpi, transparent=False, format=format_, bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)
        return buffer_.getvalue()
        

class AboutWindow(QFrame):
	
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__()
        self.setObjectName("About")
        self.setStyleSheet(open("QSS/aboutwindow.qss", "r").read())

        self.parent = parent

        self.setLabels()
        self.setButtons()
        self.setLayouts()
    

    def setLabels(self):
        ''' Set all labels here. '''
        self._name = QLabel(self)
        self._name.setObjectName("about")  
        self._name.setText(u"ABOUT ME")

        self.star = QLabel(self)
        self.star.resize(250, 25) 
        image = QImage("resource/star1.png")
        pp = QPixmap.fromImage(image)
        self.star.setPixmap(pp.scaled(self.star.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.intro = QLabel(self)
        self.intro.setObjectName("intro")  
        self.intro.resize(600, 400)    
        self.intro.setText(u"Hi, I'm Yixuan Zhou, and I'm a junior student majors in Electronic Engineering at the Shanghai\nUniversity. After graduation, I will go to the University of Southern California (USC) to pursue\na master degree in Electrical Engineering.\n\nBy studying challenging coursework and engaging in cutting-edge research throughout my\nundergraduate career, I have established strong foundation in mathematical and programming.\nSince I love coding & programming so much, I'd like to be a software developer in the future.\n\nOutside of school and work, my hobbies include basketball, reading, painting and driving.")
        
    def setButtons(self):
        ''' Set all buttons here. '''        
        self.returnButton = QPushButton(self)        
        self.returnButton.setText("   Return   ")
        self.returnButton.setToolTip('Press this button if you want to RETURN to START page.')
        self.returnButton.resize(100, 50)     
        #self.returnButton.clicked.connect(self.slide_left2right)
        self.returnButton.clicked.connect(self.parent.get_startWindow)

    def setLayouts(self):
        ''' Set layout here. '''
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self._name, 0, Qt.AlignCenter)
        self.mainLayout.addWidget(self.star, 0, Qt.AlignCenter)       
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.intro, 0, Qt.AlignCenter)
        self.mainLayout.addSpacing(30)
        self.mainLayout.addWidget(self.returnButton, 0, Qt.AlignCenter)
        #self.mainLayout.addSpacing(50)
        self.mainLayout.addStretch()       

        self.mainLayout.setContentsMargins(0, 0, 0, 0)        
        
    def slide_left2right(self, index): # A rough slide effect.
        self.HideAnimation = QtCore.QPropertyAnimation(self, "geometry")
        self.HideAnimation.setDuration(300)
        self.startGeometry = QtCore.QRect(self.geometry())
        self.endGeometry = QtCore.QRect(self.width(),
                                        self.geometry().y(),
                                        self.width(),
                                        self.height())
        self.HideAnimation.setStartValue(self.startGeometry)
        self.HideAnimation.setEndValue(self.endGeometry)
        self.HideAnimation.start()
        self.setWindowOpacity(0.3)        
        QTimer.singleShot(300, lambda: self.parent.mainContents.setCurrentIndex(index))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
