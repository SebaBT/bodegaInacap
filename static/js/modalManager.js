var myModal;
var cloneModal;
var cloneModalBS;
var cloneModalNewContent;
var prevURL;

function replaceModal(htmlContent, url, retornar) {
    myModal = document.getElementById("myModal")
    cloneModal = myModal.cloneNode(true)
    
    cloneModal.id = "cloneModal"
    
    if (retornar) cloneModal.childNodes[1].childNodes[1].childNodes[1].setAttribute("onClick", `openModal('${prevURL}')`)
    prevURL = url

    cloneModalNewContent = $(cloneModal.childNodes[1].childNodes[1].childNodes[3])
    cloneModalNewContent.replaceWith(htmlContent)
    document.body.insertBefore(cloneModal, myModal.nextSibling)

    cloneModalBS = new bootstrap.Modal(cloneModal)
    cloneModalBS.show()

    tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


    var lockerSelect = $('#id_locker');
    var cajaSelect = $('#id_caja');

    lockerSelect.on('change', function() {
        const lockerId = this.value;
        if (!lockerId) return
        fetch(`/api/locker/${lockerId}/cajas`)
            .then(response => response.json())
            .then(cajas => {
                cajaSelect.empty()
                cajaSelect.append('<option value="">No Caja</option>');
                cajas.forEach(caja => {
                    const option = document.createElement('option');
                    option.value = caja.id;
                    option.text = caja.nameTag;
                    cajaSelect.append(option);
                });
            });
    });


    cloneModal
    .childNodes[1]
    .childNodes[1]
    .childNodes[1]
    .addEventListener(
        'click',
        event => {
            cloneModalBS.hide()
        }
    )
}

function errorPopUp() {
    console.log("error")
}

function openModal(url, retornar)
{
    $.ajax({
            url: url,
            type: 'GET',
            dataType: 'html',
            error: errorPopUp,
            success: (htmlContent) => {
                if (retornar) {cloneModalBS.hide(); replaceModal(htmlContent, url, true);}
                else replaceModal(htmlContent, url)
            }
    });
    
}

function enviarFormulario(event,form) {
    event.preventDefault();

    var formData = new FormData(form)

    $.ajax({
        url: form.action,  
        type: 'POST',      
        data: formData,  
        dataType: 'json',
        processData: false,           
        contentType: false,              
        statusCode: {
            200: function(response) {
                if (response.status == 200) {
                    cloneModalBS.hide()
                    replaceModal(response.responseText)
                    $(".modalCloseButton").remove()
                }
            }
        },
        error: function(response) {  // For other AJAX errors
            const div = document.getElementById("errorsForm");
            div.innerHTML = '';
            for (const key in response.responseJSON) {
                $("#errorsForm").append(`<p class="text-danger">• <b>${key.charAt(0).toUpperCase() + key.slice(1)}:</b> ${response.responseJSON[key]}</p>`); 
            }
        }

    });
}

function confirmDelete(url, form) {
    $.ajax({
        url: url,
        data: $(form).serialize(),
        type: 'POST',
        dataType: 'html', 
        success: function(htmlContent) {
            closeModalBS.hide()
            replaceModal(htmlContent)
        }
    })
}