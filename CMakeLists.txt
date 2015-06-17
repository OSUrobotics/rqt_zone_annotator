cmake_minimum_required(VERSION 2.8.3)
project(rqt_zone_annotator)

find_package(catkin REQUIRED COMPONENTS
  rospy
  rqt_gui
  rqt_gui_py
)
catkin_python_setup()
catkin_package()

install(FILES plugin.xml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY resource
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(PROGRAMS scripts/rqt_zone_annotator
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)