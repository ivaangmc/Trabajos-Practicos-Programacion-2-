from mailjet_rest import Client

# Tus credenciales configuradas
api_key = '96be6d35fd49f7e7ebdc90715051b1d4'
api_secret = '1931879f346aa58c32d47a0916e4c144'

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

data = {
  'Messages': [
    {
      "From": {
        "Email": "ivangmclp@gmail.com",
        "Name": "Ivan"
      },
      "To": [
        {
          "Email": "ivangmclp@gmail.com", 
          "Name": "Ivan Moreira"
        }
      ],
      "Subject": "Entrega TP Programación 2",
      "TextPart": "hola este es el tp de programacion 2 , espero que ande !!",
      "HTMLPart": "<h3>TP Programación 2</h3><p>hola este es el tp de programacion 2 , espero que ande !!</p>"
    }
  ]
}

# Ejecutar el envío
result = mailjet.send.create(data=data)

# Verificación en consola
print(f"Código de estado: {result.status_code}")
if result.status_code == 200:
    print("¡Éxito! El correo fue enviado correctamente.")
else:
    print("Hubo un error al enviar.")
    print(result.json())