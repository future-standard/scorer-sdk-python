$(function() {
    if($.cookie('tab') == 'image1'){
        $('.tab1').prop('checked', true);
    }
    else if($.cookie('tab') == 'image2'){
        $('.tab2').prop('checked', true);
    }
    else{
        $('.tab1').prop('checked', true);
    }

    $('[name="tabs"]:radio').change( function() {
        if($('[id=tab1]').prop('checked')){
            $('.canvas1').show();
            $('.canvas2').hide();
            $.cookie('tab', 'image1', {expires: 1});
        } else if ($('[id=tab2]').prop('checked')) {
            $('.canvas1').hide();
            $('.canvas2').show();
            $.cookie('tab', 'image2', {expires: 1});
        } 
    });
});
