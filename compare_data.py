import json


def read_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    return json_data


def write_json(data):
    with open('alerts.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_data(file) -> list:
    data = read_json(file)
    messages = data["messages"]

    all_alarms = []
    for message in messages:
        if message["text"] != "":
            obj = get_instance(
                date=message["date"],
                data=message["text"]
            )
            if obj['flag'] == 'air alert':
                all_alarms.append(obj)

    return all_alarms


def get_instance(date, data):
    region = ''
    flag = ''

    for m in data:
        if isinstance(m, dict):
            if m.get("type") == "hashtag":
                region = m["text"].replace("#", "")
            if m.get("type") == "bold":
                flag = get_alert_flag(m["text"])

    return {
        'date': date,
        'region': region,
        'flag': flag,
    }


def get_alert_flag(text):
    if "🔴" in text:
        return "air alert"
    if "🟢" in text:
        return "all clear"
    if "🟡" in text:
        return "all clear"
    return None
