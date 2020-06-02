import pandas as pd
import requests
from time import sleep
try:
    from io import BytesIO as IO # for legacy python
except:
    from io import StringIO as IO

def handle_uploaded_file(file, columna_seriales):

    columna = str(columna_seriales)
    file_xlsx = pd.read_excel(file)
    seriales = []
    for i in file_xlsx[columna]:
        if str(i) != 'nan':
            seriales.append(str(i))

    chunk = chunked(seriales, 20)
    token = api_token()
    dataFrame_contratos = api_contracts(token, chunk)
    dataFrame_eox = api_eox(token, chunk, dataFrame_contratos)
    return dataFrame_eox


def chunked(SN,limit):
    # Divide 20 en 20
    chunk = []
    for i in range(0,len(SN),limit):
        chunk.append(SN[i:i+limit])
    return chunk


def api_token():
    URL = 'https://cloudsso.cisco.com/as/token.oauth2'
    client_id = '2pc3f8j2evy75k6bdgnuzj5b'
    client_secret = 'FDnRYa3szTtvabQVtaUE5JBB'

    HEADERS = {
        'content-type':'application/x-www-form-urlencoded'
    }
    DATA = {
        'grant_type':'client_credentials',
        'client_id':client_id,
        'client_secret':client_secret
    }
    req = requests.post(url=URL,data=DATA,headers=HEADERS).json()
    return req['access_token']


def api_eox(token,chunk, lista_contratos):
    HEADERS = {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % (token)
    }
    comma = ','

    data_api = []
    for i in range(len(chunk)):
        URL = 'https://api.cisco.com/supporttools/eox/rest/5/EOXBySerialNumber/%s' % (comma.join(chunk[i])) + '?responseencoding=json'
        data_api.append(requests.get(url=URL,headers=HEADERS).json())

    #print(data_api[0]['EOXRecord'][0])

    aux_index = 0

    for w in range(len(lista_contratos[0])):
        lista_contratos[6].append(0)
        lista_contratos[7].append(0)
        lista_contratos[8].append(0)
        lista_contratos[9].append(0)
        lista_contratos[10].append(0)
        lista_contratos[11].append(0)
        lista_contratos[12].append(0)
        lista_contratos[13].append(0)
        lista_contratos[14].append(0)


    for x in range(len(data_api)):
        for i in range(len(data_api[x]['EOXRecord'])):
            if len(data_api[x]['EOXRecord'][i]['EOXInputValue'].split(',')) > 1:
                lista_aux = data_api[x]['EOXRecord'][i]['EOXInputValue'].split(',')
                for j in lista_aux:
                    aux_index = lista_contratos[0].index(j)
                    #SN
                    lista_contratos[6][aux_index] = (j)
                    #EOLProductID
                    if len(data_api[x]['EOXRecord'][i]['EOLProductID']) > 0:
                        lista_contratos[7][aux_index] = (data_api[x]['EOXRecord'][i]['EOLProductID'])
                    else:
                        lista_contratos[7][aux_index] = (data_api[x]['EOXRecord'][i]['EOXError']['ErrorDataValue'])
                    #EOXExternalAnnouncementDate
                    if len(data_api[x]['EOXRecord'][i]['EOXExternalAnnouncementDate']['value']) > 0:
                        lista_contratos[8][aux_index] = (data_api[x]['EOXRecord'][i]['EOXExternalAnnouncementDate']['value'])
                    else:
                        lista_contratos[8][aux_index] = 'Not Announced'
                    #EndOfSaleDate
                    if len(data_api[x]['EOXRecord'][i]['EndOfSaleDate']['value']) > 0:
                        lista_contratos[9][aux_index] = (data_api[x]['EOXRecord'][i]['EndOfSaleDate']['value'])
                    else:
                        lista_contratos[9][aux_index] = 'Not Announced'
                    #LastDateOfSupport
                    if len(data_api[x]['EOXRecord'][i]['LastDateOfSupport']['value']) > 0:
                        lista_contratos[10][aux_index] = (data_api[x]['EOXRecord'][i]['LastDateOfSupport']['value'])
                    else:
                        lista_contratos[10][aux_index] = 'Not Announced'
                    #EndOfSWMaintenanceReleases
                    if len(data_api[x]['EOXRecord'][i]['EndOfSWMaintenanceReleases']['value']) > 0:
                        lista_contratos[11][aux_index] = (data_api[x]['EOXRecord'][i]['EndOfSWMaintenanceReleases']['value'])
                    else:
                        lista_contratos[11][aux_index] = 'Not Announced'
                    #EndOfRoutineFailureAnalysisDate
                    if len(data_api[x]['EOXRecord'][i]['EndOfRoutineFailureAnalysisDate']['value']) > 0:
                        lista_contratos[12][aux_index] = (data_api[x]['EOXRecord'][i]['EndOfRoutineFailureAnalysisDate']['value'])
                    else:
                        lista_contratos[12][aux_index] = 'Not Announced'
                    #EndOfServiceContractRenewal
                    if len(data_api[x]['EOXRecord'][i]['EndOfServiceContractRenewal']['value']) >0:
                        lista_contratos[13][aux_index] = (data_api[x]['EOXRecord'][i]['EndOfServiceContractRenewal']['value'])
                    else:
                        lista_contratos[13][aux_index] = 'Not Announced'
                    #EndOfSvcAttachDate
                    if len(data_api[x]['EOXRecord'][i]['EndOfSvcAttachDate']['value']) > 0:
                        lista_contratos[14][aux_index] = (data_api[x]['EOXRecord'][i]['EndOfSvcAttachDate']['value'])
                    else:
                        lista_contratos[14][aux_index] = 'Not Announced'
