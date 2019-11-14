$(function() {
    if($.cookie('tab') == 'enter'){
        $('.tab1').prop('checked', true);
    }
    else if($.cookie('tab') == 'exit'){
        $('.tab2').prop('checked', true);
    }
    else{
        $('.tab1').prop('checked', true);
    }

    $('[name="tabs"]:radio').change( function() {
        if($('[id=tab1]').prop('checked')){
            $('.tabslide').slick('setPosition');
            $.cookie('tab', 'enter', {expires: 1});
        } else if ($('[id=tab2]').prop('checked')) {
            $('.tabslide2').slick('setPosition');
            $.cookie('tab', 'exit', {expires: 1});
        } 
    });
});

$(document).ready(function(){
    var slider = $('.tabslide').slick({
        autoplay: false,
        dots: false,
        infinite: true,
        rows: 2,
        slidesToShow: 5,
        slidesToScroll: 1
    });
});

$(document).ready(function(){
    var slider = $('.tabslide2').slick({
        autoplay: false,
        dots: false,
        infinite: true,
        rows: 1,
        slidesToShow: 5,
        slidesToScroll: 1
    });
});
