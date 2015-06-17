from python_qt_binding import loadUi
from python_qt_binding.QtGui import QWidget, QTreeWidgetItem,\
    QFileDialog
from python_qt_binding.QtCore import Qt, QTimer, QAbstractListModel,\
    QModelIndex
from python_qt_binding.QtCore import Signal
import os
import rospkg
from rqt_bag.plugins import raw_view

from peac_bridge.msg import ControlActuation

import yaml

import rospy

from genpy.message import strify_message


class MainWidget(QWidget):
    new_msg = Signal(ControlActuation)

    def __init__(self, zone_yaml_path):
        super(MainWidget, self).__init__()
        ui_file = os.path.join(
            rospkg.RosPack().get_path('rqt_zone_annotator'),
            'resource',
            'zone_widget.ui'
        )


        self.zone_yaml_path = zone_yaml_path
        with open(zone_yaml_path, 'r') as zone_file:
            self.zones = [z['Name'] for z in yaml.load(zone_file)['Zone List']]

        self.load_zone_dict()
        loadUi(ui_file, self)
        self.msgWidget = raw_view.MessageTree(self)
        self.msgLayout.addWidget(self.msgWidget)
        self.new_msg.connect(self.update_msg_widget)
        self.control_sub = rospy.Subscriber('/control_actuated', ControlActuation, self.control_cb)
        self.zoneListWidget.addItems(self.zones)

        self.setZoneButton.clicked.connect(self.add_control)

    def control_cb(self, msg):
        self.new_msg.emit(msg)

    def update_msg_widget(self, msg):
        self.msgWidget.set_message(msg)
        for item in self.msgWidget.get_all_items():
            item.setExpanded(True)

    def add_control(self):
        try:
            msg_dict = yaml.load(strify_message(self.msgWidget.msg))
            zone = self.zoneListWidget.selectedItems()[0].text()
            if zone not in self.zone_dict:
                self.zone_dict[zone] = []

            self.zone_dict[zone].append(msg_dict)
        except:
            import pdb; pdb.set_trace()  # breakpoint 82a32b6a //

    def load_zone_dict(self):
        parts = self.zone_yaml_path.split('.yaml')
        parts[0] += '_collected_controls'
        out_path = '.yaml'.join(parts)
        if os.path.exists(out_path):
            with open(out_path, 'r') as out_file:
                self.zone_dict = yaml.load(out_file)
                if self.zone_dict is None:
                    self.zone_dict = {}                    
        else:
            self.zone_dict = {}

    def shutdown(self):
        self.control_sub.unregister()
        parts = self.zone_yaml_path.split('.yaml')
        parts[0] += '_collected_controls'
        out_path = '.yaml'.join(parts)

        with open(out_path, 'w+') as outfile:
            yaml.dump(self.zone_dict, outfile)