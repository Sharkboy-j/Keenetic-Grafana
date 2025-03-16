import logging
import re


def isstring(value): return isinstance(value, str)


def isfloat(value: str): return re.match(r'^-?\d+(?:\.\d+)?$', value) is not None


def isinteger(value: str): return re.match(r'^\d+$', value) is not None


def isvalidmetric(value): return isinstance(value, int) or isinstance(value, float) or isinstance(value, bool)

def is_temperature(value: str) -> bool:
    pattern = r'^-?\d+(?:\.\d+)?\s*\(?[CFK]\)?$'
    return re.match(pattern, value) is not None

def is_voltage(value: str) -> bool:
    # Регулярное выражение для напряжения (V)
    return re.match(r'^-?\d+(?:\.\d+)?\s*\(?V\)?$', value) is not None

def is_current(value: str) -> bool:
    # Регулярное выражение для тока (mA)
    return re.match(r'^-?\d+(?:\.\d+)?\s*\(?mA\)?$', value) is not None

def is_power(value: str) -> bool:
    # Регулярное выражение для мощности (dBm)
    return re.match(r'^-?\d+(?:\.\d+)?\s*\(?dBm\)?$', value) is not None

def extract_number(value: str) -> float:
    match = re.search(r'-?\d+(?:\.\d+)?', value)
    if match:
        return float(match.group())  # Преобразуем найденное число в float
    else:
        raise ValueError("No numeric value found in the string")

def extract_number_with_unit(value: str, unit: str) -> float:
    if re.search(r'\(?' + re.escape(unit) + r'\)?', value):
        return extract_number(value)
    else:
        raise ValueError(f"The string does not contain the unit '{unit}'")

type_mapping = {
    "yes": 1,
    "no": 0,
    "up": 1,
    "down": 0,
    True: 1,
    False: 0,
    "MOUNTED": 1,
    "UNMOUNTED": 0
}


def normalize_value(value):
    if value is None:
        return None

    value = type_mapping.get(value) if type_mapping.get(value) is not None else value

    if isstring(value):
        value = parse_string(value)

    if isvalidmetric(value):
        return value
    else:
        logging.warning("Value: " + str(value) + " is not valid metric type")
        return None


def parse_string(value):
    value = remove_data_unit(value)

    if isinteger(value):
        value = int(value)
    elif isfloat(value):
        value = float(value)


    return value


#def remove_data_unit(value: str):
#    return value.replace(" kB", "")
def remove_data_unit(value: str) -> str:
    # Регулярное выражение для удаления единиц измерения
    pattern = r'\s*\(?(C|V|mA|dBm|mW)\)?'
    return re.sub(pattern, '', value)