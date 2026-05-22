import argparse

from google.oauth2 import service_account
from googleapiclient.discovery import build
from ruamel.yaml import YAML

SCOPES = ["https://www.googleapis.com/auth/forms.body"]


def update_form_item(service, form_id, item_id, data):
    """Update a Google Form dropdown with the current list of Master's/PhD students."""
    options = sorted(
        name for name, info in data.items()
        if (info.get("current_role") or {}).get("title") in ("Master's", "PhD")
    )
    options.append("I won't need mentorship.")

    response = (
        service.forms()
        .batchUpdate(
            formId=form_id,
            body={
                "requests": [
                    {
                        "updateItem": {
                            "item": {
                                "itemId": item_id,
                                "questionItem": {
                                    "question": {
                                        "choiceQuestion": {
                                            "options": [{"value": name} for name in options]
                                        }
                                    }
                                },
                            },
                            "updateMask": "questionItem.question.choiceQuestion.options",
                        }
                    }
                ]
            },
        )
        .execute()
    )
    print("Form item updated:", response)


def main():
    parser = argparse.ArgumentParser(
        description="Update a Google Form item based on authors.yml data."
    )
    parser.add_argument("service_account_file", help="Path to the service account credentials file.")
    parser.add_argument("yaml_file_path", help="Path to the YAML file containing data.")
    parser.add_argument("form_id", help="ID of the Google Form to update.")
    parser.add_argument("item_id", help="ID of the form item to update.")
    args = parser.parse_args()

    credentials = service_account.Credentials.from_service_account_file(
        args.service_account_file, scopes=SCOPES
    )
    service = build("forms", "v1", credentials=credentials)

    yaml = YAML()
    with open(args.yaml_file_path) as f:
        data = yaml.load(f)

    update_form_item(service, args.form_id, args.item_id, data)


if __name__ == "__main__":
    main()
