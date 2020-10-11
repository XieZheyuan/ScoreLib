import logging
import sys

from PyQt5 import QtWidgets, QtCore, Qt
import os

try:
    from ScoreLib import read_data, paths, helps, count
except (ModuleNotFoundError, ImportError):
    import read_data, paths, helps, count

TITLE_STYLE = "font-size:24px;"


class Splash(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Splash, self).__init__(parent)
        self.resize(700, 500)
        self.setWindowTitle("ScoreLib Splash")
        self.setWindowFlags(QtCore.Qt.SplashScreen)
        self.setObjectName("Splash")
        self.setStyleSheet("#Splash{border-image:url(img/spash.png);}")


class AppWidget(QtWidgets.QDialog):
    """
    https://blog.csdn.net/jia666666/article/details/81835851
    """

    def __init__(self, parent=None):
        super(AppWidget, self).__init__(parent)
        # 水平布局
        Hloyout = QtWidgets.QHBoxLayout()

        # 实例化标签与列表控件
        self.styleLabel = QtWidgets.QLabel('set Style')
        self.styleComboBox = QtWidgets.QComboBox()

        # 从QStyleFactory中增加多个显示样式到列表控件
        self.styleComboBox.addItems(QtWidgets.QStyleFactory.keys())

        # 选择当前窗口的风格
        index = self.styleComboBox.findText(
            QtWidgets.QApplication.style().objectName(),

        )

        # 设置当前窗口的风格
        self.styleComboBox.setCurrentIndex(index)

        # 通过combobox控件选择窗口风格
        self.styleComboBox.activated[str].connect(self.handlestyleChanged)

        # 添加控件到布局，设置窗口布局
        Hloyout.addWidget(self.styleLabel)
        Hloyout.addWidget(self.styleComboBox)
        self.setLayout(Hloyout)

    # 改变窗口风格
    @staticmethod
    def handlestyleChanged(style):
        QtWidgets.QApplication.setStyle(style)


