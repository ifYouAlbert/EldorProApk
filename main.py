'''init'''

from kivy.core.window import Window
W, H = Window.size
special_mult = 1.3
mult = 1.5
Kcanvas = W / 548
ScreenCoof = -0.3
WKoof = W * Kcanvas
buttonSizeX = WKoof / 3.1
buttonSizeY = WKoof / 2.7

drawShiftY = 1.25

drawClockKoof = 1.22

clockDrawSize = 147

buttonShift = (WKoof - (buttonSizeX * 3)) / 4

from kivy.config import Config
Config.set('graphics', 'width', str(W))
Config.set('graphics', 'height', str(H))
Config.set('graphics', 'resizable', '0')
Window.size = (W, H)

from kivy.core.window import Window
'''import'''

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Canvas, Line, Ellipse, Triangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock as kivyClock
import math
import time

'''dateManager'''
mainData = JsonStore('mydata.json')
def popEntryList(date, time):
    try:
        entryList = mainData.get(date)
    except:
        entryList = {}
    entryList = entryList['data']
    entryList.pop(time)
    mainData.put(date, data=entryList)
    mainData.store_sync()


def appendDataEntry(date, time, text):
    try:
        entryList = mainData.get(date)
        entryList = entryList['data']
    except:
        entryList = {}
    entryList.update({time: text})
    mainData.put(date, data=entryList)
    mainData.store_sync()


def appendDataEntryList(date, entryList):
    mainData.put(date, data=entryList)
    mainData.store_sync()


def getDataEntryList(date):
    try:
        entryList = mainData.get(date)
        entryList = entryList['data']
    except:
        entryList = {}
    return entryList

'''dateFunc'''
def generateDays(date, countRange):
    day, week, month, year = date
    countWeek = 0
    weekList = list(weekDict.keys())
    for _week in weekList:
        if _week == week:
            break
        countWeek += 1

    countMonth = 0
    monthList = list(monthDict.keys())
    for _month in monthList:
        if _month == month:
            break
        countMonth += 1

    dateList = []
    for i in range(countRange):
        day = int(day)
        dayCount = dayCountDict[month]

        countWeek += 1
        if countWeek < len(weekList):
            week = weekList[countWeek]
        else:
            countWeek = 0
            week = weekList[0]

        if day < dayCount:
            day += 1
        else:
            day = 1
            countMonth += 1
            if countMonth < len(monthList):
                month = monthList[countMonth]
            else:
                month = monthList[0]
                year += 1

        dateList.append((day, week, month, year))
    return dateList


def getDate():
    _time = str(time.asctime())
    hourStr, min, secAndYear = _time.split(':')
    lenHourStr = len(hourStr)
    date = hourStr[0: lenHourStr - 2]
    lendate = len(date)
    day = date[lendate - 3: lendate]
    month = date[0: lendate - 2]
    monthsplit = month.split(' ')
    week = monthsplit[0]
    month = monthsplit[1]
    year = secAndYear.split(' ')[1]
    return day, week, month, year


def datePrepare(dateList):
    day, week, month, year = dateList
    day = int(day)
    month = str(monthDict[month])
    week = str(weekDict[week])
    tmpStr = week + '. ' + str(day) + ' ' + month
    return tmpStr


monthDict = {'Jan': 'Января', 'Feb': 'Февраля', 'Mar': 'Марта', 'Apr': 'Апреля',
             'May': 'Мая', 'Jun': 'Июня', 'Jul': 'Июля', 'Aug': 'Августа',
             'Sep': 'Сентября', 'Oct': 'Октября', 'Nov': 'Ноября', 'Dec': 'Декабря'}

weekDict = {'Mon': 'Пн', 'Tue': 'Вт', 'Wed': 'Ср', 'Thu': 'Чт',
            'Fri': 'Пт', 'Sat': 'Сб', 'Sun': 'Вс'}

dayCountDict = {'Jan': 31, 'Feb': 28, 'Mar': 31, 'Apr': 30, 'May': 31, 'Jun': 30,
                'Jul': 31, 'Aug': 31, 'Sep': 30, 'Oct': 31, 'Nov': 30, 'Dec': 31}

'''month'''
class ScreenMonth(Screen):
    def __init__(self, **kw):
        super(ScreenMonth, self).__init__(**kw)

        with self.canvas:
            Color(0.8, 0.8, 0.8)
            Rectangle(pos=(0, 0), size=(W, H*Kcanvas))
        self.add_widget(Label(text='Month', font_size=50, color=(0, 0, 0)))

    def on_enter(self):
        pass

    def on_leave(self):
        pass

