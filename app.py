'''Anzo Avalos Maria Citlalli'''
from flask import Flask, request, jsonify   
import mysql.connector, re    #Nos ayuda a conectarnos a la base de datos 

app = Flask(__name__)

# Configuración de la base de datos
config = {
    'user': 'mroot', #nombre del usuario
    'password': 'Password', 
    'host': 'localhost', 
    'database': 'recuperacion1'
}

def es_clave_valida(clave): #Cumplimiento de ciertos requisitos previos para la contraseña
    if len(clave) < 8:
        return False
    if not re.search(r'[A-Z]', clave):
        return False
    if not re.search(r'[a-z]', clave):
        return False
    if not re.search(r'[0-9]', clave):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', clave):
        return False
    return True

@app.post('/users/add') # Se realiza una solicitud de registro de nuevos usuarios 
def add_usuario():
    data = request.get_json() # Solicitud de datos JSON 
    username = data.get('username')
    clave = data.get('clave')

    if not username or not clave:   #Si Falta alguno de los datos, te marcara error 400
        return {'error': 'Se requieren username y clave'}, 400

    if not es_clave_valida(clave):  #Nos ayuda a verificar si cumple con los requesitos de la contraseña 
        return {'error': 'La clave no cumple con los requisitos'}, 400   #Si no cumple marcara error 400

    cnx = mysql.connector.connect(**config)   #Conexión con base de datos 
    cursor = cnx.cursor()
    query = ("INSERT INTO login (username, correo, clave, fecha_registro, fecha_vencimiento) "
             "VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(query, (data['username'], data['correo'], data['clave'], data['fecha_registro'], data['fecha_vencimiento']))
    cnx.commit()
    cursor.close()
    cnx.close()
    return {'success': 'Usuario registrado con éxito'}, 201 #Nos ayuda a verificar que se aya agregado el usuario correcamete 
                                                            #marcando con exito el registro 
@app.get('/users')        #Se verifica el usuario agregado 
def get_usuarios():        #Nos ayuda a recuperar todos los usuarios registrados desde la base de datos y devolverlos como respuesta
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True) #Indica que devuelva los datos agregados 
    query = "SELECT * FROM login"
    cursor.execute(query)
    users = cursor.fetchall()  #Los resulatdos arrojados, son como una lista de diccionarios
    cursor.close()
    cnx.close()
    return jsonify(users)

@app.post('/users/login')    #Solicitud a usar para posma
def login():    #Nos ayudara a verificar losdatos proporcionados
    data = request.get_json()
    username = data.get('username')
    clave = data.get('clave')  #Nos ayudan a  extraer los datos

    if not username or not clave:
        return {'error': 'Se requieren username y clave'}, 400  #Si falta algunos de los datos que pide marcara un error

    cnx = mysql.connector.connect(**config) #Conexión con la base de datos 
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM login WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close() #Cierre del cursor 
    cnx.close()

    if user and user['clave'] == clave:  # Compara la clave proporcionada con la almacenada
        return {'success': 'Login exitoso'}
    else:
        return {'error': 'Username o clave incorrectos'}, 401


@app.delete('/users/delete')      #Solicitud de eliminacion de usuarios 
def delete_usuario():     #Elimina un usuario de la base de datos basado en el nombre del usuario 
    data = request.get_json()    #Nos ayuda a extraer el valor del username.
    username = data.get('username')
    if not username:
        return {'error': 'No se proporcionó un username'}, 400 

    cnx = mysql.connector.connect(**config) #Conexión de base de datos
    cursor = cnx.cursor()
    query = "DELETE FROM login WHERE username = %s"
    cursor.execute(query, (username,))
    
    if cursor.rowcount == 0:      # Si no se encuentra un usuario para eliminar te dara un error 
        return {'error': 'No se encontró el usuario para eliminar'}, 404
    
    cnx.commit()
    cursor.close()
    cnx.close()
    return {'success': 'Usuario eliminado con éxito'}, 200  # Si la eliminación fue exitosa te dara el mensaje de éxito

@app.put('/users/update')       #Solicitudes de actualización de información de usuarios 
def update_usuario():      # Ayuda a actualizar la información de un usuario en la base de datos 
    data = request.get_json()
    idUsuario = data['idUsuario']    # Nos ayuda a identificar el usuario que se actualizará
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("UPDATE login SET username = %s, correo = %s, clave = %s, fecha_registro = %s, fecha_vencimiento = %s "
             "WHERE idUsuario = %s")   #Se define la culsulta para actualizar los campos.
    cursor.execute(query, (data['username'], data['correo'], data['clave'], data['fecha_registro'], data['fecha_vencimiento'], idUsuario))
    cnx.commit()   #Confirma actualización en la base de datos 
    cursor.close()
    cnx.close()
    return {'success': 'Usuario actualizado con éxito'}, 200      #Si todo salio bien la respuesta sera éxitosa



@app.post('/clientes/add') #Dirección para un nuevo cliente 
def add_cliente():   # agrega un nuevo cliente a la base de datos 
    data = request.get_json()   #Se obtienen los datos 
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("INSERT INTO cliente (IdUsuario, nombre, correo, edad, clave, Numero_productos, Fecha_expiración) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (data['IdUsuario'], data['nombre'], data['Correo'], data['edad'], data['clave'], data['Numero_productos'], data['Fecha_expiración']))
    cnx.commit()
    cursor.close()
    cnx.close()
    return {'success': 'Cliente agregado con éxito'}, 201   #Se agrego el cliente de manera éxitosa

@app.get('/clientes')  #Ruta para información de los clientes 
def get_clientes():  #Ayuda a recuperar toda la información sobre todos los clientes almacenados 
    cnx = mysql.connector.connect(**config)   #Conexión con la base de datos 
    cursor = cnx.cursor(dictionary=True)   #Indica que los datos arojados se deben de dar como diccionarios 
    query = "SELECT * FROM cliente"
    cursor.execute(query)
    clientes = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify(clientes)   #Respuesta JSON



@app.post('/products/add')   #Dirección para agregar a un nuevo producto 
def add_product(): #
    data = request.get_json() #se obtiene datos JSON
    cnx = mysql.connector.connect(**config)  #Conexión con la base de datos 
    cursor = cnx.cursor()
    query = ("INSERT INTO product (IdCliente, nombre_producto, precio_compra, precio_venta, descripción, fecha_caducidad, ingredientes, sabor) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)") #Requerimientos de datos para agregar a un nuevo producto 
    cursor.execute(query, (data['IdCliente'], data['nombre_producto'], data['precio_compra'], data['precio_venta'], data['descripción'], data['fecha_caducidad'], data['ingredientes'], data['sabor']))
    cnx.commit()
    cursor.close()
    cnx.close()
    return {'success': 'Producto agregado con éxito'}, 201   #Si los datos estan correctamente, te da un mensaje de extito 

@app.get('/products')  #Ruta para obtener información 
def get_products():   #Nos da información sobre los productos almacenados 
    cnx = mysql.connector.connect(**config)  #Conexión con la base de datos 
    cursor = cnx.cursor(dictionary=True)  
    query = "SELECT * FROM product"  #Se define una consulta sql para la seleccion de los registros 
    cursor.execute(query)
    products = cursor.fetchall()   #Los resultados se devuelven como una lista, donde cada uno representa un producto con sus atributos.
    cursor.close()
    cnx.close()
    return jsonify(products)


if __name__ == '__main__':   #Nos ayuda a reiniciar el servidor 
    app.run(debug=True)