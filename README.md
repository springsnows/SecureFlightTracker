# SecureFlightTracker


Matthias Schäfer, Martin Strohmeier, Vincent Lenders, Ivan Martinovic and Matthias Wilhelm.
"Bringing Up OpenSky: A Large-scale ADS-B Sensor Network for Research".
In Proceedings of the 13th IEEE/ACM International Symposium on Information Processing in Sensor Networks (IPSN), pages 83-94, April 2014.


# HOW TO RUN

1. Download all files.

2. Open your terminal and navigate to the project folder:

   ```bash
   cd "C:\Users\your_name\Documents\GitHub\SecureFlightTracker"
   ```

3. Install all required dependencies:

   ```pip install -r requirements.txt
   ```

4. Run the following command:

   ```bash
   uvicorn app:app --reload
   ```

5. The app will be running at:  
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

6. Open the link in your web browser.