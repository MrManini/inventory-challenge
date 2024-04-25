//aumentar y disminuir todos los elementos
for (let i=1;i<=8;i++){
    const aumentar = document.getElementById("aumentar"+i);
    const disminuir = document.getElementById("disminuir"+i);
    const cantidad=document.getElementById("cantidad_producto"+i)
    
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


var boton_salir=document.getElementById("boton_salir")
boton_salir.addEventListener("click", function(){
  location.href="login.html"
})


var boton_envio=document.getElementById("boton_envio")
boton_envio.addEventListener("click",function(){
  for(let m=1;m<=8;m++){
    const cantidades_ingresadas=document.getElementById("cantidad_producto"+m)
    const valor=parseInt(cantidades_ingresadas.value)
    console.log("Del producto con identificador "+ m+ " se ingresaron "+ valor +" unidades")

  }
})

var redirigir_sacar_elemento=document.getElementById("redirigir_sacar_elemento")

redirigir_sacar_elemento.addEventListener("click",function(){
  location.href="sacar_bodega.html"
})

