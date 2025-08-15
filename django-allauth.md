# 📄 Documentación de Configuración de `django-allauth`

Esta configuración define cómo se comporta el sistema de autenticación de **Django** utilizando **django-allauth**, incluyendo inicios de sesión, cierres de sesión, formularios personalizados y métodos de autenticación.

---

## 1️⃣ Configuración de rutas de Login y Logout

```python
LOGIN_REDIRECT_URL = "/"      # Redirige a esta URL después de iniciar sesión
LOGOUT_REDIRECT_URL = "/"     # Redirige a esta URL después de cerrar sesión
ACCOUNT_LOGOUT_ON_GET = True  # Permite cerrar sesión simplemente accediendo a /logout/
```

### 💡 Explicación:
- **`LOGIN_REDIRECT_URL`**: Página a la que se envía al usuario después de iniciar sesión.
- **`LOGOUT_REDIRECT_URL`**: Página a la que se envía después de cerrar sesión.
- **`ACCOUNT_LOGOUT_ON_GET`**: Si está en `True`, el logout se hace solo visitando la URL `/logout/`.  
  Esto es útil para evitar confirmaciones, pero no es recomendado si se quiere prevenir cierres de sesión accidentales.

---

## 2️⃣ Backends de autenticación

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Autenticación tradicional de Django
    "allauth.account.auth_backends.AuthenticationBackend",  # Autenticación de django-allauth
]
```

### 💡 Explicación:
- **`ModelBackend`**: Autenticación básica de Django usando usuario y contraseña.
- **`AuthenticationBackend`** de **allauth**: Permite autenticación con métodos adicionales (correo, redes sociales, etc.).

---

## 3️⃣ Configuración de proveedores sociales

```python
SOCIALACCOUNT_PROVIDERS = {}
```

💡 **Explicación**:  
- Aquí se definen los proveedores como Google, Facebook, GitHub, etc.
- Ejemplo de integración con Google:
```python
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "TU_CLIENT_ID",
            "secret": "TU_SECRET",
            "key": ""
        }
    }
}
```

---

## 4️⃣ Formularios personalizados

```python
ACCOUNT_FORMS = {
    "add_email": "allauth.account.forms.AddEmailForm",
    "change_password": "allauth.account.forms.ChangePasswordForm",
    "confirm_login_code": "allauth.account.forms.ConfirmLoginCodeForm",
    "login": "allauth.account.forms.LoginForm",
    "request_login_code": "allauth.account.forms.RequestLoginCodeForm",
    "reset_password": "allauth.account.forms.ResetPasswordForm",
    "reset_password_from_key": "allauth.account.forms.ResetPasswordKeyForm",
    "set_password": "allauth.account.forms.SetPasswordForm",
    "signup": "allauth.account.forms.SignupForm",
    "user_token": "allauth.account.forms.UserTokenForm",
}
```

💡 **Explicación**:  
Cada clave indica el formulario que **allauth** usará para cada proceso.  
Puedes reemplazar las rutas por tus propios formularios para personalizar validaciones o apariencia.

---

## 5️⃣ Sesiones

```python
ACCOUNT_SESSION_REMEMBER = False
```

💡 **Explicación**:
- Si está en `True`, el usuario permanecerá autenticado aunque cierre el navegador.
- En `False`, la sesión expira cuando el navegador se cierra.

---

## 6️⃣ Métodos de inicio de sesión

```python
ACCOUNT_LOGIN_METHODS = {"username", "email"}
```

💡 **Explicación**:
- Define con qué datos puede iniciar sesión el usuario.
- Opciones comunes:
  - `{"username"}`
  - `{"email"}`
  - `{"username", "email"}` (como en este caso).

⚠ **Importante**:  
Si se usa junto con `ACCOUNT_SIGNUP_FIELDS`, los campos deben coincidir para evitar advertencias (`W001`).

---

## 7️⃣ Campos del formulario de registro

```python
ACCOUNT_SIGNUP_FIELDS = {
    "email*",
    "password1*",
    "password2*",
}
```

💡 **Explicación**:
- Indica qué campos se solicitan al registrarse.
- El `*` indica que son **obligatorios**.
- Para agregar más campos personalizados, se debe extender el formulario de registro.

---

## 8️⃣ Correo electrónico único

```python
ACCOUNT_UNIQUE_EMAIL = True
```

💡 **Explicación**:
- Garantiza que no haya dos cuentas con el mismo email.
- Ideal para evitar duplicados en la base de datos.

---

## ⚠ Posibles advertencias (`W001`)
La advertencia:
```
ACCOUNT_LOGIN_METHODS conflicts with ACCOUNT_SIGNUP_FIELDS
```
Significa que los métodos de inicio de sesión (`username`, `email`) no coinciden con los campos que el formulario de registro está pidiendo.  
Para corregirlo:
- Si permites login con `username`, también pide `username` en `ACCOUNT_SIGNUP_FIELDS`.
- Si solo usas email, elimina `username` de `ACCOUNT_LOGIN_METHODS`.

---

## 📌 Ejemplo de configuración limpia

```python
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = {"email*", "password1*", "password2*"}
```

O si quieres **usuario y email**:

```python
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = {"username*", "email*", "password1*", "password2*"}
```

---

✍ **Luis Mario Cervantes Suárez**: Configuración adaptada y documentada para un proyecto Django profesional con `django-allauth`.
