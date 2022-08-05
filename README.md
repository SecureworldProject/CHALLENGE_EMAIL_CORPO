# CHALLENGE_EMAIL_CORPO
Challenge que produce una subclave valida si puedes acceder al mail corporativo

IMPORTANTE
Para que el challenge funcione tienes que:
1. Poner en midict["param3"] tu correo electronico
2. Tener la contraseña de la cuenta de correo, hay que pedirla ya que esta en un fichero que no se sube a git

USO DEL CHALLENGE

Este challenge te pregunta si te puede enviar un email y si contestas que si, te envia una clave que tienes que copiar
y pegar en la siguiente ventana que te abra.

CARACTERISTICAS

- Tiene modo parental (con 3 oportunidades) y modo normal
- Tiene un modo fácil: Si estas probando un desarrollo mas grande que incluye este challenge puedes poner la variable easy_mode a True y no te mandará el email, pero te escribirá la clave correcta automáticamente en la ventana en que te la pide
- Aunque no usa capturas, necesita la variable de entorno SECUREMIRROR_CAPTURAS para poder realizar el mecanismo de lock
