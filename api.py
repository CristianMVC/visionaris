import requests
import csv
import variables
import sys
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import codecs
import logging


reload(sys)
sys.setdefaultencoding('utf8')
logging.basicConfig(filename=variables.path+'/log.log', filemode='w', level=logging.DEBUG)
logging.info('Comienzo...')
logging.info(variables.hasta)
def obtenerToken():
    ''' login a la api  '''

    params = {
        "grant_type": variables.grant_type,
        "client_id": variables.client_id,
        "client_secret": variables.client_secret,
    }
    result = requests.get(variables.token, params = params)
    if result.ok:
        return result.content

def comprasEnColumnas(token, empresa):
    '''Libro de iva compras en columna'''

    auth = {'Authorization': 'Bearer ' + token}

    result = requests.get(variables.comparasURL +'? \
                           &PARAMWEBREPORT_fechaDesde='+variables.desde+'\
                           &PARAMWEBREPORT_fechaHasta='+variables.hasta+' \
                           &PARAMWEBREPORT_exposicionFiscal=IVACOM\
                               &PARAMWEBREPORT_Empresa='+empresa, headers=auth)

    return result

def analisisFacturaCompras(token, empresa):
    '''Analisis de factura de compras - recupero iva'''

    auth = {'Authorization': 'Bearer ' + token}
    params = (('FechaDesde', variables.desde), ('FechaHasta', variables.hasta), ('PARAMEmpresa', empresa))

    result = requests.get(variables.recuperoivaURL, params=params, headers=auth)

    return result

def saldo_proveedores(token, empresa):
    '''Obtener saldo proveedores'''

    auth = {'Authorization': 'Bearer ' + token}
    params = (('PARAMWEBREPORT_FechaHasta', variables.hasta), ('PARAMWEBREPORT_Empresa', empresa))

    result = requests.get(variables.saldo_proveedores, params=params, headers=auth)

    return result



def escribir1(param_1, nombre_archivo):
    ''' exportar datos a csv '''

    with codecs.open(nombre_archivo, 'wb', encoding='iso-8859-1') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONE, escapechar='\\')
        spamwriter.writerow(['TransaccionID', 'Fecha', 'Comprobante', 'CUIT', 'Proveedor', 'Iva_cf_2100',
                             'Neto_grav_2100_iva_cf', 'Neto_grav_1050_iva_cf',
                              'Iva_cf_1050', 'Neto_grav_2700_iva_cf', 'Iva_cf_2700',
                              'Tipo', 'Documento','Cat_siap','Cod_cat_fiscal', 'Exento', 'PER_IIBB', 'PERCEP_IVA', 'TOTAL'])

        for w in param_1:

            spamwriter.writerow([w['TRANSACCIONID'], w['FECHACOMPROBANTE'], w['COMPROBANTEDOCUMENTO'], w['CUIT'], w['ORGANIZACION'],
                                 w['IVA CF 21.00%'],
                                 w['NETO GRAV. 21.00% - IVA CF'],
                                 w['NETO GRAV. 10.50% - IVA CF'],
                                 w['IVA CF 10.50%'],
                                 w['NETO GRAV. 27.00% - IVA CF'],
                                 w['IVA CF 27.00%'], w['COMPROBANTETIPO'], w['DOCUMENTO'], w['CATEGORIASIAP'],
                                 w['CODIGOCATEGORIAFISCAL'], w['EXENTO'], w['PER. IIBB'], w['PERCEP IVA'], w['TOTAL']])




def escribir2(param_2, nombre_archivo):
    ''' exportar datos a csv '''

    with codecs.open(nombre_archivo, 'wb',  encoding='iso-8859-1') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONE, escapechar='\\')
            spamwriter.writerow(['TransaccionID', 'Fecha','FechaComprobante', 'Doc.-nro. interno', 'Organizacion', 'Comprobante', 'Condicion pago',
                                 'Producto', 'Cuenta', 'Cantidad', 'Unidad', 'Precio', 'Precio sobre', 'Importe',
                                 'Gravado', 'No gravado', 'Moneda', 'Cotizacion', 'Proveedor', 'Ano', 'ano - mes',
                                 'Empresa', 'Tasa impositiva','Estado', 'Prov. origen', 'cai/cae', 'Subfamilia',
                                 'familia', 'Rubro', 'Marca', 'IdentificacionExterna'])

            for w in param_2:
                spamwriter.writerow([w['TRANSACCIONID'], w['FECHA'], w['FECHACOMPROBANTE'], w['DOCNROINT'], w['ORGANIZACION'], w['COMPROBANTE'],
                                     w['CONDICIONPAGO'], w['PRODUCTO'], w['CUENTA'], w['CANTIDAD'], w['UNIDADVENTA'],
                                     w['PRECIO'],w['PRECIOSOBRE'], w['IMPORTE'], w['GRAVADO'], w['NO GRAVADO'], w['MONEDA'],
                                     w['COTIZACION'], w['PROVEEDOR'], w['ANO'], w['ANO-MES'], w['EMPRESA'], w['GRAVADOPORTASAIMPOSITIVA'],
                                     w['ESTADO'], w['PROVINCIAORIGEN'], w['CAI/CAE'], w['SUBFAMILIA'], w['FAMILIA'], w['RUBRO'], w['MARCA'],
                                     w['IDENTIFICACIONEXTERNA']])


