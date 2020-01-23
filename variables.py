import time

''' End-points '''
comparasURL = 'https://8.teamplace.finneg.com/BSA/api/reports/comparas'
recuperoivaURL = 'https://8.teamplace.finneg.com/BSA/api/reports/recuperoiva'
saldoURL = 'https://8.teamplace.finneg.com/BSA/api/reports/saldo'
pagos = 'https://8.teamplace.finneg.com/BSA/api/reports/analisisordenpago'
proveedores = 'https://8.teamplace.finneg.com/BSA/api/reports/proveedores'
saldo_proveedores = 'https://8.teamplace.finneg.com/BSA/api/reports/saldoproveedores'


'''Datos para obtener token'''
grant_type = 'client_credentials'
client_id = '18ed0830d755e026a1ccc718e88e7cee'
client_secret = 'a44e5d053fe15c6c98fe0c813dfb7614'
token = 'https://8.teamplace.finneg.com/BSA/api/oauth/token'

'''Fechas'''
desde = '2019-01-01'
hasta = time.strftime("%Y-%m-%d")

comprasDesde = '2017-01-01'


path = 'C:/venv'



