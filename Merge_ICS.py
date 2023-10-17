import os


def print_intro():
    print("Welcome to ICS Merger.")
    print("Specify the folder path containing .ics files.")
    print("The merged .ics file will be saved in the same folder.")
    print()
    print()


def merge_ics_files(folder_path):
    merged_content = "BEGIN:VCALENDAR\n"

    merged_content += "VERSION:2.0\nPRODID:-//Visual Reality/Calendar Version 1.0/NL\nCALSCALE:GREGORIAN\nX-WR-CALNAME;VALUE=TEXT:badmintonvlaanderen.be\nMETHOD:PUBLISH\nX-MS-OLK-FORCEINSPECTOROPEN:TRUE\nBEGIN:VTIMEZONE\nTZID:Europe/Brussels\nX-LIC-LOCATION:Europe/Brussels\nBEGIN:STANDARD\nTZOFFSETFROM:+0200\nTZOFFSETTO:+0100\nDTSTART:19700101T030000\nRRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETFROM:+0100\nTZOFFSETTO:+0200\nDTSTART:19700101T020000\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU\nEND:DAYLIGHT\nEND:VTIMEZONE"

    for filename in os.listdir(folder_path):
        if filename.endswith(".ics"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                ics_content = file.read()
                events = ics_content.strip().split("BEGIN:VEVENT\n")[
                    1:
                ]  # Split on event start

                for event in events:
                    merged_content += "BEGIN:VEVENT\n" + event

    merged_content += "END:VCALENDAR\n"

    return merged_content


# Specify the folder path containing .ics files
print_intro()
folder_path = input()
folder_path = "/home/woutd/Downloads/Competitie/"
merged_ics_content = merge_ics_files(folder_path)

# Save the merged .ics content to a new file
with open(folder_path + "merged_events.ics", "w", encoding="utf-8") as merged_file:
    merged_file.write(merged_ics_content)
