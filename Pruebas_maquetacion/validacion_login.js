var boton=document.getElementById("boton_envio")
var correo=document.getElementById("correo")
var contraseña=document.getElementById("contraseña")


boton.addEventListener("click",function(){
    if(correo.value=="jhonatan@hotmail.com" && contraseña.value=="12345"){
        location.href="ingresar_bodega.html"
    }else{
        alert("credenciales incorrectas")
    }
})





