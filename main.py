import os, requests, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, GLib, Notify as notify
show_alert=0
prev_price=0
exchanges=["kraken","binance","bitstamp"]
exchange="kraken"
window=None
def main():
  app_name = "btc_price_ind_kraken"
  iconpath = os.path.abspath(__file__).replace("main.py","icon.png")
  indicator = appindicator.Indicator.new(app_name, iconpath, appindicator.IndicatorCategory.APPLICATION_STATUS)
  indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
  indicator.set_menu(menu())
  notify.init(app_name)
  change_label(indicator)
  GLib.timeout_add(10000, change_label, indicator)
  gtk.main()
def menu():
  menu = gtk.Menu()
  exittray = gtk.MenuItem('Exit Tray')
  exittray.connect('activate', quit)
  menu.append(exittray)
  exittray = gtk.MenuItem('Settings')
  exittray.connect('activate', show_settings)
  menu.append(exittray)
  menu.show_all()
  return menu
def change_label(ind_app):
  global prev_price, show_alert
  try:
    if exchange == "kraken":
      price = float(requests.get("https://api.kraken.com/0/public/Ticker?pair=XXBTZUSD").json()["result"]['XXBTZUSD']["a"][0])
    elif exchange == "binance":
      price = float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()["price"])
    elif exchange == "bitstamp":
      price = float(requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd").json()["last"])
    if show_alert and ((price>float(show_alert) and prev_price<price) or (price<float(show_alert) and prev_price>price)):
      show_notif(price)
      show_alert=0
    prev_price = price
    ind_app.set_label(str(round(price,2)),"")
  except Exception as e:
    print(e)
  return True
def set_alert(win):
  global show_alert
  try:
   show_alert=float(win.entry.get_text())
  except:
   show_alert=0
def show_notif(price):
  notify.Notification.new("BTC price", str(price), None).show()
def show_settings(_):
  global window
  window = gtk.Window()
  window.set_focus()
  window.set_position(gtk.WindowPosition.CENTER)
  window.set_title('Settings')
  window.box = gtk.Box(orientation=gtk.Orientation.HORIZONTAL,spacing=7)
  window.add(window.box)
  vbox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=7)
  window.box.pack_start(vbox, True, True, 10)
  label = gtk.Label()
  label.set_text("Set price for showing alert")
  label.set_justify(gtk.Justification.LEFT)
  vbox.pack_start(label, True, True, 7)
  window.entry = gtk.Entry()
  window.entry.set_text("0")
  vbox.pack_start(window.entry, True, True, 7)
  label2 = gtk.Label()
  label2.set_text("Choose exchange")
  label2.set_justify(gtk.Justification.LEFT)
  vbox.pack_start(label2, True, True, 7)
  exchange_list = gtk.ListStore(str)
  for el in exchanges:
    exchange_list.append([el])
  window.combobox = gtk.ComboBox.new_with_model(exchange_list)
  renderer_text = gtk.CellRendererText()
  window.combobox.pack_start(renderer_text, True)
  window.combobox.add_attribute(renderer_text, "text", 0)
  window.combobox.set_active(exchanges.index(exchange))
  vbox.pack_start(window.combobox, True, True, 7)
  but = gtk.Button.new_with_label("Save")
  vbox.pack_start(but, True, True, 7)
  but.connect("clicked", save_prefs)
  window.connect("destroy", save_prefs)
  window.show_all()
def save_prefs(widget):
  global window,exchange
  exchange = exchanges[window.combobox.get_active()]
  set_alert(window)
  try:
    window.destroy()
  except:
    pass
def quit(_):
  gtk.main_quit()
if __name__ == "__main__":
  main()

