$(document).ready(function(){
    if($.cookie('sort') == 'early_enter'){
        $('[id=sort1]').prop('selected', true);
    }
    else if($.cookie('sort') == 'late_enter'){
        $('[id=sort2]').prop('selected', true);
    }
    else if($.cookie('sort') == 'early_exit'){
        $('[id=sort3]').prop('selected', true);
    }
    else if($.cookie('sort') == 'late_exit'){
        $('[id=sort4]').prop('selected', true);
    }
    else if($.cookie('sort') == 'young_age'){
        $('[id=sort5]').prop('selected', true);
    }
    else if($.cookie('sort') == 'old_age'){
        $('[id=sort6]').prop('selected', true);
    }
    else{
        $('[id=sort1]').prop('selected', true);
    }

    $('select').change(function() {
        if($('[id=sort1]').prop('selected')){
            $.cookie('sort', 'early_enter', {expires: 1});
            location.reload();
        } else if ($('[id=sort2]').prop('selected')) {
            $.cookie('sort', 'late_enter', {expires: 1});
            location.reload();
        } else if ($('[id=sort3]').prop('selected')) {
            $.cookie('sort', 'early_exit', {expires: 1});
            location.reload();
        } else if ($('[id=sort4]').prop('selected')) {
            $.cookie('sort', 'late_exit', {expires: 1});
            location.reload();
        } else if ($('[id=sort5]').prop('selected')) {
            $.cookie('sort', 'young_age', {expires: 1});
            location.reload();
        } else if ($('[id=sort6]').prop('selected')) {
            $.cookie('sort', 'old_age', {expires: 1});
            location.reload();
        }
    });
});
