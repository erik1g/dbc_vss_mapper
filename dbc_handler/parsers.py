import cantools

def parse_dbc(file):
    # Lade DBC aus Datei-Inhalt
    dbc_content = file.read().decode('utf-8')
    db = cantools.database.load_string(dbc_content, 'dbc')

    parsed = {
        "messages": []
    }

    for message in db.messages:
        message_dict = {
            "message_name": message.name,
            "frame_id": hex(message.frame_id),
            "length": message.length,
            "senders": message.senders,
            "comment": message.comment,
            "signals": []
        }

        for signal in message.signals:
            # Choices in saubere Liste umwandeln
            if signal.choices:
                choices_list = [
                    {"value": k, "label": getattr(v, 'name', str(v))}
                    for k, v in signal.choices.items()
                ]
            else:
                choices_list = None

            signal_dict = {
                "signal_name": signal.name,
                "start_bit": signal.start,
                "length": signal.length,
                "byte_order": signal.byte_order,
                "is_signed": signal.is_signed,
                "scale": signal.scale,
                "offset": signal.offset,
                "min": signal.minimum,
                "max": signal.maximum,
                "unit": signal.unit or "",
                "choices": choices_list
            }

            message_dict["signals"].append(signal_dict)

        parsed["messages"].append(message_dict)

    return parsed



