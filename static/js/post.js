var voteBtns = document.getElementsByClassName('vote')
var commentVoteBtns = document.getElementsByClassName('comment-vote')
var replyVoteBtns = document.getElementsByClassName('reply-vote')
var deleteBtns = document.getElementsByClassName('deletebtn')
var reportBtns = document.getElementsByClassName('reportbtn')
var commentBtn = document.getElementById('addCommentBtn')
var commentBox = document.getElementById('commentbox')
var textBox = document.getElementById('textbox')
var replyBtns = document.getElementsByClassName('replybtn')
var subReplyBtns = document.getElementsByClassName('subreplybtn')
var awardBtns = document.getElementsByClassName('awardBtn')
var giftBtns = document.getElementsByClassName('gift')
var buyGiftBtns = document.getElementsByClassName('buyGift')

function dev(){alerT('', 'This page is under development. Please come back later.', '#261E7D');}

function checkGuest(e, btn, msg = 'Sign in to use this feature', color = '#C9162D') {
    if (user == 'AnonymousUser') {
        //            console.log('Guest')
        btn.style.animation = 'award-shake 1s';
        alerT(e, msg, color);

        return true
    }
}


//Add Vote Functions
for (var i=0; i<voteBtns.length; i++){
    voteBtns[i].addEventListener('click', function (e){
        this.disabled = true;
        if (user == 'AnonymousUser') {
//            console.log('Guest')
            this.style.animation = 'award-shake 1s';
            console.log(this.disabled)
            if (this.disabled) {

                alerT(e, 'Oops! You have to be logged in to vote', '#C9162D');
            }
            this.disabled = false

//            location.delay(7000).reload()

        }else {
            if (this.classList.contains('selected')) {

                this.style.animation = 'award-shake 1s';
            }else{

                this.style.animation = 'award-rotate 1s';
            }

            var slug = this.dataset.slug
            var poll = this.dataset.poll
            console.log('Class:', this.classList.contains('selected'))
            console.log('Slug:', slug)
            console.log('Poll:', poll)
            console.log('USER:', user)
            updateArticleVote(slug, poll)
        }
//        location.reload()
//        $('#articlevotes').load(location.href+ ' #articlevotes')
//        $('#novote').load(location.href+ ' #novote')

    })

}

for (var i=0; i<commentVoteBtns.length; i++){
    commentVoteBtns[i].addEventListener('click', function (e){
        if (user == 'AnonymousUser'){

            this.style.animation = 'award-shake 1s';
            alerT(e, 'Oops! You have to be logged in to vote', '#C94B0C');

        }else{
             if (this.classList.contains('selected')){

                this.style.animation = 'award-shake 1s';
            }else{
                this.style.animation = 'award-rotate 1s';

            }
            var slug = this.dataset.article
            var id = this.dataset.comment
            var poll = this.dataset.poll
            updateCommentVote(slug, poll, id)
        }
    })

}

for (var i=0; i<replyVoteBtns.length; i++){
    replyVoteBtns[i].addEventListener('click', function (e){
        if (user == 'AnonymousUser'){

            this.style.animation = 'award-shake 1s';
            alerT(e, 'Oops! You have to be logged in to vote', '#C94B0C');

        }else{
             if (this.classList.contains('selected')){

                this.style.animation = 'award-shake 1s';
            }else{
                this.style.animation = 'award-rotate 1s';

            }
        
            var slug = this.dataset.article
            var comment_id = this.dataset.comment
            var id = this.dataset.reply
            var poll = this.dataset.poll
            updateReplyVote(slug, poll, comment_id, id)
            }
    })

}

function updateArticleVote(slug, poll) {
    console.log('Sending data..')
    var url = '/update_article_vote/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({'Slug': slug, 'Poll': poll})

    })
    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        console.log('Loading..')
//        location.reload()
        console.log($( "#yesvote" ).text())
        $( "#yesvote" ).load(location.reload() + " #yesvote");
//        $( "#articlevotes" ).load(window.location.href + " #articlevotes");
//        document.getElementById('yesvote').innerHTML = data['y'];
//        document.getElementById('novote').innerHTML = data['n'];

    })

}

function updateCommentVote(slug, poll, id) {
    console.log('Sending data..')
    var url = '/update_comment_vote/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({'Slug': slug, 'Poll': poll, 'ID': id})

    })
    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })

}

function updateReplyVote(slug, poll, comment_id, id) {
    console.log('Sending reply data..')
    var url = '/update_reply_vote/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({'Slug': slug, 'Poll': poll, 'ID': id, 'Comment ID': comment_id})

    })
    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })

}


//Add Comment Functions
try {

    commentBtn.addEventListener('click', function (){

        if (!checkGuest('', this)){
        showHide(commentBtn, commentBox, textBox)
        }
    })
}catch(err){}

function showHide(commentBtn, commentBox, textBox){

    document.addEventListener('mouseup', function(e) {
        var container = commentBox;
        if (!container.contains(e.target)) {
            container.style.display = 'none';
            try {
                commentBtn.innerText = 'Add Comment';
                commentBtn.style.display = 'block';
                document.getElementById('cancelBtn').style.display = 'none';
                } catch (err){}
        }
    });

    display = commentBox.style.display
    if (display === 'block') {
        commentBox.style.display = 'none';
        commentBtn.innerText = 'Add Comment';
    }else{
        commentBox.style.display = 'block';
        if(textBox){
        textBox.focus();
        }
//        textBox.select();
//        commentBtn.innerText = 'Cancel';
        try {
            commentBtn.style.display = 'none';
            document.getElementById('cancelBtn').style.display = 'block';
            } catch (err){}

    }

}

