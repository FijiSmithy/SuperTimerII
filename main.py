import supertimerII as st2,os, sys
import urllib3
urllib3.disable_warnings()


if __name__ == "__main__":
    #Check if any arguments have been passed
    if len(sys.argv)>1:
        if sys.argv[1] == "-s":
            simulate = True
        else:
            simulate = False
    creds = st2.get_google_credentials()
    if simulate:
        sheet_id, sheet_range = st2.get_spreadsheet_id("1aU_FeQ5vXvhdkVY4Yhm8OXZPIzVA6VONYIU4QHy3cFU","Car List!A:D")
    else:
        sheet_id, sheet_range = st2.get_spreadsheet_id()
    values = st2.read_google_sheet(creds,sheet_id, sheet_range)
    vehicles=[]
    is_not_header_row=False
    for row in values:
        if is_not_header_row:
            vehicles.append(row[1])
        else:
            is_not_header_row = True
    #At this point we have a complete list of the vehicles.
    runs,races = st2.calc_race_and_runs(len(values)-1)
    #runs = int(input("How many runs would you like to do? "))
    os.system("clear")
    print("Welcome...")
    print("Number of racers: ",len(vehicles))
    print("Number of recommended runs: ",str(runs))
    print("Number of races per run: ",str(races))
    cont = input("Press return to continue...")
    print("Connecting to track.....")
    ser = st2.connect_to_track()
    for run in range(0,runs):
        
        for race in range(0,races):
            new_range = st2.race_range(sheet_range,run,race)
            os.system("clear")
            stats ={"current":{},"next":{}}
            print("Run "+str(run+1)+" Race "+str(race+1))
            for i in range(0,4):
               
                if 4*race+i < len(vehicles):
                    print("LANE "+str(int(i+1))+": "+vehicles[4*race+i])
                    stats["current"][str(int(i+1))]=vehicles[4*race+i]
                if 4*(race+1)+i <len(vehicles):
                    print("Next LANE "+str(int(i+1))+": "+vehicles[4*(race+1)+i])
                    stats["next"][str(int(i+1))]=vehicles[4*(race+1)+i]
            st2.post_stats(stats)           
            results = {}
            line = ser.readline()
            str_line = line.decode("utf-8")
            str_line = str_line.replace("\r","").replace("\n","").replace(" ","")
            while "#" not in str_line and "!" in str_line:
                print("Waiting for Race...")
                line = ser.readline()
                str_line = line.decode("utf-8")
                str_line = str_line.replace("\r","").replace("\n","").replace(" ","")
            while str_line != "!":
                if "#" in str_line:
                    key = str_line.replace("#","")
                else:
                    results[key]=str_line
                line = ser.readline()
                str_line = line.decode("utf-8")
                str_line = str_line.replace("\r","").replace("\n","").replace(" ","")
            print("\n")
            os.system("clear")
            print("Results...")
            race_results=[]
            for car in results:
                car_int = int(car)
                race_results.append([vehicles[4*race+car_int-1],results[car]])
            print(race_results)
            #Increase sheet_range by 1 column
            st2.update_google_sheet(creds,sheet_id,new_range,race_results)
            print("Make any adjustments in Google Sheet and then....")
            cont=input("Press return to continue")
        print("Go to the Sheet and sort the results")
        cont=input("Press return to continue....")
        if run+1 < runs:
            vehicles = st2.sort_vehicles(creds=creds,run=run,sheet_range=sheet_range,sheet_id=sheet_id,header=True)
    print("Race Over")

