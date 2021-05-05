$(function () {
    /*
     * Envia una peticion al servidor para obtener un formulario
     * que se mostrara en un modal.
     */
    var loadForm = function () {
        var btn = $(this);      //Obtiene la instancia del boton presionado
        $.ajax({
            url: btn.attr("data-url"),  //Obtiene el atributo "data-url" \
                                        //que contiene la url del servico 
            type: 'get',                //Asigna el tipo de peticion que se hará
            dataType: 'json',           //Formato de la petición
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
                    //Si son correctos se verifica que tabla se afecto y se actualiza
                    if(data.type) {
                        $("#marca-table tbody").html(data.html_list);
                    } 
                    else  {
                        $("#presentacion-table tbody").html(data.html_list);
                    }
                    //Se oculta el modal con el formulario
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
  
  
    /* Enlazamos los metodos a sus respectivos botones */
                    //+===========Marcas=========//
    // Create marca
    $(".js-create-marca").click(loadForm);
    $("#modal-acciones").on("submit", ".js-marca-create-form", saveForm);
  
    // edit marca
    $("#marca-table").on("click", ".js-edit-marca", loadForm);
    $("#modal-acciones").on("submit", ".js-marca-edit-form", saveForm);
  
    // Delete marca
    $("#marca-table").on("click", ".js-delete-marca", loadForm);
    $("#modal-acciones").on("submit", ".js-marca-delete-form", saveForm);


                    //+======Presentaciones=========//
    // Create presentacion
    $(".js-create-presentacion").click(loadForm);
    $("#modal-acciones").on("submit", ".js-presentacion-create-form", saveForm);
  
    // edit presentacion
    $("#presentacion-table").on("click", ".js-edit-presentacion", loadForm);
    $("#modal-acciones").on("submit", ".js-presentacion-edit-form", saveForm);
  
    // Delete presentacion
    $("#presentacion-table").on("click", ".js-delete-presentacion", loadForm);
    $("#modal-acciones").on("submit", ".js-presentacion-delete-form", saveForm);
  
  });
  