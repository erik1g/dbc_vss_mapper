import json

def extract_signals_recursive(node):
    signals = []

    # Prüfen: ist das ein Signal?
    node_type = node.get('type')
    if node_type in ('sensor', 'actuator', 'attribute'):
        signal_info = {
            'apiName': node.get('apiName'),
            'name': node.get('name'),
            'type': node_type,
            'datatype': node.get('datatype'),
            'unit': node.get('unit'),
            'description': node.get('description')
        }
        signals.append(signal_info)

    # Rekursiv über Kinder
    children = node.get('children')
    if isinstance(children, dict):
        for child in children.values():
            signals.extend(extract_signals_recursive(child))

    return signals


def parse_vss_file(file_obj):
    import json

    try:
        full_data = json.load(file_obj)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    # Einstiegspunkt: root node z. B. 'Vehicle'
    root_node = None
    if 'Vehicle' in full_data:
        root_node = full_data['Vehicle']
    else:
        raise ValueError("Missing top-level 'Vehicle' key in VSS JSON.")

    signals = extract_signals_recursive(root_node)

    return {
        'full_data': full_data,
        'signals': signals
    }