#-------------------------------------------------------------------------------------------------------------------------------------------
            else:

                aux_index = lista_contratos[0].index(data_api[x]['EOXRecord'][i]['EOXInputValue'])
                #SN
                lista_contratos[6][aux_index] = (data_api[x]['EOXRecord'][i]['EOXInputValue'])
                #EOLProductID
                if len(data_api[x]['EOXRecord'][i]['EOLProductID']) > 0:
                    lista_contratos[7][aux_index] = (data_api[x]['EOXRecord'][i]['EOLProductID'])
                else:
                    lista_contratos[7][aux_index] = (data_api[x]['EOXRecord'][i]['EOXError']['ErrorDataValue'])
                #EOXExternalAnnouncementDate
                if len(data_api[x]['EOXRecord'][i]['EOXExternalAnnouncementDate']['value']) > 0:
                    lista_contratos[8][aux_index] = (data_api[x]['EOXRecord'][i]['EOXExternalAnnouncementDate']['value'])
                else:
                    lista_contratos[8][aux_index] = 'Not Announced'
                #EndOfSaleDate
                if len(data_api[x]['EOXRecord'][i]['EndOfSaleDate']['value']) > 0:
                    lista_contratos[9][aux_index] = (data_api[x]['EOXRecord'][i]['EndOfSaleDate']['value'])
                else:
                    lista_contratos[9][aux_index] = 'Not Announced'
                #LastDateOfSupport
                if len(data_api[x]['EOXRecord'][i]['LastDateOfSupport']['value']) > 0:
                    lista_contratos[10][aux_index] = (data_api[x]['EOXRecord'][i]['LastDateOfSupport']['value'])
                else:
                    lista_contratos[10][aux_index] = 'Not Announced'
                #EndOfSWMaintenanceReleases
                if len(data_api[x]['EOXRecord'][i]['EndOfSWMaintenanceReleases']['value']) > 0:
                    lista_contratos[11][aux_index] = (data_api[x]['EOXRecord'][i]['EndOfSWMaintenanceReleases']['value'])
                else:
                    lista_contratos[11][aux_index] = 'Not Announced'
                #EndOfRoutineFailureAnalysisDate
                if len(data_api[x]['EOXRecord'][i]['EndOfRoutineFailureAnalysisDate']['value']) > 0:
                    lista_contratos[12][aux_index] = (data_api[x]['EOXRecord'][i]['EndOfRoutineFailureAnalysisDate']['value'])
                else:
                    lista_contratos[12][aux_index] = 'Not Announced'
                #EndOfServiceContractRenewal
                if len(data_api[x]['EOXRecord'][i]['EndOfServiceContractRenewal']['value']) >0:
                    lista_contratos[13][aux_index] = (data_api[x]['EOXRecord'][i]['EndOfServiceContractRenewal']['value'])
                else:
                    lista_contratos[13][aux_index] = 'Not Announced'
                #EndOfSvcAttachDate
                if len(data_api[x]['EOXRecord'][i]['EndOfSvcAttachDate']['value']) > 0:
                    lista_contratos[14][aux_index] = (data_api[x]['EOXRecord'][i]['EndOfSvcAttachDate']['value'])
                else:
                    lista_contratos[14][aux_index] = 'Not Announced'


    dataFrame = pd.DataFrame({
        'SN1':lista_contratos[0],
        #'SN2':lista_contratos[6],
        'PID': lista_contratos[3],
        'Covered': lista_contratos[1],
        'Contrato': lista_contratos[5],
        'Contract End Date': lista_contratos[2],
        'Garantía': lista_contratos[4],
        'EOX': lista_contratos[8],
        'EOS': lista_contratos[9],
        'LDOS': lista_contratos[10],
        'EOSWR': lista_contratos[11],
        'EORFA': lista_contratos[12],
        'EOSCR': lista_contratos[13],
        'EOSAD': lista_contratos[14]
        })

    return dataFrame


