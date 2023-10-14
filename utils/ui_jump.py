import sys
sys.path.append('./ui')

from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_main_window import Ui_MainWindow as UiMain
from Ui_search_route import Ui_MainWindow as UiRoute
from Ui_search_station import Ui_MainWindow as UiStation
from Ui_route_result import Ui_MainWindow as UiRouteResult
from Ui_station_result import Ui_MainWindow as UiStationResult
from search_bus_routes import search_bus_route
from search_bus_stop import search_bus_stop
from text_to_unicode import *


class MainWindow(QMainWindow):
    """
    This class represents the main window of the bus route and station search application.

    Attributes:
        app (QApplication): The PyQt5 application.
        ui (UiMain): The user interface of the main window.
        route_window (RouteWindow): The window for searching bus routes.
        station_window (StationWindow): The window for searching bus stations.

    Methods:
        show_route(): Displays the window for searching bus routes.
        show_station(): Displays the window for searching bus stations.

    """
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ui = UiMain()
        self.ui.setupUi(self)
        self.ui.main2route.clicked.connect(self.show_route)
        self.ui.main2station.clicked.connect(self.show_station)
        self.ui.exit_button.clicked.connect(self.app.quit)
        self.route_window = None
        self.station_window = None

    def show_route(self):
        if self.route_window is None:
            self.route_window = RouteWindow(self.app, self)
        self.route_window.show()
        self.hide()

    def show_station(self):
        if self.station_window is None:
            self.station_window = StationWindow(self.app, self)
        self.station_window.show()
        self.hide()


class RouteWindow(QMainWindow):
    """
    This class represents the window for searching bus routes.

    Attributes:
        app (QApplication): The PyQt5 application.
        main_window (MainWindow): The main window of the application.
        ui (UiRoute): The user interface of the route window.
        route_result_window (RouteResultWindow): The window displaying bus route search results.

    Methods:
        show_main(): Displays the main window of the application.
        handle_route_search(): Handles the bus route search operation.

    """
    def __init__(self, app, main_window):
        super().__init__()
        self.app = app
        self.main_window = main_window
        self.ui = UiRoute()
        self.ui.setupUi(self)
        self.ui.route2main.clicked.connect(self.show_main)
        self.ui.search_route.clicked.connect(self.handle_route_search)
        self.route_result_window = None
        self.ui.empty_warn.setText("查询可能需要几秒时间，请耐心等待！")
        self.ui.line_route.clear()

    def show_main(self):
        self.main_window.show()
        self.close()

    def handle_route_search(self):
        number = self.ui.line_route.text()
        if number.strip():
            route_result = search_bus_route(str(number))
            self.route_result_window = RouteResultWindow(self.app, route_result, self ,self.main_window)
            self.route_result_window.show()
            self.hide()
            self.ui.empty_warn.setText("查询可能需要几秒时间，请耐心等待！")
            self.ui.line_route.clear()
        else:
            self.ui.empty_warn.setText("输入为空，请重新输入!")


class StationWindow(QMainWindow):
    """
    This class represents the window for searching bus stations.

    Attributes:
        app (QApplication): The PyQt5 application.
        main_window (MainWindow): The main window of the application.
        ui (UiStation): The user interface of the station window.
        station_result_window (StationResultWindow): The window displaying bus station search results.

    Methods:
        show_main(): Displays the main window of the application.
        handle_station_search(): Handles the bus station search operation.

    """
    def __init__(self, app, main_window):
        super().__init__()
        self.app = app
        self.main_window = main_window
        self.ui = UiStation()
        self.ui.setupUi(self)
        self.ui.station2main.clicked.connect(self.show_main)
        self.ui.search_station.clicked.connect(self.handle_station_search)
        self.station_result_window = None
        self.ui.empty_warn.setText("查询可能需要几秒时间，请耐心等待！")
        self.ui.line_station.clear()

    def show_main(self):
        self.main_window.show()
        self.close()

    def handle_station_search(self):
        name = self.ui.line_station.text()
        if name.strip():
            station_result = search_bus_stop(str(name))
            self.station_result_window = StationResultWindow(self.app, station_result, self, self.main_window)
            self.station_result_window.show()
            self.hide()
            self.ui.empty_warn.setText("查询可能需要几秒时间，请耐心等待！")
            self.ui.line_station.clear()
        else:
            self.ui.empty_warn.setText("输入为空，请重新输入!")


