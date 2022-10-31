// function inc(e){
//     id = $('.cart-plus').attr('product-id').toString()
//     var ele = $(this).prev()
//     console.log(id)
//     $.ajax({
//         type : 'GET',
//         url : '/cart_plus',
//         data : {
//             id : id
//         },
//         dataType : 'json',
        
//         success : function(data){
//             ele.innerText = data.quantity
//             $('.amount').text('Rs'+ data.amount)
//             $('.s-price').text('Rs.'+ data.selling_price)
//             $('.d-price').text('Rs.'+ data.discounted_price)
//             $('.saved').text('Rs.'+ data.saved )
//             $('.t-amount').text('Rs.'+data.total_amount)
//         }
//     })
// }


$('.cart-plus').click(function(){
    id = $(this).attr('product-id').toString()
    var ele = $(this).siblings('p')
    $.ajax({
        type : 'GET',
        url : '/cart_plus',
        data : {
            id : id
        },
        dataType : 'json',
        
        success : function(data){
            ele.text( data.quantity)
            $('.amount').text('Rs'+ data.amount)
            $('.s-price').text('Rs.'+ data.selling_price)
            $('.d-price').text('Rs.'+ data.discounted_price)
            $('.saved').text('Rs.'+ data.saved )
            $('.t-amount').text('Rs.'+data.total_amount)
        }
    })
})
$('.cart-minus').click(function(){
    id = $(this).attr('product-id').toString()
    var ele = $(this).siblings('p')
    $.ajax({
        type : 'GET',
        url : '/cart_minus',
        data : {
            id : id
        },
        dataType : 'json',
        
        success : function(data){
            ele.text(data.quantity)
            $('.amount').text('Rs'+ data.amount)
            $('.s-price').text('Rs.'+ data.selling_price)
            $('.d-price').text('Rs.'+ data.discounted_price)
            $('.saved').text('Rs.'+ data.saved )
            $('.t-amount').text('Rs.'+data.total_amount)
        }
    })
})

$('.del-btn').click(function(){
    let id = $(this).attr('cart-product-id').toString()
    let element = this
    console.log(id)
    $.ajax({
        type:'GET',
        url : '/remove_product',
        dataType : 'json',
        data : {
            id : id
        },
        success : function(data){
           var e =  element.parentNode.parentNode.parentNode.parentNode.remove()
           $('.amount').text('Rs'+ data.amount)
            $('.s-price').text('Rs.'+ data.selling_price)
            $('.d-price').text('Rs.'+ data.discounted_price)
            $('.saved').text('Rs.'+ data.saved )
            $('.t-amount').text('Rs.'+data.total_amount)
        }
    })
})

