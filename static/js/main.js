$('#infobtn').click(function(){alerT('', 'Stop!', 'blue');});

$('#read-more').click(function(){
    $('#mid-content').hide();
    $('#full-content').show();
    console.log($('#mid-content'));
});

function alerT(event, text='Hey! This is a success message!!', color='green'){
//    console.log('EResult:', e.result)
//    if(!event.detail || event.detail == 1){
//    console.log(event)

    $('#navHeader').hide();
    $('#infoContent').text(text);
    $('#info').css('font-family', 'sans-serif');
    $('#info').css('background-color', color);
    $('#info').slideDown();
//    $('#info').delay(5000).fadeOut('slow');

    var ty = setTimeout(function() {
        $('#info').fadeOut('slow');
        $('#navHeader').fadeIn();

    }, 5000);


};

//$('#dprofile').click(function(){alerT('', 'Stop!', 'blue');}
$('.awardBtn').click(function(){
//    console.log('clicked')
    var awardBox = $('#db-' + this.classList[1])
//    console.log(awardBox)
    $(document).mouseup(function(e)
    {
        var container = awardBox;

        // if the target of the click isn't the container nor a descendant of the container
//        if (!container.is(e.target) && $('.awardBtn').is(e.target))
        if (!container.is(e.target) && container.has(e.target).length === 0)
        {
            container.hide();
        }
    });

    awardBox.toggle()
})


function randx(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * 
 charactersLength));
   }
   return result;
}
