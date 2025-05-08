from pathlib import Path
from datetime import datetime

today = datetime.today().strftime("%Y%m%d")

def generate_start_calendar_intervals():
    # Weekday 2 (Monday) to 6 (Friday) + Weekday 7 (Saturday early AM)
    weekdays = [2, 3, 4, 5, 6, 7]
    output = []

    for wd in weekdays:
        # Nighttime hours (22, 23) and early morning (0–5)
        for hr in ([22, 23] if wd in range(2, 6) else []) + ([0, 1, 2, 3, 4, 5] if wd in range(3, 8) else []):
            for minute in list(range(0,60,5)):
                block = f"""    <dict><key>Weekday</key><integer>{wd}</integer><key>Hour</key><integer>{hr}</integer><key>Minute</key><integer>{minute}</integer></dict>"""
                output.append(block)

    return '\n'.join(output)


if __name__ == "__main__":
    root = Path.cwd()
    fallback_dir = root / "launch_agents"
    fallback_dir.mkdir(exist_ok=True)

    output_path = fallback_dir / f"{today}_snippet_StartCalendarInterval.xml"
    xml_blocks = generate_start_calendar_intervals()
    with open(output_path, "w") as f:
        f.write(xml_blocks)

    print(f"✅ Schedule snippet written to: {output_path}")