class ScoreLib(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScoreLib, self).__init__(parent=None)
        self.splashWindow = Splash()
        self.splashWindow.show()
        logging.debug("Splash window is showed, Program is going to open timer")
        self.splashTimer = QtCore.QTimer(self)
        self.splashTimer.timeout.connect(self.closeSplashWindow)
        self.splashTimer.start(2000)
        logging.debug("Splash Timer is started")

    def closeSplashWindow(self):
        logging.info("Timer is over, Program is going to close splash window , stop timer and show mainWindow")
        self.splashWindow.close()
        self.splashTimer.stop()
        self.init()
        self.showMaximized()

    def init(self):
        logging.info("Window is going to init")
        self.setWindowTitle("ScoreLib——让每一位老师轻松统计成绩数据")
        menu = self.menuBar()
        self.fileMenu = QtWidgets.QMenu("文件")
        self.importExcelAction = QtWidgets.QAction("从Microsoft Excel工作表导入")
        self.importExcelAction.triggered.connect(self.importExcel)
        self.fileMenu.addAction(self.importExcelAction)
        self.importDExcelAction = QtWidgets.QAction("从示例工作表导入")
        self.importDExcelAction.triggered.connect(self.importDExcel)
        self.fileMenu.addAction(self.importDExcelAction)
        self.ChangeSysStyle = QtWidgets.QAction("更改系统主题")
        self.ChangeSysStyle.triggered.connect(self.changeSys)
        self.fileMenu.addAction(self.ChangeSysStyle)
        menu.addMenu(self.fileMenu)
        self.mainTab = QtWidgets.QTabWidget()
        self.tab_table = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()
        self.tab_table_table = QtWidgets.QTableWidget()
        layout.addRow(self.tab_table_table)
        self.tab_table.setLayout(layout)
        self.mainTab.addTab(self.tab_table, "表格视图")
        self.tab_table_table.setEditTriggers(Qt.QAbstractItemView.NoEditTriggers)
        self.setCentralWidget(self.mainTab)
        self.data = []
        self.tab_edit = QtWidgets.QWidget()
        layout2 = QtWidgets.QFormLayout()
        label = QtWidgets.QLabel("列表转置")
        label.setStyleSheet(TITLE_STYLE)
        layout2.addWidget(label)
        label2 = QtWidgets.QLabel("列表转置是指行变列，列变行，具有对称性")
        layout2.addWidget(label2)
        zhuan_zhi_btn = QtWidgets.QPushButton("立即转置")
        zhuan_zhi_btn.clicked.connect(self.ZhuanZhi)
        layout2.addWidget(zhuan_zhi_btn)
        label3 = QtWidgets.QLabel("批量格式化")
        label3.setStyleSheet(TITLE_STYLE)
        layout2.addWidget(label3)
        label4 = QtWidgets.QLabel("批量格式化采用python风格格式符，如'%d'指取整（直接截断）等")
        layout2.addWidget(label4)
        self.format_btn = QtWidgets.QPushButton("立即格式化")
        self.format_btn.clicked.connect(self.format)
        self.format_help_btn = QtWidgets.QPushButton("帮助")
        self.format_help_btn.clicked.connect(self.format_help)
        layout2.addRow(self.format_help_btn, self.format_btn)

        self.tab_edit.setLayout(layout2)

        self.mainTab.addTab(self.tab_edit, "编辑")
        self.tab_a_student = QtWidgets.QWidget()
        layout3 = QtWidgets.QFormLayout()
        label5 = QtWidgets.QLabel("计算数据")
        label5.setStyleSheet(TITLE_STYLE)
        layout3.addWidget(label5)
        self.a_student_count_mode = QtWidgets.QComboBox()
        self.a_student_count_mode.addItems(count.items)
        layout3.addRow(QtWidgets.QLabel("类型："), self.a_student_count_mode)
        self.a_student_count_students = QtWidgets.QComboBox()
        self.a_student_count_students.addItems(self.get_students())
        layout3.addRow(QtWidgets.QLabel("同学："), self.a_student_count_students)
        self.a_student_count_label = QtWidgets.QLabel("现在还没有计算呢！")
        self.a_student_count_label.setStyleSheet(TITLE_STYLE)
        layout3.addWidget(self.a_student_count_label)
        label6 = QtWidgets.QLabel("绘图")

        self.a_student_count = QtWidgets.QPushButton("计算")
        self.a_student_count.clicked.connect(self.count)
        self.a_student_paint = QtWidgets.QPushButton("标绘")
        self.a_student_paint.clicked.connect(self.a_student_painter)

        layout3.addWidget(self.a_student_count)
        layout3.addWidget(self.a_student_paint)
        self.all_paint = QtWidgets.QPushButton("总体画图")
        self.all_paint.clicked.connect(self.all_painter)
        layout3.addWidget(self.all_paint)
        self.tab_a_student.setLayout(layout3)
        self.mainTab.addTab(self.tab_a_student, "单学生统计")
        self.tab_student_analysis = QtWidgets.QWidget()
        layout4 = QtWidgets.QFormLayout()
        label7 = QtWidgets.QLabel("学生趋势分析")
        label7.setStyleSheet(TITLE_STYLE)
        layout4.addWidget(label7)
        self.student_analysis_choice_student = QtWidgets.QComboBox()
        self.upgrade_student_action(1)
        self.student_analysis_btn = QtWidgets.QPushButton("立即生成分析")
        layout4.addRow("学生：", self.student_analysis_choice_student)
        self.student_analysis_btn.clicked.connect(self.got_student_analysis)
        layout4.addWidget(self.student_analysis_btn)
        self.tab_student_analysis.setLayout(layout4)
        self.mainTab.addTab(self.tab_student_analysis, "学生分析")

    def upgrade_student_action(self, ns=0):
        if ns == 1:
            self.a_student_count_students.clear()
            self.student_analysis_choice_student.addItems(self.get_students())

        else:
            print("1111")
            self.a_student_count_students.clear()
            self.a_student_count_students.addItems(self.get_students())
            for i in range(self.a_student_count_students.count()):print(self.a_student_count_students.itemText(i))
    def upgrade_student_action_1(self):
        print("1111")
        self.a_student_count_students.clear()
        self.a_student_count_students.addItems(self.get_students())
        for i in range(self.a_student_count_students.count()): print(self.a_student_count_students.itemText(i))

    def importExcel(self):
        logging.debug("import Excel is Running!")

        fn = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", paths.getDocuments(), "Microsoft Excel工作表(*.xlsx)")[0]
        fn = str(fn)
        if fn.replace(" ", "") == "":
            logging.warning("Excel Path is None")
            return -1

        logging.info("Excel Path: %s" % fn)
        data = read_data.get_data_from_excel_2(fn)

        self.tab_table_table.setRowCount(len(data))
        self.tab_table_table.setColumnCount(len(data[0]))
        for i in range(len(data)):

            for j in range(len(data[i])):
                self.tab_table_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
        self.data = data
        self.upgrade_student_action_1()
        self.upgrade_student_action(1)

    def ZhuanZhi(self):
        logging.debug("Loading...")
        if len(self.data) == 0:
            QtWidgets.QMessageBox.critical(self, "ScoreLib", "数据为空，无法转置，请先导入数据")
            return
        data = list(map(list, zip(*self.data)))

        self.tab_table_table.setRowCount(len(data))
        self.tab_table_table.setColumnCount(len(data[0]))
        for i in range(len(data)):

            for j in range(len(data[i])):
                self.tab_table_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
        self.data = data
        self.upgrade_student_action()
        self.upgrade_student_action(1)

    def format(self):
        if len(self.data) == 0:
            QtWidgets.QMessageBox.critical(self, "ScoreLib", "数据为空，无法批量格式化，请先导入数据")
            return
        m, flag = QtWidgets.QInputDialog.getText(self, "ScoreLib", "格式化字符串（python)风格")
        if not flag:
            return
        m = str(m)
        data = self.data
        for i in range(len(data)):
            for j in range(len(data[i])):
                try:
                    data[i][j] = m % (float(data[i][j]))
                except BaseException:
                    pass

        self.tab_table_table.setRowCount(len(data))
        self.tab_table_table.setColumnCount(len(data[0]))
        for i in range(len(data)):

            for j in range(len(data[i])):
                self.tab_table_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
        self.data = data

    def format_help(self):
        QtWidgets.QMessageBox.about(self, "格式化帮助", helps.FORMAT_HELP)

    def get_students(self):
        students = []
        logging.info(str(self.data))
        try:
            for i in self.data:
                students.append(i[0])
        finally:
            return students

    def count(self):
        try:
            data = self.data[1:]
        except IndexError:
            pass
        if not self.data:
            QtWidgets.QMessageBox.critical(self, "ScoreLib", "现在还没有导入数据呢")
            return

        this = []
        f = str(self.a_student_count_students.currentText())
        s = str(self.a_student_count_mode.currentText())
        for i in data:
            if i[0] == f:
                this = i[1:]
        print(this)
        for i in range(len(this)):
            this[i] = float(this[i])
        print(this)
        function = count.item_dict[s]
        ans = function(this)
        self.a_student_count_label.setText("%s的%s计算结果为：%s" % (f, s, ans))

    def a_student_painter(self):
        if not self.data:
            QtWidgets.QMessageBox.critical(self, "ScoreLib", "现在还没有导入数据呢")
            return

        os.system("python drawer.py " + str(self.data).replace(" ", "") + " " + str(
            self.a_student_count_students.currentText()) + " d")

    def all_painter(self):
        if not self.data:
            QtWidgets.QMessageBox.critical(self, "ScoreLib", "现在还没有导入数据呢")
            return

        os.system("python drawer.py " + str(self.data[1:]).replace(" ", "") + " a")

    def importDExcel(self):
        logging.debug("import Excel is Running!")

        fn = os.path.join(os.path.abspath("."), "1.xlsx")

        logging.info("Excel Path: %s" % fn)
        data = read_data.get_data_from_excel_2(fn)

        self.tab_table_table.setRowCount(len(data))
        self.tab_table_table.setColumnCount(len(data[0]))
        for i in range(len(data)):

            for j in range(len(data[i])):
                self.tab_table_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
        self.data = data
        self.upgrade_student_action_1()
        self.upgrade_student_action(1)

    def changeSys(self):
        aw = AppWidget(self)
        aw.show()

    def got_student_analysis(self):
        try:
            data = self.data[1:]
        except IndexError:
            pass
        if not self.data:
            QtWidgets.QMessageBox.critical(self, "ScoreLib", "现在还没有导入数据呢")
            return

        this = []
        f = str(self.student_analysis_choice_student.currentText())
        for i in data:
            if i[0] == f:
                this = i[1:]
        print(this)
        for i in range(len(this)):
            this[i] = float(this[i])
        print(this)
        msgs = []
        var = count.count_var(this)
        if var == 0:
            msgs.append("好神奇，竟然一直都是同一个分数！")
        elif var < 5:
            msgs.append("分数波动不大哦!")
        elif var < 10:
            msgs.append("分数波动有点大哦！")
        else:
            msgs.append("分数波动很大哦！")
        var = count.count_range(this)
        if var != 0:
            if var < 5:
                msgs.append("分数范围不大哦!")
            elif var < 10:
                msgs.append("分数范围有点大哦！")
            else:
                msgs.append("分数范围很大哦！")
        var = max(this) - count.count_average(this)
        if var != 0:
            if var < 5:
                msgs.append("最好的成绩与平均成绩差不大哦！")
            elif var < 10:
                msgs.append("最好的成绩与平均成绩差有点大哦！")
            else:
                msgs.append("最好的成绩与平均成绩差很大哦！")
        var = abs(min(this) - count.count_average(this))
        if var != 0:
            if var < 5:
                msgs.append("最差的成绩与平均成绩差不大哦！")
            elif var < 10:
                msgs.append("最差的成绩与平均成绩差有点大哦！")
            else:
                msgs.append("最差的成绩与平均成绩差很大哦！")

        msg = "\n".join(msgs)
        QtWidgets.QMessageBox.about(self,"ScoreLib", msg)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    mainWindow = ScoreLib()
    exit(app.exec_())
