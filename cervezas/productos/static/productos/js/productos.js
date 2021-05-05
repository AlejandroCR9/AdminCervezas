$(function () {
    
    /*
     * Envia una peticion al servidor para obtener un formulario
     * que se mostrara en un modal.
     */
    var loadForm = function () {
        var btn = $(this);     //Obtiene la instancia del boton presionado
        $.ajax({    
            url: btn.attr("data-url"),  //Obtiene el atributo "data-url" 
                                        //que contiene la url del servico 
            type: 'get',                //Asigna el tipo de peticion que se hara
            dataType: 'json',           //Formato de la peticion
            //Antes de que la peticion se envie se muestra el modal
            beforeSend: function () {   
                //Limpiamos el modal de cualquier contenido que tenga
                $("#modal-acciones .modal-content").html("");
                //Mostramos el modal
                $("#modal-acciones").modal("show");
            },
            success: function (data) {
                //Una vez que la peticion se haya cumplido se actualiza el contenido del modal
                $("#modal-acciones .modal-content").html(data.html_form);
            }
        });
    };
    /*
     * Envia una peticion al servidor para guardar, datos
     * en el servidor.
     */
    var saveForm = function () {
        var form = $(this);     //Obtiene la instancia del formulario que se esta enviando
        $.ajax({
            url: form.attr("action"),   //Obtiene el contenido del atributo action
                                        //pues contiene la url del servicio
            data: form.serialize(),     //Convertimos los camos del form en un string
            type: form.attr("method"),  //Obtenemos el tipo de request que se hara y asignamos
            dataType: 'json',           //Formato de la peticion
            success: function (data) {
                //Si la peticion ha salido bien, se verifica que los datos del formulario 
                // enviado hayan sido correctos
                if (data.form_is_valid) {
                    //Se actualiza la tabla
                    $("#productos-table tbody").html(data.html_list);
                    //Se oculta el modal
                    $("#modal-acciones").modal("hide");
                    $("#alert").html(`<div class="alert alert-warning alert-dismissible fade show" role="alert">
                                            La acción se llevo acabo.
                                            <button type="button" class="btn-close" 
                                            data-bs-dismiss="alert" aria-label="Close"></button>
                                    </div>`);
                }
                else {
                    //El modal permanece y se muestran los errores de formulario
                    $("#modal-acciones .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };
    $("#alert-demo-success").click(function() {
       
      });
    /* Enlazamos los metodos a sus respectivos botones */
                    //+===========PRODUCTOS=========//
    // Create producto
    $(".js-create-producto").click(loadForm);
    $("#modal-acciones").on("submit", ".js-producto-create-form", saveForm);
  
    // edit producto
    $("#productos-table").on("click", ".js-edit-producto", loadForm);
    $("#modal-acciones").on("submit", ".js-producto-edit-form", saveForm);
  
    // Delete prodcuto
    $("#productos-table").on("click", ".js-delete-producto", loadForm);
    $("#modal-acciones").on("submit", ".js-producto-delete-form", saveForm);
  
  });