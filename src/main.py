import packages

def main():

    #inizializza moduli
    pack = packages.Packages()

    while(1):

        print("Inserisci il comando")
        inp = input()

        match inp:
            case "close":
                break
            case "packages":
                pack.install_packages()


if __name__=="__main__":
    main()