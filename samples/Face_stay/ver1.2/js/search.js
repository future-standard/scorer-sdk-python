$(document).ready(function(){
    $('[id=search]').keypress(function(e){
        if(e.which == 13){
            $.cookie('search', $(this).val(), {expires: 1});
            location.reload();
        }
    });
});

