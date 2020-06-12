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
    def printit(initial, less ,full,Discharge,connect):
        try:
            print("-->",initial ,less,full)
            URL = 'http://jiofi.local.html/cgi-bin/en-jio/mStatus.html'
            print('aaa')
            page = requests.get(URL)
            print("wwww")
            soup = BeautifulSoup(page.content, 'html.parser')
            name = soup.find(id='lWirelessNwValue')
            charge = soup.find(id='lDashBatteryQuantity')
            status = soup.find(id='lDashChargeStatus').get_text()
            a = int(charge.get_text()[:-1])
            print("charge=", a)
            connect = 1
            if initial == 1:
                if status == "Discharging":
                    Discharge = 1
                if a == 100:
                    rumps.notification(name.get_text(), 'Connected & Full Charge', charge.get_text() + " " + status)
                    initial = 2
                    full = 1
                elif a <= 20:
                    rumps.notification(name.get_text(), 'Connected & Low Charge', charge.get_text() + " " + status)
                    initial = 2
                    less = 1
                    print("less",less)
                else:
                    rumps.notification(name.get_text(), 'Connected', charge.get_text() + " " + status)
                    initial = 2
            print("discharge = ", Discharge)
            print(status)
            if status == "Discharging" and (Discharge == 0 or Discharge == 3):  #Charge -> Discharge
                print('-->',status)
                rumps.notification(name.get_text(), 'Discharging', charge.get_text() + " " + status)
                Discharge = 2
            if status != "Discharging" and (Discharge == 1 or Discharge == 2):  #Discharge -> Charge
                print('-->',status)
                rumps.notification(name.get_text(), 'Charging', charge.get_text() + " " + status)
                Discharge = 3
            if a < 100 and a > 20 and (full == 1 or full==2):#chagre<100 and initiall or current
                print("nott 100")
                full = 3
            if a <= 20 and (less==0 or less == 2):
                less = 3
                print("less", less)
            if a > 20 and less == 1:
                less = 3
                
            if initial == 2 and a == 100 and (full == 0 or full == 3):
                rumps.notification(name.get_text(), "Fully Charged", charge.get_text() + " " + status)
                full = 2
            if initial == 2 and a <= 20 and (less == 0  or less == 3):
                print(initial,a,less,"1111111")
                rumps.notification(name.get_text(), "Battery Low", charge.get_text() + " " + status)
                less = 1
                print("less",less)

            print("ini", initial,less)
        except Exception as e:
            if connect == 0:
                initial = 1
                full = 0
                less = 0
                connect = 0
            else:
                print(e)
                rumps.notification("JioFi", "Not Connected", "Please Connect to JioFi")
                initial = 1
                full = 0
                less = 0
                connect = 0
        threading.Timer(5, printit,[initial,less,full,Discharge,connect]).start()
    printit(1,0,0,0,1)
    AwesomeStatusBarApp("Jio").run()
