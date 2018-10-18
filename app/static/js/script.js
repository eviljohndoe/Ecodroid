//-----------------------EDIT PROJECT NAME DIALOG----------------------//
function edit(project_id) {
    /* Act on the event */
    var url = Flask.url_for("project.edit", {"id": project_id});
    $.get(url, function(data){
        $('#editProjectDialog .modal-content').html(data)
        $('#editProjectDialog').modal();

        $('#submit').click(function(event) {
            //Act on the event
            event.preventDefault();
            $.post(url, data=$('#editProjectForm').serialize(), function(data, textStatus, xhr) {
                //optional stuff to do after success
                if (data.status == 'ok') {
                    $('#editProjectDialog').modal('hide');
                    location.reload();
                }
                else{
                    $('#editProjectDialog .modal-content').html(data);
                }
            });
        });
    });
}
//-----------------------END EDIT PROJECT NAME DIALOG----------------------//

//-----------------------UPLOAD MULTIPLE FILE----------------------//
function bs_input_file(el) {
    var _element;
    if(el == ".input-apk"){
        _element = $("<input type='file' multiple='' name='file[]' class='input-ghost' style='visibility:hidden; height:0'>");
    }else{
        _element = $("<input type='file' name='file' class='input-ghost' style='visibility:hidden; height:0'>");
    }
    $(el).before(
        function() {
            var submit = $(this).parents("fieldset").children('div').children('button')
            submit.prop('disabled', true);
            if ( ! $(this).prev().hasClass('input-ghost') ) {
                var element = _element//$("<input type='file' multiple='' name=" + file + " class='input-ghost' style='visibility:hidden; height:0'>");
                element.attr("name",$(this).attr("name"));
                element.change(function(){
                    submit.prop('disabled', false)
                    var names = [];
                    for(var i = 0; i < element.get(0).files.length; i++){
                        names.push(element.get(0).files[i].name);
                    }
                    //element.next(element).find('input').val((element.val()).split('\\').pop());
                    element.next(element).find('input').val(names)
                });
                $(this).find("button.btn-choose").click(function(){
                    element.click();
                });
                $(this).find("button.btn-reset").click(function(){
                    submit.prop('disabled', true)
                    element.val(null);
                    $(this).parents(el).find('input').val('');
                });
                $(this).find('input').css("cursor","pointer");
                $(this).find('input').mousedown(function() {
                    $(this).parents(el).prev().click();
                    return false;
                });
                return element;
            }
        }
    );
}
//-----------------------END UPLOAD MULTIPLE FILE----------------------//


//-----------------------DATATABLES USING datatables.js----------------------//
function create_table(){
    savedDevices()
    connectedDevices()
    project()
    apk()
}

function savedDevices(){
    $("#all_devices").DataTable();
}

function connectedDevices(){
    $("#plugged").DataTable()
}

function project(){
    $("#project").DataTable()
}

function apk(){
    $("#apk").DataTable()
}


function configure(){
}

//-----------------------END DATATABLES----------------------//

$(function() {
    bs_input_file(".input-apk");
    bs_input_file(".input-wallpaper");
});

$( window ).on( "load", create_table );