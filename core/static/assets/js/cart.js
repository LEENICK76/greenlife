// var updateBtns = document.getElementsByClassName('update-cart');
// var updateBtns = document.get

//
// for (var i=0; i<updateBtns.length; i++){
//     updateBtns[i].addEventListener('click', function () {
//         var prodId = this.dataset.product;
//         var action = this.dataset.action;
//         console.log('prodId:', prodId, 'action:', action);
//     });
// }
$(document).ready(function () {
    $("#add-button").on('click', function (e) {
        console.log('hello');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '{% url "basket:checkout" %}',
            data: {
                productid: $('#add-button').val(),
                csrfmiddlewaretoken: '{{ csrf_token }}',
                action: 'post'
            },
            success: function (json) {

            },
            error(xhr, errmsg, err){}
        });
    })
});
// $(document).on('click', "#add-button", function (e) {
//     e.preventDefault();
//     var url = '{% url "basket:checkout" %}';
//
//     $.ajax({
//         type: 'POST',
//         url: url,
//         data: {
//             productid: $('#add-button').val(),
//             csrfmiddlewaretoken: '{{ csrf_token }}',
//             action: 'post'
//         },
//         success: function (json) {
//
//         },
//         error: function (xhr, errmsg, err) {}
//     });
// });