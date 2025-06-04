import uuid
import json
import sys


def main():
    deploy = { "deploy_id" : str(uuid.uuid4())}
    print(json.dumps(deploy))



if __name__ == "__main__":
    main()