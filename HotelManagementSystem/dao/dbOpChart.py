import pymysql
from dao.dbConfig import localSourceConfig as localConfig
import xlwt
import matplotlib
matplotlib.use("Qt5Agg")  # Declare the use of QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime


class Chart:
    def __init__(self,config=localConfig):
        self.db = pymysql.connect(host=config['host'], port=config['port'], user=config['user'],
                                  passwd=config['passwd'], db=config['db'], charset=config['charset'],
                                  cursorclass=config['cursorclass'])
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        print("Database version : %s " % data['VERSION()'])


    def toExcel(self,path, table_name):
        """
        Export to excel form
        """
        sql = "select * from " + table_name
        self.cursor.execute(sql)
        path = str(path)
        fields = [field[0] for field in self.cursor.description]
        all_data = self.cursor.fetchall()
        # 写入excel
        book = xlwt.Workbook()
        sheet = book.add_sheet('sheet1')
        for col, field in enumerate(fields):
            sheet.write(0, col, field)
        row = 1
        for i in range(len(all_data)):
            data = all_data[i].values()
            for col, field in enumerate(data):
                sheet.write(row, col, field)
            row += 1
        book.save(path+"/%s.xls" % table_name)

    def getRevenue(self):
        """
        get the date of turnover
        """
        list_revenue = []
        list_date = []
        for i in range(7):
            data = ()
            sum = 0
            delta = datetime.timedelta(days=i)
            date = datetime.date.today()
            date_selected = date - delta
            str_date = str(date_selected)
            list_date.append(str_date[5:])
            self.cursor.execute("select money from hotelorder where end_time=%s",(date_selected))
            data = self.cursor.fetchall()
            if data != ():
                for i in range(len(data)):
                    sum = sum + int(data[i]['money'])
            list_revenue.append(sum)
        print(list_revenue)
        print(list_date)
        list_date.reverse()
        return list_date, list_revenue

    def getOccupy(self):
        """
        Get the Indicators of Occupancy Rate/Occupancy Rate
        """
        list_occupy = []
        list_date = []
        self.cursor.execute("select count(*) from room")
        totalRoomCount = self.cursor.fetchall()[0]['count(*)']
        print(totalRoomCount)
        for i in range(7):
            data = ()
            occupyRate = 0.0
            delta = datetime.timedelta(days=i)
            date = datetime.date.today()
            date_selected = date - delta
            str_date = str(date_selected)
            list_date.append(str_date[5:])
            self.cursor.execute("select distinct rid from hotelorder where end_time>=%s and start_time<=%s",
                                (date_selected,date_selected))
            data = self.cursor.fetchall()
            print(data)
            if data != ():
                occupyRate = float(len(data) / totalRoomCount)
            list_occupy.append(occupyRate)
        print(list_occupy)
        list_date.reverse()
        return list_date, list_occupy








