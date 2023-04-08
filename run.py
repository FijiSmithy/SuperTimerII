from app import app
import sys

if __name__ == "__main__":
    n = len(sys.argv)
    if n > 1:
        portn = int(sys.argv[1])
    else:
        portn = 8080
    if n > 2:
        if sys.argv[2] == "ssl":
            print("Running in SSL")
            app.run(host='0.0.0.0', port=portn , debug=False, ssl_context='adhoc')
        else:
            app.run(host='0.0.0.0', port=portn , debug=True)
    else:
        app.run(host='0.0.0.0', port=8080 , debug=True)
