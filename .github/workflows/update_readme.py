import requests

# Fetch moon phase data
moon_phase_response = requests.get("https://www.moonphases.co.uk/api/current-phase")
moon_phase = moon_phase_response.json()["phase"]

# Fetch live celestial events data (dummy URL, replace with actual API if available)
events_response = requests.get("https://space-event-tracker.herokuapp.com/api/live-events")
events = events_response.json()

# Read the README file
with open("README.md", "r") as file:
    readme = file.readlines()

# Update the moon phase and live events sections
for i, line in enumerate(readme):
    if "![Moon Phase]" in line:
        readme[i] = f"![Moon Phase](https://www.moonphases.co.uk/api/current-phase) - {moon_phase}\n"
    if "![Live Events]" in line:
        readme[i] = f"![Live Events](https://space-event-tracker.herokuapp.com/api/live-events) - {events}\n"

# Write the updated README file
with open("README.md", "w") as file:
    file.writelines(readme)
