import os

from hello_settings import SECRETS_DICT, PROJECT_PATH


if __name__ == '__main__':
    os.environ['AWS_ACCESS_KEY_ID'] = SECRETS_DICT['AWS_ACCESS_KEY_ID']
    os.environ['AWS_SECRET_ACCESS_KEY'] = SECRETS_DICT['AWS_SECRET_ACCESS_KEY']
    spawn_server_yml = os.path.join(PROJECT_PATH, 'devops/spawn_server.yml')
    os.system('ansible-playbook {}'.format(spawn_server_yml))
