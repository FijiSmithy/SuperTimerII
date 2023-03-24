import supertimerII as st2



if __name__ == "__main__":
    creds = st2.get_google_credentials()
    values = st2.read_google_sheet(creds)
    st2.calc_race_and_runs(len(values)-1)
    