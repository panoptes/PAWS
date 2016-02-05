function add_chat_item(name, msg, time){

    item = '<div class="item">';
    item = item + ' <img src="/static/img/pan.png" alt="user image" class="online">';
    item = item + '  <p class="message">';
    item = item + '    <a href="#" class="name">';
    item = item + '      <small class="text-muted pull-right"><i class="fa fa-clock-o"></i> ' + time +' UTC</small>';
    item = item + name;
    item = item + '    </a>';
    item = item + msg;
    item = item + '  </p>';
    item = item + '</div><!-- /.item -->';

    $('#bot_chat').prepend(item);
}


function WebSocketTest(server) {
    if ("WebSocket" in window) {
        var ws = new WebSocket("ws://" + server + "/ws/");
        ws.onopen = function() {
            // toggle_status('on');
            // ws.send("Connection established");
        };
        ws.onmessage = function (evt) {
            var type = evt.data.split(' ', 1)[0];
            var received_msg = evt.data.substring(evt.data.indexOf(' ') + 1)

            var msg = jQuery.parseJSON(received_msg);

            if (type == 'PAN001'){
                add_chat_item(type, msg.message, msg.timestamp);
            }
            if (type == 'STATUS'){
                update_info(msg['observatory']);
                change_state(msg['state']);
                refresh_images();
            }
            if (type == 'WEATHER'){
                console.log(msg);
            }
        };
        ws.onclose = function() {
            toggle_status('off');
        };
    } else {
        toggle_status('error');
    }
}

function toggle_status(status){
    var icon = $('.current_state i');
    var text = $('.current_state span');

    icon.removeClass().addClass('fa');
    if (status == 'on'){
        icon.addClass('fa-circle');
        text.html('Online');
    } else if (status == 'off'){
        icon.addClass('fa-bolt').addClass('text-danger');
        text.html('Offline').addClass('text-danger');
    } else {
        icon.addClass('fa-exclamation-triangle', 'text-danger').addClass('text-danger');
        text.html('Error').addClass('text-danger');
    }
}

function change_state(state){
    var icon = $('.current_state i');
    var text = $('.current_state span');

    icon.removeClass().addClass('fa');
    text.html(state);
    switch(state) {
        case 'Analyzing':
            icon.addClass('fa-calculator');
            break;
        case 'Tracking':
            icon.addClass('fa-binoculars');
            break;
        case 'Observing':
            icon.addClass('fa-camera');
            break;
        case 'Pointing':
            icon.addClass('fa-dot-circle-o');
            break;
        case 'Slewing':
            icon.addClass('fa-cog fa-spin');
            break;
        case 'Scheduling':
            icon.addClass('fa-tasks');
            break;
        case 'Ready':
            icon.addClass('fa-thumbs-o-up');
            break;
        case 'Parking':
        case 'Parked':
            icon.addClass('fa-car');
            break;
        case 'Sleeping':
            icon.addClass('fa-check-circle');
            break;
        default:
            icon.addClass('fa-circle');
    }
}

// Find all the elements with the class that matches a return value
// and update their html
function update_info(status){
    $.each(status, function(key, val){
        $('.' + key).each(function(idx, elem){
            $(elem).html(val);
        })
    });
}

// Refresh all images with `img_refresh` container class
function refresh_images(){
    console.log("Refreshing images")
    $.each($('.img_refresh img'), function(idx, img){
        reload_img(img);
    });
}

// Reload individual image
function reload_img(img){
    base = $(img).attr('src').split('?')[0];

    // Hack for others
    if(base.startsWith('http')){
        new_src = $(img).attr('src');
    } else {
        new_src = base + '?' + Math.random()
    }


    $(img).attr('src', new_src);
}

// Startup
$( document ).ready(function() {
    // Image refresh timer
    second = 1000;

    WebSocketTest(window.location.host);

    // Refresh images
    // setInterval(refresh_images, 15 * second);
})
