from modules import launch_utils
from modules import auth


args = launch_utils.args
prepare_environment = launch_utils.prepare_environment
start = launch_utils.start

def switch():
    global login
    login.close()
    start().launch()

def main():
    global login
    if args.dump_sysinfo:
        filename = launch_utils.dump_sysinfo()
        print(f"Sysinfo saved as {filename}. Exiting...")
        exit(0)

    launch_utils.startup_timer.record("initial startup")
    prepare_environment()
    with launch_utils.startup_timer.subcategory("prepare environment"):
            prepare_environment()

    login = auth.create_login_interface()
    login.launch()  
    start().launch()

if __name__ == "__main__":
    main()