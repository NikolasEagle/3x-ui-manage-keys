import os, yaml
from .models import AuthInfo, MatrixConfig, MatrixUser, Remark


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
            remarks = data["remarks"]
            for remark in remarks:
                remarks[remark] = Remark(**remarks[remark])
                users = remarks[remark].users
                for i in range(len(users)):
                    users[i] = MatrixUser(**users[i])
            return MatrixConfig(**data)
    except yaml.YAMLError as err:
        print(f"❌ Error - Parsing YAML: {err}")
    except PermissionError:
        print(f"❌ Error - No permissions for reading")
    except OSError as err:
        print(f"❌ Error - OS error: {err}")
    except Exception as err:
        print(f"❌ Error - {err}")
    return
