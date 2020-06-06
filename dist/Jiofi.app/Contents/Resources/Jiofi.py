import rumps
import requests
from bs4 import BeautifulSoup
import threading
import pkg_resources.py2_warn


class AwesomeStatusBarApp(rumps.App):
    @rumps.clicked("Info")
    def prefs(self, _):
        URL = 'http://jiofi.local.html/cgi-bin/en-jio/mStatus.html'
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        charge = soup.find(id='lDashBatteryQuantity')
        name = soup.find(id='lWirelessNwValue')
        status = soup.find(id='lDashChargeStatus')
        speed = soup.find(id="lulCurrentDataRate")
        ass = "Charge :" + charge.get_text() + "\nStatus:" + status.get_text() + "\nSpeed :" + speed.get_text()
        # print(ass)
        rumps.alert(name.get_text(), ass)
    # @rumps.clicked("Silly button")
    # def onoff(self, sender):
    #     sender.state = not sender.state

    @rumps.clicked("Notify")
    def sayhi(self, _):
        URL = 'http://jiofi.local.html/cgi-bin/en-jio/mStatus.html'
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.find(id='lWirelessNwValue')
        speed = soup.find(id="lulCurrentDataRate")
        charge = soup.find(id='lDashBatteryQuantity')
        status = soup.find(id='lDashChargeStatus')
        ass = "Charge :" + charge.get_text() + "\nStatus:" + status.get_text() + "\nSpeed :" + speed.get_text()
        # print(ass)
        rumps.notification(name.get_text(), "Details", ass)

if __name__ == "__main__":
    def printit(val, lav):
        print("lav",lav,"val",val)
        URL = 'http://jiofi.local.html/cgi-bin/en-jio/mStatus.html'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.find(id='lWirelessNwValue')
        charge = soup.find(id='lDashBatteryQuantity')
        status = soup.find(id='lDashChargeStatus').get_text()
        a=int(charge.get_text()[:-1])
        # print(charge.get_text(), a, status)
        # print("val", val)
        if lav <=2:
            if a < 100 or val == 1:
                # print("<")
                temp = 1
                lav=2
        if val == 3:
            temp = 2
        print("a=",a)
        if a ==100 and (temp == 1 or lav == 2 or lav ==7):
            print(temp)
            print("hello")
            rumps.notification(name.get_text(), charge.get_text()+status, "JioFi is Fully Charged")
            temp = temp + 1
            lav = 5
        if a < 20 and (lav == 2 or lav == 3 or lav == 5):
            
            print("working",lav)
            rumps.notification(name.get_text(), "Battery Low", "charge:"+charge.get_text())
            lav = 7

            
        
        threading.Timer(5, printit,[3,lav]).start()
            
        
        print("temp",temp)
    printit(1,1)
    AwesomeStatusBarApp("Jio").run()
