import rumps
import requests
from bs4 import BeautifulSoup
import threading
import pkg_resources.py2_warn


class AwesomeStatusBarApp(rumps.App):
    @rumps.clicked("Info")
    def prefs(self, _):
        try:
            url = 'http://jiofi.local.html/cgi-bin/en-jio/mStatus.html'
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            charge = soup.find(id='lDashBatteryQuantity')
            name = soup.find(id='lWirelessNwValue')
            status = soup.find(id='lDashChargeStatus')
            speed = soup.find(id="lulCurrentDataRate")
            cpumin = soup.find(id="lcpuMinUsage")
            cpumax = soup.find(id="lcpuMaxUsage")
            Productid = soup.find(id="lProductID")
            hotname = soup.find(id="lPrimaryHostNameValue")
            ass = "Charge :" + charge.get_text() +"\t\t\tCpu-Min Usage :"+cpumin.get_text()+ "\nStatus:" + status.get_text()+ "\t\tCpu-Max Usage :"+cpumax.get_text()+ "\nSpeed :" + speed.get_text()+"\t\t\tProduct id:"+Productid.get_text()+"\nHOTSPOT NAME :"+ hotname.get_text()
            rumps.alert(name.get_text(), ass)
        except Exception:
            rumps.alert('Please connect to a JioFi',' You are not connected to JioFi')


    @rumps.clicked("Notify")
    def sayhi(self, _):
        try:
            URL = 'http://jiofi.local.html/cgi-bin/en-jio/mStatus.html'
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            name = soup.find(id='lWirelessNwValue')
            speed = soup.find(id="lulCurrentDataRate")
            charge = soup.find(id='lDashBatteryQuantity')
            status = soup.find(id='lDashChargeStatus')
            ass = "Charge :" + charge.get_text() + "\nStatus:" + status.get_text() + "\nSpeed :" + speed.get_text()
            rumps.notification(name.get_text(), "Details", ass)
        except Exception:
            rumps.notification('JioFi', "Not Coonected", "You are not connected to JioFi")

if __name__ == "__main__":
    def printit(val, lav, chr):
        try:
            print("lav",lav,"val",val)
            URL = 'http://jiofi.local.html/cgi-bin/en-jio/mStatus.html'
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            name = soup.find(id='lWirelessNwValue')
            charge = soup.find(id='lDashBatteryQuantity')
            status = soup.find(id='lDashChargeStatus').get_text()
            print(status)
            a = int(charge.get_text()[:-1])
            if status != "Discharging" and chr == 1:
                rumps.notification(name.get_text(), "Your JioFi is " + status, "Charge:" + charge.get_text())
                chr = 2
            if status == "Discharging" and chr == 2:
                rumps.notification(name.get_text(), "Your JioFi is " + status, "Charge:" + charge.get_text())
            if status == "Discharging":
                chr = 1
            if val == 1 and a!= 100 and a>= 20:
                rumps.notification(name.get_text(), "Details", charge.get_text()+status)
            if lav <=2:
                if a < 100 or val == 1:
                    temp = 1
                    lav=2
            if val == 3:
                temp = 2
            print("a=", a)
            if a > 20 and a<100 :
                print("in >")
                lav = 2
            if a ==100 and (temp == 1 or lav == 2 or lav ==7):
                print(temp)
                print("hello")
                rumps.notification(name.get_text(), charge.get_text()+status, "JioFi is Fully Charged")
                temp = temp + 1
                lav = 5
            if a <= 20 and (lav == 2 or lav == 3 or lav == 5) :
                print("working",lav)
                rumps.notification(name.get_text(), "Battery Low", "charge:"+charge.get_text())
                lav = 7
            threading.Timer(5, printit,[3,lav,chr]).start()
            print("temp", temp)
        except Exception:
            rumps.notification("JioFi", "Not Coonected", "Please Connect to JioFi")

    printit(1,1,1)
    AwesomeStatusBarApp("Jio").run()
