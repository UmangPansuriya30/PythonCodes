import json

# Load the uploaded file
file_path = "temp.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract only localizedAspectName and values (aspectValues.localizedValue)
simplified = []

for aspect in data.get("refinement").get("aspectDistributions", []):
    name = aspect.get("localizedAspectName")
    values = [val.get("localizedAspectValue") for val in aspect.get("aspectValueDistributions", [])]
    simplified.append({
        "localizedAspectName": name,
        "values": values
    })
    
with open("simplified_aspects.json", "w", encoding="utf-8") as f:
    json.dump(simplified, f, ensure_ascii=False, indent=4)
