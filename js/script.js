document
    .getElementById("contactForm")
    .addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevenir la recarga de la página

    const nombre = document.getElementById("nombre").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const mensaje = document.getElementById("mensaje").value.trim();
    const resultado = document.getElementById("resultado");

    try {
      // Enviar los datos usando fetch()
        const response = await fetch("/ayuda", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ nombre, correo, mensaje }),
    });

    if (response.ok) {
        resultado.textContent = "¡Mensaje enviado con éxito!";
        resultado.style.color = "green";
    } else {
        resultado.textContent = "Hubo un error al enviar el mensaje.";
        resultado.style.color = "red";
    }
    } catch (error) {
    resultado.textContent = "Hubo un error al enviar el mensaje.";
    resultado.style.color = "red";
    }
});



// Funcion creada para el boton volver arriba
window.onscroll = function() {
    const button = document.getElementById("volver-arriba");
    if (document.documentElement.scrollTop > 850) {
        button.style.display = "block";
    } else{
        button.style.display = "none";
    }
}

function volverArriba(){
    window.scrollTo({
        top:0,behavior: "smooth"})
}
