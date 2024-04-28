//para devolverse a la pagina de ingresar elementos a la bodega
var redirigir_ingresar_elementos=document.getElementById("redirigir_ingresar_elemento")

const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
//si no ha iniciado sesion y altera la url, de igual se redirige a la pagina de login
if (!isAuthenticated) {
  window.location.href = 'login.html';
}


redirigir_ingresar_elementos.addEventListener("click",function(){
    location.href="ingresar_bodega.html"
})

var salir=document.getElementById("boton_salir")

salir.addEventListener("click",function(){
  localStorage.setItem('isAuthenticated', 'false');

})
//para salir de la pagina
var boton_salir=document.getElementById("boton_salir")
boton_salir.addEventListener("click", function(){
  location.href="login.html"
})


// para aumentar todos los campos de los elementos
for (let i=1;i<=4;i++){
    const aumentar = document.getElementById("s_aumentar"+i);
    const disminuir = document.getElementById("s_disminuir"+i);
    const cantidad=document.getElementById("s_cantidad_producto"+i)
    
    aumentar.addEventListener("click", () => {
      const currentValue = parseInt(cantidad.value, 10);
      cantidad.value = currentValue + 1;
    });
    
    disminuir.addEventListener("click", () => {
      const currentValue = parseInt(cantidad.value, 10);
      if(currentValue>0){
        cantidad.value = currentValue - 1;
      }
    });
    
  }


