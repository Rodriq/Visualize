// alert("Hello!")



$(document).ready(function() {
    // console.log('oooooooooo---------')

    var checkState = $('#check-state').val();
    var checkSubState = $('#check-sub-state').val();
    console.log(checkState, "----------------");
    console.log(checkSubState, "----------------");
    divToShow(checkState);

    // $(window).on('load', function() {
    if (checkSubState == '1.1') {
        $('#displayFullHead').modal('show');
    } else if (checkSubState == '1.2') {
        $('#displayFullTail').modal('show');
    } else if (checkSubState == '4.1') {
        // alert(checkSubState)
        $('#displayGraph').modal('show');
    }
    // });

    function divToShow(state) {
        // var allContent = $('.content-div')
        $('.content-div').hide();
        $(`#div-${state}`).show();
    }

    function divToShow(state) {
        // var allContent = $('.content-div')
        $('.content-div').hide();
        $(`#div-${state}`).show();
    }

    $("table").addClass("table").addClass("table-striped").addClass("table-bordered").addClass("table-hover").addClass("table-sm");
    $("thead").addClass("thead-dark");

})