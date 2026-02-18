import os
import json

custom_dir = "law_management/law_management/custom"
fixtures_dir = "law_management/fixtures"

if not os.path.exists(fixtures_dir):
    os.makedirs(fixtures_dir)

all_custom_fields = []
all_property_setters = []

# Fields to strip from fixtures to ensure v15 compatibility and clean imports
STRIP_FIELDS = [
    "_assign", "_comments", "_liked_by", "_user_tags", 
    "creation", "modified", "modified_by", "owner", 
    "idx", "name", "parent", "parentfield", "parenttype"
]

def clean_doc(doc):
    return {k: v for k, v in doc.items() if k not in STRIP_FIELDS}

if os.path.exists(custom_dir):
    for filename in os.listdir(custom_dir):
        if filename.endswith(".json"):
            with open(os.path.join(custom_dir, filename), "r") as f:
                data = json.load(f)
                if "custom_fields" in data:
                    for field in data["custom_fields"]:
                        field["doctype"] = "Custom Field"
                        all_custom_fields.append(clean_doc(field))
                if "property_setters" in data:
                    for setter in data["property_setters"]:
                        setter["doctype"] = "Property Setter"
                        all_property_setters.append(clean_doc(setter))

if all_custom_fields:
    with open(os.path.join(fixtures_dir, "custom_field.json"), "w") as f:
        json.dump(all_custom_fields, f, indent=1)

if all_property_setters:
    with open(os.path.join(fixtures_dir, "property_setter.json"), "w") as f:
        json.dump(all_property_setters, f, indent=1)

print(f"Consolidated {len(all_custom_fields)} clean custom fields and {len(all_property_setters)} clean property setters.")
