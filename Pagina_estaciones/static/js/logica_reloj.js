//-----------------------------------------------Cronometro de actividad----------------------------------------------------------------
let hr=min=sec=ms="0"+0,startTimer;

let hora=document.querySelector(".horas")
let minutos=document.querySelector(".minutos")
let segundos=document.querySelector(".segundos")
let milisegundos=document.querySelector(".milisegundos")
let boton_envio=document.querySelector(".envio_tiempo")

function start(){
    const currentDateTime = new Date();
    console.log("Recogiendo en bodega inicio a la fecha "+ currentDateTime.toLocaleString())
    if(sec2>1){
        stop2()

    }
    startTimer=setInterval(()=>{
        //se usa ms++ con los ++ despues para que se retorne el valor antes
        //del incremento y, por ende, empieza a contar en cero
        ms++;
        ms=ms<10? "0"+ms:ms;
        if(ms==100){
            sec++;
            sec=sec<10? "0"+sec:sec;
            ms="0"+0;
        }
        if(sec==60){
            min++
            min=min<10?"0"+min:min;
            sec="0"+0;
        }
        if(min==60){
            hr++
            hr=hr<10?"0"+hr:hr;
            min="0"+0;
        }
        putValue()
    },10)
}

function stop(){
    clearInterval(startTimer);
    const currentTime = new Date();
    console.log("Recogiendo en bodega termino a las "+ currentTime.toLocaleTimeString()+" el tiempo en bodega fue: "+hr+":"+min+":"+sec+":"+ms)
    hora.value=hr
    minutos.value=min
    segundos.value=sec
    milisegundos.value=ms
    boton_envio.click()
    reset2()
    start2()
}

function reset(){

    clearInterval(startTimer);
    hr=min=sec=ms="0"+0;
    putValue()
}

function putValue(){
    document.querySelector(".millisecond").innerHTML=ms
    document.querySelector(".second").innerHTML=sec
    document.querySelector(".minute").innerHTML=min
    document.querySelector(".hour").innerHTML=hr
}

//-------------------------------------Manejar el QR-------------------------------------------------------------------------------------

var myqr=document.getElementById("your-qr-result")
var lastResult,countResults=0;
var contenedor=document.getElementById("contenedor")



//ocultar el boton de pausa
document.addEventListener('DOMContentLoaded', function() {
    var pausa=document.getElementById("my-qr-reader__dashboard_section")
    pausa.style.display="none"
    const videostr=document.getElementById("my-qr-reader__scan_region")
    //videostr.style.opacity=0

    const elements = document.querySelectorAll('*');
    elements.forEach(element => {
      element.style.borderColor = 'transparent';
    });
  });
  

var informe_estado = document.querySelector(".estado_proceso")

function onScanSuccess(decodeText,decodeResult){       
    console.log(decodeText)
    if(decodeText!==lastResult){
        ++countResults;
        lastResult=decodeText;
        reset()
        start()

        informe_estado.innerHTML="Nuevo proceso iniciado"


        function actualizar_estado(){
            informe_estado.innerHTML="Trabajando en el producto"

        }
          
          setTimeout(actualizar_estado, 2000);
    }
    else{
        stop()
        informe_estado.innerHTML="Proceso finalizado"
    }
}

var htmlscanner=new Html5QrcodeScanner(
    "my-qr-reader", {fps:1,qrbox:210})

    htmlscanner.render(onScanSuccess)

//-------------------------------------------------Cronometro de inactividad-------------------------------------------------------------
let hr2=min2=sec2=ms2="0"+0,startTimer2;
let hora_inactivo=document.querySelector(".horas_inactivo")
let minutos_inactivo=document.querySelector(".minutos_inactivo")
let segundos_inactivo=document.querySelector(".segundos_inactivo")
let milisegundos_inactivo=document.querySelector(".milisegundos_inactivo")
let boton_envio_inactivo=document.querySelector(".envio_tiempo_inactivo")


function start2(){
    const currentDateTime = new Date();
    //console.log("Recogiendo en bodega inicio a la fecha "+ currentDateTime.toLocaleString())

    startTimer2=setInterval(()=>{
        //se usa ms++ con los ++ despues para que se retorne el valor antes
        //del incremento y, por ende, empieza a contar en cero
        ms2++;
        ms2=ms2<10? "0"+ms2:ms2;
        if(ms2==100){
            sec2++;
            sec2=sec2<10? "0"+sec2:sec2;
            ms2="0"+0;
        }
        if(sec2==60){
            min2++
            min2=min2<10?"0"+min2:min2;
            sec2="0"+0;
        }
        if(min2==60){
            hr2++
            hr2=hr2<10?"0"+hr2:hr2;
            min2="0"+0;
        }
        putValue2()
    },10)
}

function stop2(){
    clearInterval(startTimer2);
    const currentTime = new Date();
    //console.log("Recogiendo en bodega termino a las "+ currentTime.toLocaleTimeString()+" el tiempo en bodega fue: "+hr+":"+min+":"+sec+":"+ms)
    hora_inactivo.value=hr2
    minutos_inactivo.value=min2
    segundos_inactivo.value=sec2
    milisegundos_inactivo.value=ms2
    boton_envio_inactivo.click()

}

function reset2(){
    clearInterval(startTimer2);
    hr2=min2=sec2=ms2="0"+0;
    putValue2()
}

function putValue2(){
    document.querySelector(".millisecond2").innerHTML=ms2
    document.querySelector(".second2").innerHTML=sec2
    document.querySelector(".minute2").innerHTML=min2
    document.querySelector(".hour2").innerHTML=hr2
}
