import subprocess
def main():

    while(1):

        print("Inserisci il comando")
        inp = input()

        match inp:
            case "close":
                break
            case "packages":
                install_packages()

def install_packages(packages):
    run = ["./install.sh"] + packages
    exec = subprocess.call(run)
    return exec


if __name__=="__main__":
    main()