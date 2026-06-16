import os, yaml
from .models import AuthInfo, MatrixConfig


def read_config(auth_info: AuthInfo) -> MatrixConfig | None:
    config = auth_info.CONFIG
    if not os.path.exists(config):
        print(f"❌ Error - File {config} is not found")
        return
    try:
        with open(config, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data is None:
                print(f"❌ Error - File {config} is empty")
                return
            return data
    except yaml.YAMLError as err:
        print(f"❌ Error - Parsing YAML: {err}")
    except PermissionError:
        print(f"❌ Error - No permissions for reading")
    except OSError as err:
        print(f"❌ Error - OS error: {err}")
    except Exception as err:
        print(f"❌ Error - {err}")
    return
