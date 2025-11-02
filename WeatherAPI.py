import datetime as dt
import requests
from datetime import date, datetime
from geopy.geocoders import Nominatim
from dateutil.relativedelta import relativedelta 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
import geocoder
import tkinter as tk
from tkinter import simpledialog, messagebox

URL_PAST="https://archive-api.open-meteo.com/v1/archive?"
URL_FUTURE="https://api.open-meteo.com/v1/forecast?"
LAT="52.52"
LONG="13.41"
START="2023-03-30"
END="2023-04-13"
TEMP="temperature_2m"
TODAY = date.today()




def main():
    # Create GUI window
    root = tk.Tk()
    root.title("Weather API")
    root.geometry("1000x700")
    
    # Create matplotlib figure and canvas
    fig = Figure(figsize=(10, 6), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    # Create menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # Create File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Weather Data", menu=file_menu)
    file_menu.add_command(label="1 - Set Location", command=lambda: handle_mode_1(root, canvas, fig))
    file_menu.add_command(label="2 - My Location", command=lambda: handle_mode_2(root, canvas, fig))
    file_menu.add_command(label="3 - Past Weather (7 days)", command=lambda: handle_mode_3(root, canvas, fig))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    # Preload my location on startup
    try:
        responseFuture = MyLocation(show_info=False)
        if responseFuture:
            ShowData(responseFuture, canvas, fig)
    except Exception as e:
        # Silently fail on startup - user can manually select location
        pass
    
    root.mainloop()

def handle_mode_1(root, canvas, fig):
    """Handle mode 1: Set custom location"""
    try:
        responseFuture = Location()
        if responseFuture:
            ShowData(responseFuture, canvas, fig)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather data: {str(e)}")

def handle_mode_2(root, canvas, fig):
    """Handle mode 2: Use my location"""
    try:
        responseFuture = MyLocation()
        if responseFuture:
            ShowData(responseFuture, canvas, fig)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather data: {str(e)}")

def handle_mode_3(root, canvas, fig):
    """Handle mode 3: Past weather"""
    try:
        responsePast = RealTime()
        if responsePast:
            ShowData(responsePast, canvas, fig)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather data: {str(e)}")





def Location():
    geoLocator = Nominatim(user_agent="MyApp")
    location = simpledialog.askstring("Location", "Enter Location:")
    if not location:
        return None
    try:
        Location = geoLocator.geocode(location)
        if not Location:
            messagebox.showerror("Error", "Location not found. Please try again.")
            return None
        lat = str(Location.latitude)
        long = str(Location.longitude)
        messagebox.showinfo("Location Found", 
                          f"Latitude: {Location.latitude}\nLongitude: {Location.longitude}")
        
        urlFuture = URL_FUTURE + "latitude=" + lat + "&longitude=" + long + "&hourly=" + TEMP
        responseFuture = requests.get(urlFuture).json()
        return responseFuture
    except Exception as e:
        messagebox.showerror("Error", f"Failed to geocode location: {str(e)}")
        return None

def MyLocation(show_info=True):
    try:
        g = geocoder.ip('me')
        if not g.latlng:
            messagebox.showerror("Error", "Could not determine your location.")
            return None
        lat = str(g.latlng[0])
        long = str(g.latlng[1])
        if show_info:
            messagebox.showinfo("Location Detected", 
                              f"Latitude: {g.latlng[0]}\nLongitude: {g.latlng[1]}")
        
        urlFuture = URL_FUTURE + "latitude=" + lat + "&longitude=" + long + "&hourly=" + TEMP
        responseFuture = requests.get(urlFuture).json()
        return responseFuture
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get your location: {str(e)}")
        return None


def RealTime():
    try:
        start = TODAY - relativedelta(days=7)
        urlPast = URL_PAST + "latitude=" + LAT + "&longitude=" + LONG + "&start_date=" + str(start) + "&end_date=" + str(TODAY) + "&hourly=" + TEMP
        responsePast = requests.get(urlPast).json()
        return responsePast
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get past weather data: {str(e)}")
        return None


def ShowData(data, canvas, fig):
    try:
        # Clear the figure
        fig.clear()
        ax = fig.add_subplot(111)
        
        # Convert time strings to datetime objects (handle both with and without seconds)
        times = []
        for t in data["hourly"]["time"]:
            try:
                # Try format with seconds first
                times.append(datetime.strptime(t, "%Y-%m-%dT%H:%M:%S"))
            except ValueError:
                # Fall back to format without seconds
                times.append(datetime.strptime(t, "%Y-%m-%dT%H:%M"))
        temperatures = data["hourly"]["temperature_2m"]
        
        # Create the plot
        ax.plot(times, temperatures)
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Temperature (°C)', fontsize=12)
        ax.set_title('Weather Data', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis to reduce ticks and make them readable
        # Use MaxNLocator to limit the number of ticks
        ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
        
        # Format dates nicely - show date and time
        date_format = DateFormatter("%m/%d %H:%M")
        ax.xaxis.set_major_formatter(date_format)
        
        # Rotate labels for better readability
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Adjust layout to prevent label cutoff
        fig.tight_layout()
        
        # Update the canvas
        canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display data: {str(e)}")
    
    
if __name__ == "__main__":
    main()