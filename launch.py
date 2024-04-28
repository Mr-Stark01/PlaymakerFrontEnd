from modules import launch_utils
from modules import auth

args = launch_utils.args
prepare_environment = launch_utils.prepare_environment
start = launch_utils.start

def main():
    if args.dump_sysinfo:
        filename = launch_utils.dump_sysinfo()
        print(f"Sysinfo saved as {filename}. Exiting...")
        exit(0)

    login_interface = auth.create_login_interface()
    login_interface.launch()  

    launch_utils.startup_timer.record("initial startup")
    with launch_utils.startup_timer.subcategory("prepare environment"):
<<<<<<< Updated upstream
            prepare_environment()
=======
        prepare_environment()
        print("fldkgalésdf")
    print("sdfae")
>>>>>>> Stashed changes
    start()

if __name__ == "__main__":
    main()