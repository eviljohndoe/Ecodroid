$(document).ready(function(){

   $('form#wallpaper').on('submit', function(event){
        event.preventDefault();

        var project_id = document.wallpaper.elements['project_id'].value;
        var url = Flask.url_for("project.upload", {"id": project_id})

        upload($(this), url)
   });

   $('form#apks').on('submit', function(event){
        event.preventDefault();

        var url = Flask.url_for("apk.upload")

        upload($(this), url)

   });

   $('form#link_apks').on('submit', function(event){
        event.preventDefault();

        var project_id = document.link_apks.elements['project_id'].value;
        var url = Flask.url_for("project.add_apk", {"id": project_id})
        submit($(this), url)
   });

   function upload(form, url){
        var progressBar = $("#progressBar");
        var formData = new FormData(form[0]);
        var fieldset = form.children("fieldset");
        fieldset.prop('disabled', true);

        progressBar.parent().first().removeClass('hide');
        $.ajax({
            xhr : function(){
                var xhr = new window.XMLHttpRequest();

                xhr.upload.addEventListener('progress', function(e){
                    if(e.lengthComputable) {
                        //console.log('Bytes Loaded: ' + e.loaded);
                        //console.log('Total Size: ' + e.total);
                        //console.log('Percentage uploaded: ' + (e.loaded / e.total));

                        var percent = Math.round(e.loaded / e.total * 100)

                        progressBar.attr('aria-valuenow', percent)
                            .css('width', percent + '%').text(percent + '%')
                    }
                });

                return xhr
            },
            type : 'POST',
            url : url,
            data : formData,
            processData : false,
            contentType : false,
            success : function(data){
                console.log(data)
                fieldset.prop('disabled', false)
                progressBar.parent().first().addClass('hide');
                location.reload()
            }
        })
   }

   function submit(form, url){
        var formData = new FormData(form[0]);
        var spinner = $("#submit").children("span");
        var fieldset = form.children("fieldset");
        fieldset.prop('disabled', true);

        spinner.removeClass("hide");

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            processData: false,
            contentType: false,
            success: function(data){
                console.log(data)
                fieldset.prop('disabled', false)
                spinner.removeClass("hide");
                location.reload()
            }
        })
   }

});