for (var i=0; i<replyBtns.length; i++){
    replyBtns[i].addEventListener('click', function () {

        if (!checkGuest('', this, 'Sign in to join this conversation!', '#BD690B')){
            var comment_id = this.dataset.comment
            // console.log('Comment Id:', comment_id)
            replyBox = document.getElementById('replybox-'+comment_id)
            textBox = document.getElementById('textbox-'+comment_id)
            showHide('', replyBox, textBox)
            }
    })
}

for (var i=0; i<subReplyBtns.length; i++){
    subReplyBtns[i].addEventListener('click', function () {
    if (!checkGuest('', this)){
        var reply_id = this.dataset.reply
        // console.log('Comment Id:', comment_id)
        replyBox = document.getElementById('subreplybox-'+reply_id)
        textBox = document.getElementById('subtextbox-'+reply_id)
        showHide('', replyBox, textBox)
        // cancelBox = document.getElementById('subreplycancelbox-'+comment_id)
        // cancelBox.addEventListener('click', showHide('', replyBox))
    }
    })
}

// Awards
for (var i=0; i<giftBtns.length; i++){
    giftBtns[i].addEventListener('click', function (e){
        var award_id = this.dataset.id
        var owner = this.dataset.owner
        var parent = this.dataset.parent
        var award = this.dataset.award
        var award_data = [award_id, owner, parent, award]
        console.log(e)
        sendAward(award_data)
        e.preventDefault()
//        awardBox.style.display = 'block'
    })}

function sendAward(award_data, quantity=1) {
    // award_data = {id, owner, parent, award}
    id = award_data[0]
    owner = award_data[1]
    parent = award_data[2]
    award = award_data[3]
    console.log('Sending award..')
    var url = '/gift/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({'id': id, 'owner': owner, 'parent': parent, 'award': award, 'quantity': quantity})

    })
    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        // alerT('', data, 'green')
        location.reload()
    })

}

function logAward(log_data){
    var status = log_data.status
    var email = log_data.email
    var award = log_data.award
    var  price = log_data.price
    // var  = log_data.
    var url = '/award_transaction/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({'status': status, 'email': email, 'award': award, 'price': price})

    })
    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        // alerT('', data, 'green')
        location.reload()
    })

}

for (var i=0; i<buyGiftBtns.length; i++){
    buyGiftBtns[i].addEventListener('click', function (e){

        alerT('', 'Initializing payment...', '#12081a');
        var guest = this.dataset.auth
        var award_id = this.dataset.id
        var owner = this.dataset.owner
        var parent = this.dataset.parent
        var award = this.dataset.award
        var award_data = [award_id, owner, parent, award]
        var extras = this.dataset.extra.split(', ')
       if(guest){

            
            makePayment(extras, award_data)

        } else {
            makePayment(extras, award_data, 5) 
        }
        // makePayment();

    })}

function makePayment(extras, award_data, award_quantity=1) {
    var price = extras[0]
    var award_name = extras[1]
    var email = extras[2]
    var log_data = {'status': 'initialized', 'email': email, 'price': price, 'award': award_name}
        
    FlutterwaveCheckout({
        public_key: "FLWPUBK_TEST-SANDBOXDEMOKEY-X",
        tx_ref: "tr-" + randx(12),
        amount: price,
        currency: "NGN",
        payment_options: "card, banktransfer, ussd",
        callback: function(payment){
        console.log(payment) 
        if(payment.status == 'successful' || payment.status == 'completed'){
            sendAward(award_data, award_quantity);
            log_data.status = 'processing'
            logAward(log_data)
        }else{
            log_data.status = 'unsuccessful'
            logAward(log_data)
        }
        
    },
    onclose: function(incomplete) {
        if (incomplete === true) {
            // Record event in analytics
            log_data.status = 'incomplete'
            logAward(log_data)
        }},
        //   redirect_url: "https://glaciers.titanic.com/handle-flutterwave-payment",
        //   redirect_url: "javascript: window.history.go(0)",
        // meta: {consumer_id: 23, consumer_mac: "92a3-912ba-1192a",},
        customer: {
        email: email,
        // name: "Rose DeWitt Bukater",
        },
        customizations: {
        title: "You will Receive \n'" + award_name + "' X" + award_quantity,
        description: "The place to be..",
        logo: "http://127.0.0.1:8000/static/img/red_people.png",
        },
    });
    }

      
// Delete Buttons
for (var i=0; i<deleteBtns.length; i++){
    deleteBtns[i].addEventListener('click', function (e){
        var id = this.dataset.id
        var type = this.dataset.type
        var confirm_box_id = 'del_'+ id
        var confirmBox = document.getElementById(confirm_box_id)
        showHide('', confirmBox, '')

        }
    )
}


// Report Buttons
for (var i=0; i<reportBtns.length; i++){
    reportBtns[i].addEventListener('click', function (e){
        var id = this.dataset.id
        alerT('', 'Comment has been sent to our team for review!', '#920331')
//        alerT('', 'Comment ' + id + ' has been sent to our team for review. Thanks B!', '#920331')

        }
    )
}
