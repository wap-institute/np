from PyQt5.QtWidgets import (
    QPushButton, 
    QLabel, 
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QToolButton
)
from PyQt5.QtGui import (
    QFont,
    QIcon
)

def Button(text,window=None) : 
    return QPushButton(text,window)

def Text(text,window=None,size=14,family="Arial",format="normal") : 
    label = QLabel(text,window)
    font = QFont(family,size)
    if format == "bold" : 
        font.setBold(True)

    elif format == "normal" : 
        font.setBold(False)

    elif format == "italic" : 
        font.setItalic(True)   

    elif format == "underline" : 
        font.setUnderline(True)

    elif format == "overline" : 
        font.setOverline(True)

    elif format == "strike" : 
        font.setStrikeOut(True)

    elif format == "capital" : 
        font.setCapitalization(True)

    else : font.setBold(False)

    label.setFont(font)
    label.adjustSize()
    return label;

def Dialog(text,type="info") : 
    #NoIcon Question Information Warning Critical
    icon = QMessageBox.Information
    title = "Message"

    if type == "confirm" : 
        title = "Confirm"
        icon = QMessageBox.Question

    elif type == "warning" : 
        title = "Warning"
        icon = QMessageBox.Warning

    elif type == "error" : 
        title = "Error"
        icon = QMessageBox.Critical

    else : 
        title = "Message"
        icon = QMessageBox.Information

    alert = QMessageBox()
    alert.setText(text)
    alert.setWindowTitle(title)
    alert.setIcon(icon)
    alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    output = alert.exec()
    if output == QMessageBox.Ok : 
        return True 
    else : 
        return False
    
def HLayout(ui=[]) : 
    layout = QHBoxLayout()
    for widget in ui : 
        layout.addWidget(widget)
    return layout

def VLayout(ui=[]) : 
    layout = QVBoxLayout()
    for widget in ui : 
        layout.addWidget(widget)
    return layout

def IconButton(icon="",window=None,w=50,h=50) : 
    button = QToolButton(window)
    icon = QIcon(icon)
    button.setIcon(icon)
    button.setFixedSize(w,h)
    return button