window.zindex = 1;

$(document).ready(function(e){
    $("#mnxElecciones a").click(function(event){
        event.preventDefault();

        let modulo = $(this).data("modulo"),
            formulario = $(this).data("formulario");
        abrir_ventana(modulo, formulario);
    });

    $("#frmToken").submit(function(event){
        event.preventDefault();

        let txttoken = $("#token").val();

        token(txttoken);
    });
});
function abrir_ventana(modulo, formulario){
    $(`#${modulo}_${formulario}`).load(`${modulo}/${modulo}_${formulario}.html`)
        .draggable()
        .click(function(e){
            $(this).css("z-index", ++zindex);
        });
}
function token(txttoken){
    $.get('http://localhost:3000/admin/'+txttoken, function(data){
        if(data.response.status == 'ok'){
            $('#menuBar').css('display', 'flex');
            $("#frmToken").hide();
        }else{
            $('#menuBar').css('display', 'none');
            $("#frmToken").show();
        }
    }, 'json');
}