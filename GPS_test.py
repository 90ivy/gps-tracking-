import serial
import pynmea2

def parse_gps_data(nmea_sentence):
    try:
        msg = pynmea2.parse(nmea_sentence)
        
        if isinstance(msg, pynmea2.types.talker.GGA):  # GGA sentence for GPS fix data
            latitude = msg.latitude
            longitude = msg.longitude
            altitude = msg.altitude
            hdop = msg.horizontal_dil
            satellites = msg.num_sats
            utc_time = msg.timestamp
            print(f"UTC Time: {utc_time}, Latitude: {latitude}, Longitude: {longitude}")
            print(f"Altitude: {altitude} m, HDOP: {hdop}, Satellites: {satellites}")
            print("--------------------------------------------------------------------")

        elif isinstance(msg, pynmea2.types.talker.RMC):  # RMC sentence for speed and date
            speed = msg.spd_over_grnd
            if speed is not None:
                speed_kmh = speed * 1.852  # Convert knots to km/h
                print(f"Speed: {speed_kmh:.2f} km/h")
            else:
                print("Speed data not available.")
                
            # Extract date and time from RMC
            date = msg.datestamp
            time = msg.timestamp
            print(f"Date: {date}, Time: {time}")

    except pynmea2.ParseError as e:
        print(f"Parse error: {e}")

def read_gps():
    try:
        ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
        
        while True:
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            if data.startswith("$GPGGA") or data.startswith("$GPRMC"):  # Filter for GGA and RMC sentences
                parse_gps_data(data)

    except KeyboardInterrupt:
        print("GPS reading stopped.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_gps()