'''sup'''
class ScreenVoice(Screen):
    def __init__(self, **kw):
        super(ScreenVoice, self).__init__(**kw)
        with self.canvas:
            Color(1, 1, 1)
            Rectangle(pos=(0, 0), size=(W*Kcanvas, H*Kcanvas))

        self.targetButton = ''  # будет находиться время. Например 17:30
        self.H = H - (H * ScreenCoof)

        self.fl = FloatLayout()

        self.Entry = TextInput(pos=(0, self.H*0.7), size_hint=(1, 0.1))
        self.Button = Button(text='ok', pos=(0, self.H*0.6), size_hint=(1, 0.1), on_press=self.ButtonHandler)

        self.fl.add_widget(self.Entry)
        self.fl.add_widget(self.Button)

        self.add_widget(self.fl)

    def ButtonHandler(self, button):
        if self.Entry.text == '':
            self.Entry.text = '-'
        Screens['day'].clock.updateEntryList(self.targetButton, self.Entry.text)
        #Screens['day'].clock.entryList.update({self.targetButton: self.Entry.text})
        Screens['day'].setButtons()
        set_screen('day', 'right')

    def setTargetButton(self, time):
        self.targetButton = time

    def on_leave(self):
        self.Entry.text = ''
        self.targetButton = ''

'''day'''
class entryButton(Button):
    def __init__(self, entryTime, entryText, **kw):
        super(entryButton, self).__init__(**kw)
        # self.max_signs = 50
        self.max_signs = int(20 * (50 / self.font_size))

        self.entryTime = entryTime
        self.entryText = entryText
        self.time = entryTime
        self.textTime = entryText
        text = entryTime + ' ' + entryText
        self.text = self.textPrepare(text)
        self.font_name = 'UbuntuMono-R'

    def textPrepare(self, text):
        res = self.max_signs - len(text)
        if res < 0:
            text = text[0: self.max_signs]

        else:
            text = text + (' ' * res)

        return text

    def on_press(self):
        if self.textTime == '':
            Screens['voice'].setTargetButton(self.entryTime)
            set_screen('voice', 'left')

        else:
            Screens['day'].clock.popEntryList(self.time)
            self.background_color = (1, 1, 1)
            self.text = self.textPrepare(self.time + ' ')


