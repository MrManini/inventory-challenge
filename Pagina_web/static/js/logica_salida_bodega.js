// para aumentar todos los campos de los elementos
for (let i=1;i<=30;i++){
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


