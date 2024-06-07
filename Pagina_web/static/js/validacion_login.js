var boton=document.getElementById("boton_envio")
var correo=document.getElementById("correo")
var contraseña=document.getElementById("contraseña")

function aut(){
    if((correo.value=="jhonatan@hotmail.com" && contraseña.value=="12345") || (correo.value=='admin' && contraseña.value=='12345')){
        localStorage.setItem('isAuthenticated', 'true');
        location.href="ingresar_bodega.html"
    }else{
        alert("credenciales incorrectas")
        localStorage.setItem('isAuthenticated', 'false');

    }

}
boton.addEventListener("click",aut)




