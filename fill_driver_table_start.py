import os

from report_of_monaco_racing import groper

from my_app.fill_driver_table import fill_driver_table

if __name__ == "__main__":
    fill_driver_table(groper(os.environ.get("RACE_INFO_DIR")))
