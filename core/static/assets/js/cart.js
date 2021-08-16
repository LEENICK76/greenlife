console.log("hi");
var updateBtns = document.getElementsByClassName('update-cart');


for (var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'action:', action);
        console.log('User:', user);
        if (user === 'AnonymousUser'){
            console.log('User not authenticated');
        }
        else {
            updateUserOrder(productId, action)
        }

    });
}


function updateUserOrder(productId, action){
    console.log('User is logged in, sending data')
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action,

            })
    })
        .then((response) =>{
            return response.json()
        })
        .then((data)=>{
            console.log('data:', data)
            location.reload()
        })
}
// $(document).ready(function () {
//     $("#add-button").on('click', function (e) {
//         console.log('hello');
//         e.preventDefault();
//         $.ajax({
//             type: 'POST',
//             url: '{% url "basket:checkout" %}',
//             data: {
//                 productid: $('#add-button').val(),
//                 csrfmiddlewaretoken: '{{ csrf_token }}',
//                 action: 'post'
//             },
//             success: function (json) {
//
//             },
//             error(xhr, errmsg, err){}
//         });
//     })
// });
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