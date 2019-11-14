$(document).ready(function(){
    $('[id=name_regi]').keypress(function(e){
        if(e.which == 13){
            console.log($(this).val())
            console.log($(this).attr('name'))

            /*
            imgpath = $(this).attr('name')
            array = imgpath.split('/');
            dir = array[1]
            imgname = array[2]
            array = imgname.split('.');
            id = array[0]
            console.log('[id=' + dir + '_' + id +']')
            
            $('[id=' + dir + '_' + id +']').attr('src', 'images/process.gif');
            console.log($('[id=' + dir + '_' + id +']').children('img'))
            */

            $(this).prop('disabled', true);

            $.ajax({
                url: "name_regi.php",
                type: "post",
                dataType: "text",
                data:{'imgpath':$(this).attr('name'), 'name':$(this).val()}

            }).done(function (response) {
                alert('Registration succeeded');
                location.reload();
                
                //var array = JSON.parse(response);
                //console.log(array)
                //$("div#info").html('<div class="alert alert-success" role="alert" id="info">' + array + '</div>');

            }).fail(function (xhr,textStatus,errorThrown) {
                alert('error');
                location.reload();
            });
        }
    });
});