def api_contracts(token,chunk):
    HEADERS = {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % (token)
    }
    comma = ','
    chunk_convered = []
    for i in range(len(chunk)):
        URL = 'https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s'%(comma.join(chunk[i]))
        chunk_convered.append(requests.get(url=URL,headers=HEADERS).json())

    info_contratos = chunk_convered
    lista_contratos = [[] for i in range(15)]
    for j in range(len(info_contratos)):
        for i in range(len(info_contratos[j]['serial_numbers'])):
            #contract_site_address1
            #lista_contratos[0].append(info_contratos[j]['serial_numbers'][i]['contract_site_address1'])
            #SerialNumber
            lista_contratos[0].append(info_contratos[j]['serial_numbers'][i]['sr_no'])
            #is_covered
            lista_contratos[1].append(info_contratos[j]['serial_numbers'][i]['is_covered'])
            #covered_product_line_end_date
            lista_contratos[2].append(info_contratos[j]['serial_numbers'][i]['covered_product_line_end_date'])
            #orderable_pid_list
            #lista_contratos[2].append(info_contratos[j]['serial_numbers'][i]['orderable_pid_list'][0]['item_description'])
            lista_contratos[3].append(info_contratos[j]['serial_numbers'][i]['orderable_pid_list'][0]['orderable_pid'])
            #warranty_end_date
            lista_contratos[4].append(info_contratos[j]['serial_numbers'][i]['warranty_end_date'])
            #service_contract_number
            lista_contratos[5].append(info_contratos[j]['serial_numbers'][i]['service_contract_number'])
    '''
    dataFrame = pd.DataFrame({
        'SerialNumber':lista_contratos[0],
        'Estatus Contrato': lista_contratos[1],
        'Fecha Fin de Contrato' : lista_contratos[2],
        'PID': lista_contratos[3],
        'Fin de Garantía': lista_contratos[4],
        'Numero de Contrato': lista_contratos[5]
        })
    '''

    return lista_contratos


if __name__ == "__main__":
    handle_uploaded_file()
