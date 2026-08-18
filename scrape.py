#data from https://www.ign.com/wikis/pokemon-pokopia/Habitat_Dex_List_-_How_to_Make_All_Habitats_and_Requirements
#find the main table element and copy all html into "snippet.html"

from bs4 import BeautifulSoup
import json, re

def proc(s,lower):
    s = re.sub(r"^\d+. ", "", s)
    if lower:
        s = s.lower()
        s = s[0].upper() + s[1:]
    return s

if __name__ == "__main__":

    INPUT_FILE = "snippet.html"
    OUTPUT_FILE = "data.json"

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    table = soup.find("table")

    # Get headers, excluding Habitat Image and Checklist
    headers = [
        th.get_text(" ", strip=True)
        for th in table.find_all("th")
    ]

    exclude = {"Habitat Image", "Checklist", "Discoverable Pokemon"}
    headers = [h for h in headers if h not in exclude]

    data = []

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")

        if not cells:
            continue

        # Skip Habitat Image (index 0) and Checklist (index 5)
        cells = cells[1:-2]

        entry = {}

        for header, cell in zip(headers, cells):
            # Preserve lists as JSON arrays
            items = cell.find_all("li")

            if items:
                entry[header] = [
                    proc(item.get_text(" ", strip=True), header == "Requirements")
                    for item in items
                ]
            else:
                entry[header] = proc(cell.get_text(" ", strip=True), header == "Requirements")

        data.append(entry)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(data)} entries to {OUTPUT_FILE}")