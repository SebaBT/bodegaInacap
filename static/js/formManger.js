$(document).on('input', '#id_rut', function() {
    console.log("hola")
    $("#id_rut").inputmask({
        mask: '(9(.999){2}-K)|(99(.999){2}-K)',
        autoUnmask: false, //para que .val() devuelva sin mascara (sin puntos ni guion)
        keepStatic: false, //para que el formato de mascara mas corta se mantenga hasta que sea necesario el mas largo
        showMaskOnFocus: false, //oculta la mascara en focus
        showMaskOnHover: false, //oculta la mascara en hover
        definitions: {
            'K': {
                validator: '[0-9|kK]',
                casing: 'upper',
            }
        }
    }); 
});


$(document).on('click', '#imgPreview', function() {
    $("#id_adjunto").click();
    
    var reader = new FileReader();
    reader.onload = function(e) {
        $("#imgPreview").attr("src",e.target.result);
    }
    $("#id_adjunto").on('change', () => {
        reader.readAsDataURL($("#id_adjunto")[0].files[0])
    })
})