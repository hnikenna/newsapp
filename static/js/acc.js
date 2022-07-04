
$(function(){

$(window).bind("resize",function(){
    console.log($(this).width())
    if($(this).width() <500){
    $('#acc1').removeClass('split')
    $('#acc2').hide()
//    console.log('Test 1')
    }
    else{
    $('#acc1').addClass('split')
    $('#acc2').show()
//    console.log($(this).width())
    }
})
})
