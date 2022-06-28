from youtooler.app import Youtooler
from youtooler import utils

def main():
    app = Youtooler()
    
    app.print_logo()

    args = utils.get_arguments()

    if utils.verify_youtube_url(args.url):
        utils.create_storage_dir()
        app.start(args.url)
    else:
        print(utils.get_error_message('INVURL'), utils.stderr)

if __name__ == '__main__':
    main()