class ScreenDay(Screen):
    def __init__(self, **kw):
        super(ScreenDay, self).__init__(**kw)
        self.kivyButColor = get_color_from_hex('#585858')

        with self.canvas:
            Color(0.6, 0.6, 0.6)
            Rectangle(pos=(0, 0), size=(W*Kcanvas, H*Kcanvas))

        self.label = Label(text='Day', font_size=50 * special_mult, color=(1, 1, 1),
                           size_hint_y=None, height=dp(100))

        self.layout = GridLayout(cols=1, spacing=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = RecycleView(size_hint=(1, None), size=(W, H*mult))

        root.add_widget(self.layout)

        self.add_widget(root)

        self.clock = ''

    def setDay(self, clock):
        self.clock = clock
        self.label.text = clock.date
        self.setButtons()

    def setButtons(self):
        self.layout.clear_widgets()

        self.layout.add_widget(Label(size_hint_y=None, height=dp(80)))
        self.layout.add_widget(self.label)
        buttonList = {}
        hour = 9
        firstTime = str(hour)+':00'
        buttonList.update({firstTime: ''})
        for i in range(23):
            if i % 2 == 1:
                hour += 1
                strTime = str(hour) + ':00'

            else:
                strTime = str(hour) + ':30'
            buttonList.update({strTime: ''})

        for key in self.clock.entryList.keys():
            text = self.clock.entryList[key]
            buttonList.update({key: text})

        for key in buttonList.keys():
            time = key
            text = buttonList[key]
            color = (1, 1, 1)
            if text != '':
                color = (1, 0, 0)
            self.layout.add_widget(entryButton(time, text, size_hint_y=None, height=dp(buttonSize),
                                               font_size=buttonFont, background_color=color))
        self.layout.add_widget(Widget(size_hint_y=None, height=dp(100)))

    def on_enter(self):
        pass

    def on_leave(self):
        pass

'''clock'''
class ScreenClock(Screen):
    def __init__(self, **kw):
        super(ScreenClock, self).__init__(**kw)
        self.fl = FloatLayout()

        self.H = H - (H * ScreenCoof)
        self.W = W
        self.kivyButColor = get_color_from_hex('#585858')

        self.clocksize = 147 * mult
        self.rad = self.clocksize // 2

        self.shiftx = (buttonSizeX - self.clocksize) // 2
        self.shifty = (buttonSizeY - self.clocksize) // drawShiftY

        self.coordList = [[74, 146, 74, 123],  # t 1
                          [111, 135, 100, 116],  # t 2
                          [137, 109, 117, 98],  # t 3
                          [145, 75, 122, 75],  # t 4
                          [137, 42, 117, 52],  # t 5
                          [100, 34, 112, 14],  # t 6
                          [74, 0, 74, 24],  # t 7
                          [34, 13, 48, 34],  # t 8
                          [9, 41, 31, 52],  # t 9
                          [0, 75, 24, 75],  # t 10
                          [10, 107, 37, 92],  # t 11
                          [35, 134, 47, 116],  # t 12 ---------------
                          [92, 134, 87, 121],  # tl 1
                          [122, 118, 110, 107],  # tl 2
                          [136, 90, 122, 86],  # tl 3
                          [137, 59, 122, 63],  # tl 4
                          [122, 32, 111, 42],  # tl 5
                          [92, 15, 88, 28],  # tl 6
                          [56, 15, 60, 28],  # tl 7
                          [27, 32, 38, 42],  # tl 8
                          [12, 60, 27, 63],  # tl 9
                          [12, 90, 27, 86],  # tl 10
                          [26, 117, 37, 107],  # tl 11
                          [56, 135, 60, 122]  # tl 12
                          ]

        self.clockList = []

        self.segmentList = [[74, 146, 95, 143],
                            [94, 143, 112, 134],
                            [112, 135, 127, 121],
                            [127, 122, 137, 108],
                            [137, 109, 143, 91],
                            [143, 93, 146, 74],
                            [146, 75, 144, 57],
                            [144, 58, 139, 42],
                            [139, 43, 129, 26],
                            [130, 26, 112, 12],
                            [114, 12, 94, 4],
                            [97, 3, 74, 0],
                            [74, 0, 52, 2],
                            [54, 3, 32, 11],
                            [34, 11, 17, 26],
                            [18, 25, 7, 43],
                            [8, 39, 2, 60],
                            [2, 57, 0, 76],
                            [0, 74, 2, 94],
                            [2, 92, 9, 107],
                            [9, 107, 19, 124],
                            [20, 123, 35, 136],
                            [35, 136, 54, 143],
                            [54, 143, 74, 146]]

        self.drawArrowPos = (0, 0)

        with self.canvas:
            Color(0.7, 0.7, 0.7)
            Rectangle(pos=(0, 0), size=(W*Kcanvas, H*Kcanvas))
        # self.add_widget(Label(text='Clock', font_size=50, color=(0, 0, 0)))

        self.add_widget(self.fl)

        self.setLayout()
        self.drawClockWindow()
        for clock in self.clockList:
            clock.update()

    def addClockButton(self, text, position, butsize, fontSize, listId, _time, entryList):
        tmpClock = Clock(text, position, butsize, listId, _time, self, size_hint=(None, None), size=butsize, pos=position)
        self.fl.add_widget(tmpClock)

        sizey = (buttonSizeY - clockDrawSize) // drawShiftY
        x, y = position
        shift = 0
        shift = (butsize[1] * 0.1) * special_mult
        y = y - shift
        fontSize = fontSize * special_mult
        label = Label(pos=(x, y), size_hint=(None, None),
                      size=(buttonSizeX, sizey), font_size=fontSize)
        self.fl.add_widget(label)
        tmpClock.setLabel(label)
        tmpClock.printInLabel()
        tmpClock.setEntryList(entryList)

        self.clockList.append(tmpClock)

    def setLayout(self):
        global buttonSizeX, buttonShift, Screens

        y = self.H*1.2

        firstDate = getDate()
        tmpDateList = generateDays(firstDate, 8)
        dateList = ['Сегодня']
        for date in tmpDateList:
            _date = datePrepare(date)
            dateList.append(_date)

        countDate = -1
        labelFontSize = 20

        for j in range(3):
            y = y - buttonSizeY - buttonShift
            x = 0 - buttonSizeX
            for i in range(3):
                x = x + buttonSizeX + buttonShift
                if j == 0 and i == 0:
                    self.drawArrowPos = (x, y)
                    self.arrowUpdate()
                    kivyClock.schedule_interval(self.kivyClockHandler, 1)

                position = (x, y)
                butsize = (buttonSizeX, buttonSizeY)
                countDate += 1
                text = dateList[countDate]
                if countDate == 0:
                    _time = firstDate
                else:
                    _time = tmpDateList[countDate-1]

                timeKey = str(_time[0]) + str(_time[1]) + str(_time[2]) + str(_time[3])
                entryList = getDataEntryList(timeKey)

                _time = (_time, timeKey)

                self.addClockButton(text, position, butsize, labelFontSize,
                                    countDate, _time, entryList)

        '''
        x = buttonShift + buttonSizeX + buttonShift
        y = y - buttonSizeY - buttonShift
        position = (x, y)
        butsize = (buttonSizeX, buttonSizeY)

        self.addClockButton('день 10', position, butsize, labelFontSize, 9)
        '''

    def kivyClockHandler(self, clock):
        self.arrowUpdate()

    def drawSegment(self, pos, time, color, multiply):
        coords = self.segmentList[time]
        pos1 = coords[0], coords[1]
        pos2 = coords[2], coords[3]

        xcenter = pos[0] + self.rad + self.shiftx
        ycenter = pos[1] + self.rad + self.shifty

        with self.canvas:
            Color(color, 0, 0, 1)
            x = xcenter - self.rad
            y = ycenter - self.rad

            rad = (xcenter, ycenter)
            pos1x = (pos1[0] * multiply) + x
            pos1y = (pos1[1] * multiply) + y
            pos2x = (pos2[0] * multiply) + x
            pos2y = (pos2[1] * multiply) + y
            Triangle(points=(rad[0], rad[1], pos1x, pos1y, pos2x, pos2y, rad[0], rad[1]))

    def calculate_point(self, x0, y0, r, angle):
        angle_rad = math.radians(angle)
        x = x0 + r * math.cos(angle_rad)
        y = y0 + r * math.sin(angle_rad)
        return x, y

    def getTime(self):
        _time = str(time.asctime())
        hourStr, min, secAndYear = _time.split(':')
        lenHourStr = len(hourStr)
        hour = hourStr[lenHourStr - 2: lenHourStr]
        sec = secAndYear.split(' ')[0]
        return hour, min, sec

    def arrowUpdate(self):
        angle, _time = self.prepareArrowAngle()
        hour, min = _time
        if hour == 0 and min == 0:
            self.clearClockWindow()
            self.setLayout()
            self.drawClockWindow()
            pass
        self.canvas.remove_group(u'arrow')
        self.drawClockArrow((self.drawArrowPos), 147 * 0.5, angle)

    def clearClockWindow(self):
        for clock in self.clockList:
            x, y = clock.getDrawCoords()
            self.clearClock((x, y))

        self.fl.clear_widgets()

    def prepareArrowAngle(self):
        hour, min, sec = self.getTime()
        hour = int(hour)
        min = int(min)
        _time = (hour, min)
        hour = hour % 12
        hourAngle = hour * 30
        minAngle = min / 2
        angle = -hourAngle - minAngle
        angle += 90
        return angle, _time

    def drawClockArrow(self, pos, lenght, angle):
        xcenter = pos[0] + self.rad + self.shiftx
        ycenter = pos[1] + self.rad + self.shifty
        x, y = self.calculate_point(xcenter, ycenter, lenght, angle)
        with self.canvas:
            Color(1, 1, 1)
            Line(width=2, points=(xcenter, ycenter, x, y), group=u'arrow')

    def drawClock(self, pos, multiply):
        global size_x, size_y, clockDrawSize
        with self.canvas:
            Color(0, 0, 0, 1)

            xcenter = pos[0] + self.rad + self.shiftx
            ycenter = pos[1] + self.rad + self.shifty
            Color(0, 0, 0, 1)
            Line(circle=(xcenter, ycenter, self.rad), width=1.1)

            x = xcenter - self.rad
            y = ycenter - self.rad

            for coord in self.coordList:
                Line(points=(
                    (x + coord[0] * multiply, y + coord[1] * multiply),
                    (x + coord[2] * multiply, y + coord[3] * multiply)),
                    width=1.0001)

    def clearClock(self, pos):
        with self.canvas:
            x, y = pos
            x = x + self.shiftx
            y = y + self.shifty
            c = self.kivyButColor
            Color(c[0], c[1], c[2])
            Rectangle(pos=(x, y), size=(self.clocksize, self.clocksize))

    def drawClockWindow(self):
        global clockButSize, clockButShift

        for clock in self.clockList:
            x, y = clock.getDrawCoords()
            #self.drawSegment((x, y), 1, 1, mult)
            self.drawClock((x, y), mult)

    def on_enter(self):
        pass

    def on_leave(self):
        pass


class Clock(Button):
    def __init__(self, date, position, butsize, listId, _time, clockScreen, **kw):
        super(Clock, self).__init__(**kw)
        self.timeList = _time[0]
        self.timeKey = _time[1]
        self.date = date
        self.position = position
        self.butsize = butsize

        self.entryList = {}  # спиоск состоящий из списков по типу - ['время', 'текст']

        self.listId = listId

        self.label = None

        self.clockScreen = clockScreen

    def setLabel(self, label):
        self.label = label

    def printInLabel(self):
        self.label.text = str(self.date)

    def getDrawCoords(self):
        x = self.position[0]
        y = self.position[1]
        return x, y

    def on_press(self):
        Screens['day'].setDay(self)
        set_screen('day', 'left')

    def setEntryList(self, entryList):
        self.entryList = entryList

    def popEntryList(self, time):
        popEntryList(self.timeKey, time)
        self.entryList.pop(time)
        self.update()

    def updateEntryList(self, time, text):
        appendDataEntry(self.timeKey, time, text)
        self.entryList.update({time: text})
        self.update()

    def update(self):
        x, y = self.getDrawCoords()
        self.clockScreen.clearClock((x, y))
        for time in self.entryList.keys():
            color = 1
            if int(time.split(':')[0]) > 12:
                color = 0.7
            time = self.prepareTime(time)
            self.drawSegment(time, color)
        self.clockScreen.drawClock((x, y), mult)

    def prepareTime(self, time):
        hour, min = time.split(':')
        hour = int(hour)
        min = int(min)
        totalTime = ((hour % 12)*2) + (min/30)
        return int(totalTime)

    def drawSegment(self, time, color):
        x, y = self.getDrawCoords()
        self.clockScreen.drawSegment((x, y), time, color, mult)

'''init'''
sm = ScreenManager()

Screens = {}
Screens.update({'month': ScreenMonth(name='month')})
Screens.update({'clock': ScreenClock(name='clock')})
Screens.update({'day': ScreenDay(name='day')})
Screens.update({'voice': ScreenVoice(name='voice')})


def set_screen(name_screen, dir='right'):
    global target_screen
    sm.switch_to(Screens[name_screen], direction=dir)
    target_screen = name_screen

canvas = ''
target_screen = ' '
buttonSize = 60
buttonFont = 30 * special_mult


class navigateBox(BoxLayout):
    def __init__(self, **kw):
        super(navigateBox, self).__init__(**kw)
        with self.canvas:
            Color(0.8, 0.8, 0.8)
            _H = H * Kcanvas
            _W = W * Kcanvas
            Rectangle(pos=(0, 0), size=(_W, _H * 0.1))


class EldorProApp(App):
    def build(self):
        set_screen('clock', 'up')
        box = BoxLayout(orientation='vertical')
        buttonBox = navigateBox(orientation='horizontal', size_hint=(1, .1))

        buttonMonth = Button(text='month', on_press=self.monthHandler)
        buttonClock = Button(text='clock', on_press=self.clockHandler)
        buttonDay = Button(text='day', on_press=self.dayHandler)

        buttonBox.add_widget(buttonMonth)
        buttonBox.add_widget(buttonClock)
        buttonBox.add_widget(buttonDay)
        box.add_widget(sm)
        box.add_widget(buttonBox)
        return box

    def monthHandler(self, button):
        set_screen('month', 'right')

    def clockHandler(self, button):
        if target_screen == 'month':
            set_screen('clock', 'left')

        elif target_screen == 'day':
            set_screen('clock', 'right')

    def dayHandler(self, button):
        set_screen('day', 'left')


if __name__ == '__main__':
    Screens['day'].setDay(Screens['clock'].clockList[0])
    EldorProApp().run()