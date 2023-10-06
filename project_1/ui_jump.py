import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from Ui_main_window import Ui_MainWindow as UiMain
from Ui_search_route import Ui_MainWindow as UiRoute
from Ui_search_station import Ui_MainWindow as UiStation
from Ui_route_result import Ui_MainWindow as UiRouteResult
from Ui_station_result import Ui_MainWindow as UiStationResult
from search_bus_routes import search_bus_route
from search_bus_stop import search_bus_stop
from text_to_unicode import *

class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window_main = None
        self.window_route = None
        self.window_station = None
        self.window_route_result = None
        self.window_station_result = None

        self.line_route = None
        self.line_station = None

        self.label_empty_r = None
        self.label_empty_s = None 

        self.label_r_dir = None
        self.label_r_time = None
        self.label_r_length = None
        self.label_r_num = None
        self.label_r_company = None
        self.label_r_stops = None
        self.route_dir = 0  # 0 or 1


        self.label_s_name = None
        self.label_s_routes = None
        self.station_order = 0

    def show_main(self):
        if self.window_main is None:
            self.window_main = QMainWindow()
            ui = UiMain()
            ui.setupUi(self.window_main)
            ui.main2route.clicked.connect(self.show_route)
            ui.main2station.clicked.connect(self.show_station)
            ui.exit_button.clicked.connect(self.app.quit)

        self.window_main.show()
        if self.window_route is not None:
            self.window_route.close()
        if self.window_station is not None:
            self.window_station.close()
        if self.window_route_result is not None:
            self.window_route_result.close()
        if self.window_station_result is not None:
            self.window_station_result.close()




    def show_route(self):
        if self.window_route is None:
            self.window_route = QMainWindow()
            ui = UiRoute()
            ui.setupUi(self.window_route)
            self.line_route = ui.line_route
            self.label_empty_r = ui.empty_warn
            ui.route2main.clicked.connect(self.show_main)
            ui.search_route.clicked.connect(self.handle_route_search)

        self.window_route.show()
        self.line_route.clear()
        self.label_empty_r.clear()
        if self.window_main is not None:
            self.window_main.close()
        if self.window_station is not None:
            self.window_station.close()
        if self.window_route_result is not None:
            self.window_route_result.close()
        if self.window_station_result is not None:
            self.window_station_result.close()


    def handle_route_search(self):
        number = self.line_route.text()
        if number.strip():
            self.show_route_result(search_bus_route(str(number)))
        else:
            self.label_empty_r.setText("输入为空，请重新输入！")





    def show_station(self):
        if self.window_station is None:
            self.window_station = QMainWindow()
            ui = UiStation()
            ui.setupUi(self.window_station)
            self.line_station = ui.line_station
            self.label_empty_s = ui.empty_warn
            ui.station2main.clicked.connect(self.show_main)
            ui.search_station.clicked.connect(self.handle_station_search)

        self.window_station.show()
        self.line_station.clear()
        self.label_empty_s.clear()
        if self.window_main is not None:
            self.window_main.close()
        if self.window_route is not None:
            self.window_route.close()
        if self.window_route_result is not None:
            self.window_route_result.close()
        if self.window_station_result is not None:
            self.window_station_result.close()



    def handle_station_search(self):
        name = self.line_station.text()
        if name.strip():
            self.show_station_result(search_bus_stop(str(name)))
        else:
            self.label_empty_s.setText("输入为空，请重新输入！")



    def show_route_result(self, route_result):
        
        self.window_route_result = QMainWindow()
        ui = UiRouteResult()
        ui.setupUi(self.window_route_result)

        self.label_r_dir = ui.dir
        self.label_r_time = ui.time
        self.label_r_length = ui.length
        self.label_r_num = ui.num
        self.label_r_company = ui.company
        self.label_r_stops = ui.stops
        

        ui.result2main.clicked.connect(self.show_main)
        ui.result2route.clicked.connect(self.show_route)

        ui.change_dir.clicked.connect(lambda: self.change_dir(route_result))


        self.window_route_result.show()      

        if route_result == None:
            self.label_r_dir.setText("查找的线路不存在！")
        elif len(route_result) == 1:
            result = route_result[0]
            self.label_r_dir.setText(result['dir'])
            self.label_r_time.setText(result['time'])
            self.label_r_length.setText(result['length'])
            self.label_r_num.setText(result['stops_num'])
            self.label_r_company.setText(result['company'])
            text = ""
            for key, value in result['stops'].items():
                text = text + str(key) + "    " + str(value) + '<br>'

            self.label_r_stops.setText(text)


        else:
            result = route_result[self.route_dir]
            self.label_r_dir.setText(result['dir'])
            self.label_r_time.setText(result['time'])
            self.label_r_length.setText(result['length'])
            self.label_r_num.setText(result['stops_num'])
            self.label_r_company.setText(result['company'])
            text = ""
            for key, value in result['stops'].items():
                text = text + str(key) + "    " + str(value) + '<br>'

            self.label_r_stops.setText(text)
            

        if self.window_main is not None:
            self.window_main.close()
        if self.window_route is not None:
            self.window_route.close()
        if self.window_station is not None:
            self.window_station.close()
        if self.window_station_result is not None:
            self.window_station_result.close()

    
    def change_dir(self, route_result):

        if len(route_result) == 2:
            self.route_dir = 1 - self.route_dir
            result = route_result[self.route_dir]
            self.label_r_dir.setText(result['dir'])
            self.label_r_time.setText(result['time'])
            self.label_r_length.setText(result['length'])
            self.label_r_num.setText(result['stops_num'])
            self.label_r_company.setText(result['company'])
            text = ""
            for key, value in result['stops'].items():
                text = text + str(key) + "    " + str(value) + '<br>'

            self.label_r_stops.setText(text)





    def show_station_result(self, station_result): 
        self.station_order = 0
        self.window_station_result = QMainWindow()
        ui = UiStationResult()
        ui.setupUi(self.window_station_result)
        self.label_s_name = ui.station_name
        self.label_s_routes = ui.pass_routes
        ui.result2main.clicked.connect(self.show_main)
        ui.result2station.clicked.connect(self.show_station)
        ui.next_station.clicked.connect(lambda: self.next_station(station_result))

        self.window_station_result.show()
        if station_result == None:
            self.label_s_name.setText("查找的站点不存在！")
            self.label_s_routes.setText("")
        else:
            show_station = station_result[self.station_order]
            self.label_s_name.setText(show_station['name'])
            text = ""
            for route in show_station['route']:
                text = text + str(route) + '   '
            self.label_s_routes.setText(text)

        if self.window_main is not None:
            self.window_main.close()
        if self.window_route is not None:
            self.window_route.close()
        if self.window_station is not None:
            self.window_station.close()
        if self.window_route_result is not None:
            self.window_route_result.close()


    def next_station(self, station_result):
        self.station_order = (self.station_order + 1) % len(station_result)
        show_station = station_result[self.station_order]
        self.label_s_name.setText(show_station['name'])
        text = ""
        for route in show_station['route']:
            text = text + str(route) + '   '
        self.label_s_routes.setText(text)


    def run(self):
        self.show_main()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = Controller()
    controller.run()