import DrunkClassification

def main():

    # create Model
    pt = DrunkClassification.classify_person("Server/Classification/new.csv", threshold=0.06)
    print(pt)

   

if __name__ == "__main__":
    main()