def escribir5(param_5, nombre_archivo):
    ''' exportar datos a csv '''

    with codecs.open(nombre_archivo, 'wb', encoding='iso-8859-1') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONE, escapechar='\\')
            spamwriter.writerow(['FECHA', 'DOCUMENTO', 'COMPROBANTE', 'ORGANIZACION', 'IMPORTE', 'CODIGO', 'SALDOFACTURA',
                                 'DOCUMENTOFECHA', 'FECHACOMPROBANTE'])

            for w in param_5:
                spamwriter.writerow([w['FECHA'], w['DOCUMENTO'],w['COMPROBANTE'],w['ORGANIZACION'],w['IMPORTE'],w['CODIGO'],
                                      w['SALDOFACTURA'],w['DOCUMENTOFECHA'], w['FECHACOMPROBANTE']])



def main(empresa):
    ''' llamado a todas las funciones '''

    token = obtenerToken()

    param_1 = comprasEnColumnas(token, empresa)
    param_2 = analisisFacturaCompras(token, empresa)
    param_5 = saldo_proveedores(token, empresa)

    if param_1.ok and param_2.ok and param_5.ok:

        param_1 = param_1.json()
        param_2 = param_2.json()
        param_5 = param_5.json()

        if empresa == 'EMPRE_0241':
            try:
              escribir1(param_1, variables.path+'/Patagonia/libroIVA.csv')
              escribir2(param_2, variables.path+'/Patagonia/Analisis.csv')
              escribir5(param_5, variables.path+'/Patagonia/Saldo_proveedores.csv')
              logging.info('=======================')
              logging.info('ok Patagonia')
              logging.info('=======================')
            except ValueError:
              logging.error("Error con Patagonia")  

           
        if empresa == 'EMPRESA345':
            try:
              escribir1(param_1, variables.path+'/Cabresto/libroIVA.csv')
              escribir2(param_2, variables.path+'/Cabresto/Analisis.csv')
              escribir5(param_5, variables.path+'/Cabresto/Saldo_proveedores.csv')
              logging.info('=======================')
              logging.info('ok Cabresto')
              logging.info('=======================')
            except ValueError:
              logging.error("Error con Cabresto")   


        if  empresa == 'EMPRE_0347':
            try:
              escribir1(param_1, variables.path+'/Azul/libroIVA.csv')
              escribir2(param_2, variables.path+'/Azul/Analisis.csv')
              escribir5(param_5, variables.path+'/Azul/Saldo_proveedores.csv')
              logging.info('=======================')
              logging.info('ok Azul')
              logging.info('=======================')
            except ValueError:
              logging.info("Error con Azul")

        if empresa == 'IFSSA53':
             try:
               escribir1(param_1, variables.path+'/Sur/libroIVA.csv')
               escribir2(param_2, variables.path+'/Sur/Analisis.csv')
               escribir5(param_5, variables.path+'/Sur/Saldo_proveedores.csv')
               logging.info('=======================')
               logging.info('ok Sur')
               logging.info('=======================')
             except ValueError:
               logging.error("Error con Sur")
             

        if empresa == 'EMPRE01':
           try:
             escribir1(param_1, variables.path+'/South/libroIVA.csv')
             escribir2(param_2, variables.path+'/South/Analisis.csv')
             escribir5(param_5, variables.path+'/South/Saldo_proveedores.csv')
             logging.info('=======================')
             logging.info('ok South')
             logging.info('=======================')
           except ValueError:
             logging.error("Error con South")

    else:
        logging.error('Error en el servicio')




main('EMPRE_0241')
main('EMPRESA345')
main('EMPRE_0347')
main('IFSSA53')
main('EMPRE01')
logging.info('=======================')
print('Finalizado...')

