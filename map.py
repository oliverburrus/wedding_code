import folium
import math

# --------------------------------------------------
# Helper: generate curved path between two points
# --------------------------------------------------
def curved_line(start, end, arc_height=0.4, steps=20):
    lat1, lon1 = start
    lat2, lon2 = end

    points = []
    for i in range(steps + 1):
        t = i / steps

        # Linear interpolation
        lat = lat1 + (lat2 - lat1) * t
        lon = lon1 + (lon2 - lon1) * t

        # Add arc (sinusoidal bump)
        lat += arc_height * 0.5 * math.sin(math.pi * t)

        points.append([lat, lon])

    return points

# --------------------------------------------------
# Ultra-minimal basemap
# --------------------------------------------------
wedding_map = folium.Map(
    location=[45.75, -123.6],
    zoom_start=8,
    tiles="CartoDB positron",
    scrollWheelZoom=False,
    control_scale=False
)

# --------------------------------------------------
# Day styles (monochrome)
# --------------------------------------------------
DAY_STYLES = {
    "Friday": "#444444",
    "Saturday": "#000000",
    "Sunday": "#888888"
}

# --------------------------------------------------
# Locations (ordered progression)
# --------------------------------------------------
locations = [
    ("PDX Arrival", [45.5898, -122.5951], "Friday"),
    ("Portland Lodging", [45.5152, -122.6784], "Friday"),
    ("Cannon Beach Ceremony", [45.8918, -123.9615], "Saturday"),
    ("Farewell Brunch", [45.5200, -122.6819], "Sunday"),
    ("PDX Departure", [45.5898, -122.5951], "Sunday")
]

# --------------------------------------------------
# Pine tree markers (simple + elegant)
# --------------------------------------------------
for name, coords, day in locations:
    folium.Marker(
        location=coords,
        popup=f"<b>{name}</b><br>{day}",
        icon=folium.Icon(
            icon="tree",
            prefix="fa",
            color="darkgreen",
            icon_color=DAY_STYLES[day]
        )
    ).add_to(wedding_map)

# --------------------------------------------------
# Curved, dotted, red connectors
# --------------------------------------------------
for i in range(len(locations) - 1):
    start = locations[i][1]
    end = locations[i + 1][1]

    curve = curved_line(start, end)

    folium.PolyLine(
        locations=curve,
        color="#8B0000",   # deep muted red
        weight=2,
        opacity=0.85,
        dash_array="4,6"
    ).add_to(wedding_map)

# --------------------------------------------------
# Save output
# --------------------------------------------------
#wedding_map.save("pnw_wedding_map_minimal.html")

print("Saved pnw_wedding_map_minimal.html")
