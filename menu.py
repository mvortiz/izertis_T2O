import api.provider as pv


def show_menu(options):
    print('Seleccione una opción:')
    for clave in sorted(options):
        print(f' {clave}) {options[clave][0]}')


def read_option(options):
    while (a := input('Opción: ')) not in options:
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
        '1': ('Carga de datos metereologicos', option1),
        '2': ('Estadisticas de temperatura', option2),
        '3': ('Estadisticas de precipitacion', option3),
        '4': ('Salir', exit)
    }

    menu(options, '4')


def option1():
    print('Has elegido la opción 1')
    client = pv.setup_client()
    rs = client._session
    city_name = "Valdemoro" # input("Introduce el nombre la de ciudad: ")
    start_date = "2025-10-19" # input( "Fecha inicio para la carga de datos (aaaa-mm-dd): ")
    end_date = "2025-10-21" #input( "Fecha fin para la carga de datos (aaaa-mm-dd): ")
    pv.get_hourly_weater(client, rs, city_name,start_date, end_date)


def option2():
    print('Has elegido la opción 2')
    client = pv.setup_client()
    rs = client._session
    
    city_name = "Valdemoro" # input("Introduce el nombre la de ciudad: ")
    start_date = "2025-10-19" # input( "Fecha inicio para la carga de datos (aaaa-mm-dd): ")
    end_date = "2025-10-21" #input( "Fecha fin para la carga de datos (aaaa-mm-dd): ")
    response = input("¿Desea introducir umbrales de temperatura máxima y mínima? (y/n)")
    match response:
        case "y":
            above_thr = input("umbral max: ")
            below_thr = input("umbral min: ")
        case "n":
            above_thr = 30
            below_thr = 0
        case _:
            print("La respuesta no es válida. Se tendrán en cuenta los umbrales por defecto.")
    
    pv.obtain_temp_statics(client, rs, city_name, start_date, end_date,above_thr, below_thr)



def option3():
    print('Has elegido la opción 3')
    client = pv.setup_client()
    rs = client._session
    
    city_name = "Valdemoro" # input("Introduce el nombre la de ciudad: ")
    start_date = "2025-10-19" # input( "Fecha inicio para la carga de datos (aaaa-mm-dd): ")
    end_date = "2025-10-21" #input( "Fecha fin para la carga de datos (aaaa-mm-dd): ")
    pv.obtain_rain_statics(client, rs, city_name, start_date, end_date)


def exit():
    print('Saliendo')
    exit
