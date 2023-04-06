import supertimerII as st2,os



if __name__ == "__main__":
    creds = st2.get_google_credentials()
    sheet_id, sheet_range = st2.get_spreadsheet_id()
    values = st2.read_google_sheet(creds,sheet_id, sheet_range)
    vehicles=[]
    is_not_header_row=False
    for row in values:
        if is_not_header_row:
            vehicles.append(row[1])
        else:
            is_not_header_row = True
    runs,races = st2.calc_race_and_runs(len(values)-1)
    #runs = int(input("How many runs would you like to do? "))
    print(values)
    ser = st2.connect_to_track()
    for run in range(runs):
        
        for race in range(races):
            new_range = st2.race_range(sheet_range,run,race)
            os.system("clear")
            print("Run "+str(run+1)+" Race "+str(race+1))
            print("LANE 1: "+vehicles[4*race])
            if 4*race+1 < len(vehicles):
                print("LANE 2: "+vehicles[4*race+1])
            if 4*race+2<len(vehicles):
                print("LANE 3: "+vehicles[4*race+2])
            if 4*race+3<len(vehicles):
                print("LANE 4: "+vehicles[4*race+3])
            results = {}
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
            print("Results...")
            race_results=[]
            for car in results:
                car_int = int(car)
                race_results.append([vehicles[4*race+car_int-1],results[car]])
            print(race_results)
            #Increase sheet_range by 1 column
            print("Make any adjustments in Google Sheet and then....")
            cont=input("Press return to continue")
            st2.update_google_sheet(creds,sheet_id,new_range,race_results)
        vehicles = st2.sort_vehicles(vehicles=vehicles,run=run,sheet_id=sheet_id,sheet_range=sheet_range,creds=creds)
    print("Race Over")

