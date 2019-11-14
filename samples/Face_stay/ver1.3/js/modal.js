$(function(){
    $('.modal-open').click(function(){
        $('body').append('<div class="modal-overlay"></div>');
        $('.modal-overlay').fadeIn('slow');

        var modal = '#' + $(this).attr('data-target');
        modalResize();
        $(modal).fadeIn('slow');

        $('.modal-overlay, .modal-close').off().click(function(){
            $(modal).fadeOut('slow');
            $('.modal-overlay').fadeOut('slow',function(){
                $('.modal-overlay').remove();
            });
        });

        $(window).on('resize', function(){
            modalResize();
        });

        function modalResize(){
            var w = $(window).width();
            var h = $(window).height();

            var x = (w - $(modal).outerWidth(true)) / 2;
            var y = (h - $(modal).outerHeight(true)) / 2;

            $(modal).css({'left': x + 'px','top': y + 'px'});
        }

    });
});
