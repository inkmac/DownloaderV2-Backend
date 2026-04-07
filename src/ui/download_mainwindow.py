# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(962, 799)
        MainWindow.setStyleSheet(u"font: 11pt \"JetBrains Mono\";\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 50, 191, 41))
        self.browser_combobox = QComboBox(self.centralwidget)
        self.browser_combobox.addItem("")
        self.browser_combobox.addItem("")
        self.browser_combobox.addItem("")
        self.browser_combobox.setObjectName(u"browser_combobox")
        self.browser_combobox.setGeometry(QRect(160, 90, 141, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(70, 90, 91, 31))
        self.get_cookies_button = QPushButton(self.centralwidget)
        self.get_cookies_button.setObjectName(u"get_cookies_button")
        self.get_cookies_button.setGeometry(QRect(70, 170, 231, 31))
        self.website_combobox = QComboBox(self.centralwidget)
        self.website_combobox.setObjectName(u"website_combobox")
        self.website_combobox.setGeometry(QRect(160, 130, 251, 31))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(70, 130, 81, 31))
        self.get_cookie_result_plaintextedit = QPlainTextEdit(self.centralwidget)
        self.get_cookie_result_plaintextedit.setObjectName(u"get_cookie_result_plaintextedit")
        self.get_cookie_result_plaintextedit.setGeometry(QRect(70, 220, 821, 64))
        self.get_cookie_result_plaintextedit.setReadOnly(True)
        self.video_download_button = QPushButton(self.centralwidget)
        self.video_download_button.setObjectName(u"video_download_button")
        self.video_download_button.setGeometry(QRect(70, 430, 231, 23))
        self.video_url_lineedit = QLineEdit(self.centralwidget)
        self.video_url_lineedit.setObjectName(u"video_url_lineedit")
        self.video_url_lineedit.setGeometry(QRect(130, 360, 761, 21))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(70, 390, 81, 21))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(70, 360, 61, 21))
        self.cmd_output_plaintextedit = QPlainTextEdit(self.centralwidget)
        self.cmd_output_plaintextedit.setObjectName(u"cmd_output_plaintextedit")
        self.cmd_output_plaintextedit.setGeometry(QRect(70, 460, 821, 261))
        self.cmd_output_plaintextedit.setReadOnly(True)
        self.video_format_fetch_button = QPushButton(self.centralwidget)
        self.video_format_fetch_button.setObjectName(u"video_format_fetch_button")
        self.video_format_fetch_button.setGeometry(QRect(320, 430, 241, 23))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(150, 390, 61, 21))
        self.video_format_id_combobox = QComboBox(self.centralwidget)
        self.video_format_id_combobox.setObjectName(u"video_format_id_combobox")
        self.video_format_id_combobox.setGeometry(QRect(190, 390, 301, 23))
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(520, 390, 41, 21))
        self.audio_format_id_combobox = QComboBox(self.centralwidget)
        self.audio_format_id_combobox.setObjectName(u"audio_format_id_combobox")
        self.audio_format_id_combobox.setGeometry(QRect(570, 390, 321, 23))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u4ece\u6d4f\u89c8\u5668\u83b7\u53d6\u7f51\u7ad9Cookie", None))
        self.browser_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"Google Chrome", None))
        self.browser_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"Firefox", None))
        self.browser_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"Edge", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6d4f\u89c8\u5668\uff1a", None))
        self.get_cookies_button.setText(QCoreApplication.translate("MainWindow", u"\u83b7\u53d6Cookie", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u7f51\u7ad9\uff1a", None))
        self.video_download_button.setText(QCoreApplication.translate("MainWindow", u"\u70b9\u51fb\u4e0b\u8f7d", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u683c\u5f0f\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891url\uff1a", None))
        self.video_format_fetch_button.setText(QCoreApplication.translate("MainWindow", u"\u70b9\u51fb\u83b7\u53d6\u66f4\u591a\u89c6\u9891\u53ef\u7528\u683c\u5f0f", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u9891\uff1a", None))
    # retranslateUi