class RouteResultWindow(QMainWindow):
    """
    This class represents the window displaying bus route search results.

    Attributes:
        app (QApplication): The PyQt5 application.
        route_window (RouteWindow): The window for searching bus routes.
        ui (UiRouteResult): The user interface of the route result window.
        route_result (list or None): The bus route search results.
        route_dir (int): A flag (0 or 1) indicating the direction of the bus route.

    Methods:
        show_main(): Displays the main window of the application.
        show_route(): Displays the window for searching bus routes.
        change_dir(): Changes the direction of displayed bus route information.
        update_route_info(): Updates the displayed bus route information.

    """
    def __init__(self, app, route_result, route_window ,main_window):
        super().__init__()
        self.app = app
        self.main_window = main_window
        self.route_window = route_window
        self.ui = UiRouteResult()
        self.ui.setupUi(self)
        self.ui.result2main.clicked.connect(self.show_main)
        self.ui.result2route.clicked.connect(self.show_route)
        self.ui.change_dir.clicked.connect(self.change_dir)
        self.route_result = route_result
        self.route_dir = 0
        self.update_route_info()

    def show_main(self):
        self.main_window.show()
        self.close()

    def show_route(self):
        self.route_window.show()
        self.close()

    def change_dir(self):
        if self.route_result is not None and len(self.route_result) > 1:
            self.route_dir = 1 - self.route_dir
            self.update_route_info()


    def update_route_info(self):
        if self.route_result is None:
            self.ui.dir.setText("查找的线路不存在！")
            self.ui.dir_2.setText("")
            self.ui.time.setText("")
            self.ui.length.setText("")
            self.ui.num.setText("")
            self.ui.company.setText("")
            self.ui.stops.setText("")
            self.ui.buses.setText("")
            self.ui.stops_2.setText("")
            self.ui.buses_2.setText("")
        elif len(self.route_result) == 1:
            result = self.route_result[0]
            if len(result['dir']) < 20:
                self.ui.dir.setText(result['dir'])
                self.ui.dir_2.setText("")
            else:
                self.ui.dir.setText("")
                self.ui.dir_2.setText(result['dir'])
            self.ui.time.setText(result['time'])
            self.ui.length.setText(result['length'])
            self.ui.num.setText(result['stops_num'])
            self.ui.company.setText(result['company'])
            text_s = ""
            text_b = ""
            for key, value in result['stops'].items():
                text_s += str(key) + '<br>'
                text_b += '●' if value == 1 else '○'
                text_b += '<br>'

            if len(result['stops']) < 35:
                self.ui.stops.setText(text_s)
                self.ui.buses.setText(text_b)
                self.ui.stops_2.setText("")
                self.ui.buses_2.setText("")
            else:
                self.ui.stops.setText("")
                self.ui.buses.setText("")
                self.ui.stops_2.setText(text_s)
                self.ui.buses_2.setText(text_b)
        else:
            result = self.route_result[self.route_dir]
            if len(result['dir']) < 20:
                self.ui.dir.setText(result['dir'])
                self.ui.dir_2.setText("")
            else:
                self.ui.dir.setText("")
                self.ui.dir_2.setText(result['dir'])
            self.ui.time.setText(result['time'])
            self.ui.length.setText(result['length'])
            self.ui.num.setText(result['stops_num'])
            self.ui.company.setText(result['company'])
            text_s = ""
            text_b = ""
            for key, value in result['stops'].items():
                text_s += str(key) + '<br>'
                text_b += '●' if value == 1 else '○'
                text_b += '<br>'

            if len(result['stops']) < 35:
                self.ui.stops.setText(text_s)
                self.ui.buses.setText(text_b)
                self.ui.stops_2.setText("")
                self.ui.buses_2.setText("")
            else:
                self.ui.stops.setText("")
                self.ui.buses.setText("")
                self.ui.stops_2.setText(text_s)
                self.ui.buses_2.setText(text_b)


class StationResultWindow(QMainWindow):
    """
    This class represents the window displaying bus station search results.

    Attributes:
        app (QApplication): The PyQt5 application.
        station_window (StationWindow): The window for searching bus stations.
        ui (UiStationResult): The user interface of the station result window.
        station_result (list or None): The bus station search results.
        station_order (int): The index indicating the currently displayed station result.

    Methods:
        show_main(): Displays the main window of the application.
        show_station(): Displays the window for searching bus stations.
        next_station(): Displays the next station result.
        update_station_info(): Updates the displayed bus station information.

    """
    def __init__(self, app, station_result, station_window , main_window):
        super().__init__()
        self.app = app
        self.main_window = main_window
        self.station_window = station_window
        self.ui = UiStationResult()
        self.ui.setupUi(self)
        self.ui.result2main.clicked.connect(self.show_main)
        self.ui.result2station.clicked.connect(self.show_station)
        self.ui.next_station.clicked.connect(self.next_station)
        self.station_result = station_result
        self.station_order = 0
        self.update_station_info()

    def show_main(self):
        self.main_window.show()
        self.close()

    def show_station(self):
        self.station_window.show()
        self.close()

    def next_station(self):
        if self.station_result:
            self.station_order = (self.station_order + 1) % len(self.station_result)
            self.update_station_info()

    def update_station_info(self):
        if self.station_result is None:
            self.ui.station_name.setText("查找的站点不存在！")
            self.ui.pass_routes.setText("")
        else:
            show_station = self.station_result[self.station_order]
            self.ui.station_name.setText(show_station['name'])
            text = "该站点没有公交线路！" if not show_station['route'] else "<br>".join(map(str, show_station['route']))
            self.ui.pass_routes.setText(text)

