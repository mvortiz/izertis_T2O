import api.provider as pv
import json

bbdd = {}
def show_menu(options):
    print('Choose an option:')
    for clave in sorted(options):
        print(f' {clave}) {options[clave][0]}')


def read_option(options):
    while (a := input('Option: ')) not in options:
        print('Incorrect option, try again.')
    return a


def execute_option(option, options):
    options[option][1]()


def menu(options, exit_option):
    option = None
    while option != exit_option:
        show_menu(options)
        option = read_option(options)
        execute_option(option, options)
        print()


def principal_menu():
    
    options = {
        '1': ('Weather data by city and date range', option1),
        '2': ('Temperature statistics by city and date range', option2),
        '3': ('Precipitation statistics by city and date range', option3),
        '4': ('View stored data', option4),
        '5': ('Goodbye!', exit)
    }

    menu(options, '5')


def option1():
    client = pv.setup_client()
    rs = client._session
    city_name = input("\n\nName of the city: ")
    start_date = input( "Start date (aaaa-mm-dd): ")
    end_date = input( "End date (aaaa-mm-dd): ")
    search = city_name + " " + start_date + " " + end_date
    if search not in bbdd:
        result = pv.get_hourly_weater(client, rs, city_name,start_date, end_date)
        if result != 0: 
            bbdd[search]=result
            print("The data corresponding to have been obtained: " + city_name)
            response = input("Do you want to show them? (y/n)")        
            match response:
                case "y":
                    print(bbdd[search])
    else:
        print("The data is alreay stored. ")
        response = input("Do you want to show them? (y/n)")
        match response:
            case "y":
                print(bbdd[search])
   


def option2():
    client = pv.setup_client()
    rs = client._session
    
    city_name = input("\n\nName of the city: ")
    start_date = input( "Start date (aaaa-mm-dd): ")
    end_date = input( "End date (aaaa-mm-dd): ")
    search = city_name + " " + start_date + " " + end_date

    response = input("Do you want to enter maximum and minimum temperature thresholds? (y/n)")
    match response:
        case "y":
            above_thr = input("umbral max: ")
            below_thr = input("umbral min: ")
        case "n":
            above_thr = 30
            below_thr = 0
        case _:
            print("The response is invalid. Default thresholds will be taken into account.")
    if search not in bbdd:
        pv.obtain_temp_statistics(client=client, session=rs,bbdd=None,name=city_name, start_date=start_date, end_date=end_date,above_thr=above_thr, below_thr=below_thr)
    else:
        value = bbdd[search]
        pv.obtain_temp_statistics(client=client, session=rs, bbdd=value, name=city_name, start_date=start_date, end_date=end_date,above_thr=above_thr, below_thr=below_thr)




def option3():
    client = pv.setup_client()
    rs = client._session
    
    city_name = input("\n\nName of the city: ")
    start_date = input( "Start date (aaaa-mm-dd): ")
    end_date = input( "End date (aaaa-mm-dd): ")
    search = city_name + " " + start_date + " " + end_date
    if search not in bbdd:
        pv.obtain_prec_statistics(client=client, session=rs,bbdd=None,name=city_name, start_date=start_date, end_date=end_date)
    else:
        value = bbdd[search]
        pv.obtain_prec_statistics(client=client, session=rs, bbdd=value, name=city_name, start_date=start_date, end_date=end_date)

def option4():
    response = input("\n\nShow all data (y/n)")
    match response:
        case "y":
            for values in bbdd.values():
                print(values)
        case _:
            response=input("Show only cities stored (y/n)")
            match response:
                case "y":
                    for values in bbdd.values():
                        data = json.loads(values)
                        city_name = data.get("city_name")
                        print(city_name)
                case _:
                    response=input("Show data for a city (y/n)")
                    match response:
                        case "y":
                            city = input("Name of the city: ")
                            stored = 0
                            for key in bbdd.keys():
                                if city in key:
                                    print(bbdd[key])
                                    stored=1
                                    break
                            if stored == 0:
                                print("This city is not in our database.")
                                response = input("Do you want search this city to stored data? (y/n)")
                                if response == "y":
                                    option1()
                

def exit():
    print('\nSee you soon!')
    exit
