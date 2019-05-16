import os, requests
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, GLib
def main():
  iconpath = os.path.abspath(__file__).replace("main.py","icon.png")
  indicator = appindicator.Indicator.new("customtray", iconpath, appindicator.IndicatorCategory.APPLICATION_STATUS)
  indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
  indicator.set_menu(menu())
  change_label(indicator)
  GLib.timeout_add(5000, change_label, indicator)
  gtk.main()
def menu():
  menu = gtk.Menu()
  exittray = gtk.MenuItem('Exit Tray')
  exittray.connect('activate', quit)
  menu.append(exittray)
  menu.show_all()
  return menu
def change_label(ind_app):
  try:
    j = requests.get("https://api.kraken.com/0/public/Ticker?pair=XXBTZUSD")
    ind_app.set_label(str(round(float(j.json()["result"]['XXBTZUSD']["a"][0]),2)) , '')
  except:
    pass
  return True
def quit(_):
  gtk.main_quit()
if __name__ == "__main__":
  main()

