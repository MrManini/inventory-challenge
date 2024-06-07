const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

//si no ha iniciado sesion y altera la url, de igual se redirige a la pagina de login
if (!isAuthenticated) {
  window.location.href = 'login.html';
}


//aumentar y disminuir todos los elementos
for (let i=1;i<=30;i++){
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
