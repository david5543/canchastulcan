document.addEventListener("DOMContentLoaded", function () {
    var alertas = document.querySelectorAll(".alert");
    alertas.forEach(function (alerta) {
        setTimeout(function () {
            var instancia = bootstrap.Alert.getOrCreateInstance(alerta);
            instancia.close();
        }, 6000);
    });

    var celdas = document.querySelectorAll(".celda-horario[data-href]");
    celdas.forEach(function (celda) {
        celda.addEventListener("click", function () {
            window.location.href = celda.dataset.href;
        });
    });

    var inputComprobante = document.getElementById("comprobante");
    if (inputComprobante) {
        inputComprobante.addEventListener("change", function () {
            var nombre = inputComprobante.files.length ? inputComprobante.files[0].name : "Ningún archivo seleccionado";
            var etiqueta = document.getElementById("nombre-archivo");
            if (etiqueta) {
                etiqueta.textContent = nombre;
            }
        });
    }
});
