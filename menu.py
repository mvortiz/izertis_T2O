import api.provider as pv


def show_menu(options):
    print('Choose an option:')
    for clave in sorted(options):
        print(f' {clave}) {options[clave][0]}')


def read_option(options):
    while (a := input('Option: ')) not in options:
        print('Opción incorrecta, vuelva a intentarlo.')
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
        '4': ('Goodbye!', exit)
    }

    menu(options, '4')


def option1():
    print('You choose the option number 1.')
    client = pv.setup_client()
    rs = client._session
    city_name = "Valdemoro" # input("Name of the city: ")
    start_date = "2025-10-19" # input( "Start date (aaaa-mm-dd): ")
    end_date = "2025-10-21" #input( "End date (aaaa-mm-dd): ")
    pv.get_hourly_weater(client, rs, city_name,start_date, end_date)


def option2():
    print('You choose the option number 2.')
    client = pv.setup_client()
    rs = client._session
    
    city_name = "Valdemoro" # input("Name of the city: ")
    start_date = "2025-10-19" # input( "Start date (aaaa-mm-dd): ")
    end_date = "2025-10-21" #input( "End date (aaaa-mm-dd): ")
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
    
    pv.obtain_temp_statistics(client, rs, city_name, start_date, end_date,above_thr, below_thr)



def option3():
    print('You choose the option number 3.')
    client = pv.setup_client()
    rs = client._session
    
    city_name = "Valdemoro" # input("Name of the city: ")
    start_date = "2025-10-19" # input( "Start date (aaaa-mm-dd): ")
    end_date = "2025-10-21" #input( "End date (aaaa-mm-dd): ")
    pv.obtain_prec_statistics(client, rs, city_name, start_date, end_date)


def exit():
    print('See you soon!')
    exit
