var voteBtns = document.getElementsByClassName('vote')
var commentVoteBtns = document.getElementsByClassName('comment-vote')
var replyVoteBtns = document.getElementsByClassName('reply-vote')

function dev(){alerT('', 'This page is under development. Please come back later.', '#261E7D');}

function checkGuest(e, btn) {
    if (user == 'AnonymousUser') {
        //            console.log('Guest')
        btn.style.animation = 'award-shake 1s';
        alerT(e, 'Oops! You are not logged in', '#C9162D');

        return true
    }
}

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
            console.log('Slug:', slug)
            console.log('ID:', id)
            console.log('Poll:', poll)
            console.log('USER:', user)
            updateCommentVote(slug, poll, id)
        }
    })

}

for (var i=0; i<replyVoteBtns.length; i++){
    replyVoteBtns[i].addEventListener('click', function (){
        if (user == 'AnonymousUser' || this.classList.contains('selected')){
            this.style.animation = 'award-shake 1s';

        }else{
            this.style.animation = 'award-rotate 1s';

        }
        
        var slug = this.dataset.article
        var comment_id = this.dataset.comment
        var id = this.dataset.reply
        var poll = this.dataset.poll
        console.log('Slug:', slug)
        console.log('Comment ID:', comment_id)
        console.log('Reply ID:', id)
        console.log('Poll:', poll)
        console.log('USER:', user)
        updateReplyVote(slug, poll, comment_id, id)
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



/* Add Comment Function */

var commentBtn = document.getElementById('addCommentBtn')
var commentBox = document.getElementById('commentbox')
var textBox = document.getElementById('textbox')

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
        textBox.focus();
//        textBox.select();
//        commentBtn.innerText = 'Cancel';
        try {
            commentBtn.style.display = 'none';
            document.getElementById('cancelBtn').style.display = 'block';
            } catch (err){}

    }

}


// Comment Function
var replyBtns = document.getElementsByClassName('replybtn')
var subReplyBtns = document.getElementsByClassName('subreplybtn')

for (var i=0; i<replyBtns.length; i++){
    replyBtns[i].addEventListener('click', function () {

        if (!checkGuest('', this)){
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
        var comment_id = this.dataset.reply
        // console.log('Comment Id:', comment_id)
        replyBox = document.getElementById('subreplybox-'+comment_id)
        textBox = document.getElementById('subtextbox-'+comment_id)
        showHide('', replyBox, textBox)
        // cancelBox = document.getElementById('subreplycancelbox-'+comment_id)
        // cancelBox.addEventListener('click', showHide('', replyBox))
    }
    })
}


// Awards

//var awardBtns = document.getElementsByClassName('awardBtn')
//
//for (var i=0; i<awardBtns.length; i++){
//    awardBtns[i].addEventListener('click', function (e){
//        var awardBox = $('#db-' + this.classList[1])
//        awardBox.style.display = 'block'
//    })}
